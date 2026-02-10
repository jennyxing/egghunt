import { Client } from "boardgame.io/react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { SocketIO } from "boardgame.io/multiplayer";
import { EgghuntGame } from "../../game-logic/EgghuntGame";
import EgghuntBoard from "../../components/EgghuntBoard/EgghuntBoard";
import { useEffect, useState } from "react";
import { serverURL } from "../../context/LobbyContext";
import "./EgghuntGamePage.css";
import Tile from "../../components/Tile/Tile";

const EgghuntGamePage = () => {
    const [searchParams] = useSearchParams();
    const [showPlayerAssignment, setShowPlayerAssignment] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        setTimeout(() => {
            setShowPlayerAssignment(false);
        }, 3000);
    }, [])

    useEffect(() => {
        if (localStorage.getItem("egghuntPlayerCredentials") === null) {
            navigate("/tasks/egghunt/join");
        }
        if (!searchParams.get("playerID") || !searchParams.get("matchID")) {
            navigate("/tasks/egghunt/join");
        }
    }, [])

    const EgghuntOnlineClient = Client({
        game: EgghuntGame,
        numPlayers: 2,
        debug: false,
        board: EgghuntBoard,
        multiplayer: SocketIO({ server: serverURL })
    });

    if (showPlayerAssignment) {
        return (
            <div className="player-assignment-container">
                <h1 className="player-assignment-text">You are Player {Number(localStorage.getItem("egghuntPlayerID")) + 1}</h1>
                <Tile direction={"down"}
                    sprite={localStorage.getItem("egghuntPlayerID") === "0" ? "p1" : "p2"}
                    currentPlayer={null}
                    ctx={null}
                    inPlayerAssignmentPage={true} />
            </div>
        )
    }

    return (<EgghuntOnlineClient
        playerID={searchParams.get("playerID") || undefined}
        matchID={searchParams.get("matchID") || undefined}
        credentials={localStorage.getItem("egghuntPlayerCredentials") || undefined} />)
}

export default EgghuntGamePage;