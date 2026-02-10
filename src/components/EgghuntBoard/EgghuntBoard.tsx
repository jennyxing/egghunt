import { useEffect, useState } from "react";
import type { BoardProps } from 'boardgame.io/react';
import "./EgghuntBoard.css";
import Tile from '../Tile/Tile';
import RoundEndInfo from "../RoundEndInfo/RoundEndInfo";
import axios from "axios";
import { serverURL } from "../../context/LobbyContext";

type MoveLog = {
    action: "chick1" | "agent1" | "agent2" | undefined
    x: number,
    y: number,
    move: "up" | "down" | "left" | "right" | "stay"
}

const EgghuntBoard = ({ G, ctx, moves, matchData, log }: BoardProps) => {
    const [showRoundEndInfo, setShowRoundEndInfo] = useState(false)

    const checkIfAllPlayersAreConnected = (): boolean => {
        //this is to support local development
        if (!matchData && import.meta.env.VITE_IS_LOCAL === 'true') {
            return true;
        }
        if (!matchData) {
            return false;
        }
        return matchData.every(playerMetadata => {
            return playerMetadata.isConnected
        })
    }

    const checkIfPlayerDisconnected = (): boolean => {
        if (!matchData && import.meta.env.VITE_IS_LOCAL === 'true') {
            return false;
        }
        if (!matchData) {
            return true;
        }
        return matchData.some((playerMetadata) => {
            return playerMetadata.isConnected === false
        })
    }

    const handleKeyDown = (e: KeyboardEvent) => {
        switch (e.code) {
            case "ArrowUp":
                e.preventDefault();
                moves.moveUp({
                    action: "up" // this is passed to the log's action.payload.args[0]
                });
                break;
            case "ArrowDown":
                e.preventDefault();
                moves.moveDown({
                    action: "down" // this is passed to the log's action.payload.args[0]
                });
                break;
            case "ArrowLeft":
                e.preventDefault();
                moves.moveLeft({
                    action: "left" // this is passed to the log's action.payload.args[0]
                });
                break;
            case "ArrowRight":
                e.preventDefault();
                moves.moveRight({
                    action: "right" // this is passed to the log's action.payload.args[0]
                });
                break;
            case "Space":
                e.preventDefault();
                moves.stayInPlace({
                    action: "stay" // this is passed to the log's action.payload.args[0]
                });
                break;
            default:
                break;
        }
    }

    useEffect(() => {
        window.addEventListener("keydown", handleKeyDown, false)
        return () => {
            window.removeEventListener("keydown", handleKeyDown, false)
        }
    }, [])

    useEffect(() => {
        if (ctx.phase === "chickenPhase" && checkIfAllPlayersAreConnected()) {
            setTimeout(() => {
                moves.moveChicken();
            }, 2000);
        }
    }, [ctx.phase, matchData])

    useEffect(() => {
        if (ctx.gameover !== undefined) {
            const recordRoundResults = async () => {
                const postData = {
                    agent1_pts: ctx.gameover.p1Score,
                    agent2_pts: ctx.gameover.p2Score,
                    bgio_match_id: localStorage.getItem("matchID"),
                    total_trials: G.trialsPlayed
                }
                try {
                    const res = await axios.post(`${serverURL}/tasks/egghunt/round_results`, postData);
                    localStorage.setItem("p1TotalScore", res.data.agent1_score);
                    localStorage.setItem("p2TotalScore", res.data.agent2_score);
                } catch (error) {
                    console.error(error)
                }
            }
            recordRoundResults()
        }

        if (ctx.gameover) {
            setTimeout(() => {
                setShowRoundEndInfo(true)
            }, 3000);
        }
    }, [ctx.gameover])

    useEffect(() => {
        if (G.trialsPlayed !== 0) {
            const recordTrial = async () => {
                const postData = {
                    agent1_pts: ctx.gameover ? ctx.gameover.p1Score : G.p1Score,
                    agent2_pts: ctx.gameover ? ctx.gameover.p2Score : G.p2Score,
                    outcome: ctx.gameover ? ctx.gameover.outcome : "none",
                    trial_number: G.trialsPlayed,
                    bgio_match_id: localStorage.getItem("matchID"),
                }
                try {
                    await axios.post(`${serverURL}/tasks/egghunt/trials`, postData);
                } catch (error) {
                    console.error(error)
                }
            }
            recordTrial();
        }
    }, [G.trialsPlayed])

    useEffect(() => {
        if (log.length !== 0) {

            const mostRecentMove = log.filter(logItem => logItem.action.type === "MAKE_MOVE").at(-1);
            //maps name of move to the move that needs to be recorded
            function determinePlayer() {
                if (mostRecentMove?.action.payload.type === "moveChicken") {
                    return "chick1"
                } else {
                    if (mostRecentMove?.action.payload.playerID === "0") {
                        return "agent1"
                    }
                    if (mostRecentMove?.action.payload.playerID === "1") {
                        return "agent2"
                    }
                }
            }

            function determineMoveLocation() {
                if (mostRecentMove?.action.payload.type === "moveChicken") {
                    return G.chickenPosition
                } else {
                    if (mostRecentMove?.action.payload.playerID === "0") {
                        return G.p1Position
                    }
                    if (mostRecentMove?.action.payload.playerID === "1") {
                        return G.p2Position
                    }
                }
            }

            const recordMove = async () => {
                const newMoveLog: MoveLog = {
                    action: mostRecentMove?.action.payload.args[0]?.action || G.chickenDirectionOfLastMove,
                    player: determinePlayer(),
                    ...determineMoveLocation()
                }
                const postData = {
                    ...newMoveLog,
                    trial_number: ctx.phase === "chickenPhase" || ctx.phase === null ? G.trialsPlayed : G.trialsPlayed + 1, // this calculation is needed so that the temp_trial_id is contructed correctly
                    bgio_match_id: localStorage.getItem("matchID"),
                }
                try {
                    await axios.post(`${serverURL}/tasks/egghunt/moves`, postData);
                } catch (error) {
                    console.error(error)
                }
            }

            recordMove();
        }
    }, [ctx.turn, ctx.gameover])

    const computeContentOfTile = (x: number, y: number) => {
        if (x === G.p1Position.x && y === G.p1Position.y) {
            return "p1"
        }
        if (x === G.p2Position.x && y === G.p2Position.y) {
            return "p2"
        }
        if (x === G.chickenPosition.x && y === G.chickenPosition.y) {
            return "chicken"
        }
        return;
    }

    //this function will output a direction if the particular tile needs to be animated
    //due to how boardgame.io manages turns/phases, the animation has to occur at the beginning of the next player's turn
    const computeAnimationDirection = (x: number, y: number) => {
        // if the current phase is the chickenPhase, then second player (player at playOrder[1]) needs to animate the direction of their last move
        if (ctx.phase === "chickenPhase") {
            if (ctx.playOrder[1] === "0") {
                if (x === G.p1Position.x && y === G.p1Position.y) {
                    return G.p1DirectionOfLastMove
                }
            } else if (ctx.playOrder[1] === "1") {
                if (x === G.p2Position.x && y === G.p2Position.y) {
                    return G.p2DirectionOfLastMove
                }
            } else {
                return "down"
            }
        }
        //if the current phase is the playerPhase:
        if (ctx.phase === "playerPhase") {
            if (ctx.playOrderPos === 0) {
                // if it is the first player's turn, then the chicken needs to animate (since the chicken always goes before the first player)
                if (x === G.chickenPosition.x && y === G.chickenPosition.y) {
                    return G.chickenDirectionOfLastMove
                }
            } else if (ctx.playOrderPos === 1) {
                //if it is the second player's turn, then the first player (at playOrder[0]) needs to animate.
                if (ctx.playOrder[0] === "0") {
                    if (x === G.p1Position.x && y === G.p1Position.y) {
                        return G.p1DirectionOfLastMove
                    }
                } else if (ctx.playOrder[0] === "1") {
                    if (x === G.p2Position.x && y === G.p2Position.y) {
                        return G.p2DirectionOfLastMove
                    }
                } else {
                    return "down"
                }
            }
        }
        return "down";
    }

    const renderGrid = () => {
        let tileArray = [];
        for (let y = 2; y >= -2; y--) {
            const rowOfTiles = [];
            for (let x = -3; x <= 3; x++) {
                if (Math.abs(x) === 3 && y === 0) {
                    rowOfTiles.push(<Tile
                        direction={computeAnimationDirection(x, y)}
                        sprite={computeContentOfTile(x, y) || "egg"}
                        currentPlayer={getCurrentPlayer()}
                        ctx={ctx}
                        key={`${ctx.turn}-${x}-${y}`} />)
                } else if (Math.abs(y) === 1 && Math.abs(x) === 1) {
                    rowOfTiles.push(<div key={`${ctx.turn}-${x}-${y}`}></div>) // an empty div for gray tiles that are not part of the board
                } else if (Math.abs(x) === 3 && y !== 0) {
                    rowOfTiles.push(<div key={`${ctx.turn}-${x}-${y}`}></div>) // an empty div for gray tiles that are not part of the board
                } else {
                    rowOfTiles.push(<Tile
                        direction={computeAnimationDirection(x, y)}
                        sprite={computeContentOfTile(x, y)}
                        currentPlayer={getCurrentPlayer()}
                        ctx={ctx}
                        key={`${ctx.turn}-${x}-${y}`} />)
                }
            }
            tileArray.push(rowOfTiles)
        }
        return tileArray;
    }

    const getCurrentPlayer = (): string => {
        if (ctx.phase === "chickenPhase") {
            return "chicken"
        }
        if (ctx.phase === "playerPhase") {
            return ctx.currentPlayer
        }
        return ""
    }

    const currentTurnStyle = (player: string) => {
        return getCurrentPlayer() === player ? "turn-text turn-text--active" : "turn-text"
    }

    const getTurnOrderDisplay = () => {
        if (G.firstPlayer === "0") {
            return (
                <>
                    <h3 className={currentTurnStyle("0")}>PLAYER 1 TURN</h3>
                    <h3 className={currentTurnStyle("1")}>PLAYER 2 TURN</h3>
                </>
            )
        } else {
            return (
                <>
                    <h3 className={currentTurnStyle("1")}>PLAYER 2 TURN</h3>
                    <h3 className={currentTurnStyle("0")}>PLAYER 1 TURN</h3>
                </>
            )
        }

    }

    if (checkIfPlayerDisconnected() && !ctx.gameover) {
        return <h1>The other player has disconnected. Waiting for them to reconnect...</h1>
    }

    if (!checkIfAllPlayersAreConnected() && !ctx.gameover) {
        return <h1>Waiting for other player...</h1>
    }

    if (showRoundEndInfo) {
        return <RoundEndInfo endCondition={ctx.gameover.endCondition} p1Score={ctx.gameover.p1Score} p2Score={ctx.gameover.p2Score} />
    }
    return (
        <div>
            <div className="player-score-container">
                <h2>P1 Score: {G.p1Score}</h2>
                <h2>P2 Score: {G.p2Score}</h2>
            </div>

            <div className="turn-visualizer-container">
                <h3 className={currentTurnStyle("chicken")}>CHICKEN TURN</h3>
                {getTurnOrderDisplay()}
            </div>

            <div className="game-grid-container">
                <div className="game-grid">
                    {renderGrid()}
                </div>
            </div>
        </div>
    )
}

export default EgghuntBoard