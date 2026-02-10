import { INVALID_MOVE } from "boardgame.io/core";
import type { Game } from "boardgame.io";

export interface Position {
    x: number;
    y: number;
}

export type Direction = "up" | "down" | "left" | "right" | "stay";

const getPlayerPositionKey = (playerID: string) => {
    switch (playerID) {
        case "0":
            return "p1Position"
        case "1":
            return "p2Position"
        default:
            return "chickenPosition"
    }
}

const getPlayerDirectionKey = (playerID: string) => {
    switch (playerID) {
        case "0":
            return "p1DirectionOfLastMove"
        case "1":
            return "p2DirectionOfLastMove"
        default:
            return "chickenDirectionOfLastMove"
    }
}

const getPlayerScoreKey = (playerID: string) => {
    switch (playerID) {
        case "0":
            return "p1Score"
        case "1":
            return "p2Score"
        default:
            // this should not be the default, but I put this here to fix typescript errors
            return "p2Score"
    }
}

// returns true if the position is not a valid location on the map
// valid locations include squares where there is an egg.
const isOutOfBounds = (position: Position): boolean => {
    const { x, y } = position;
    if (Math.abs(y) === 1 && Math.abs(x) === 1) {
        return true;
    }
    if (Math.abs(x) === 3 && y !== 0) {
        return true;
    }
    if (Math.abs(x) > 3 || Math.abs(y) > 2) {
        return true;
    }
    return false;
}

// returns true if the newPlayerPosition is a position a player can move to on the map and false otherwise
// this function is not related to moving in a specific direction.
const isValidPlayerMove = (newPlayerPosition: Position, G: GameState) => {
    const { x, y } = newPlayerPosition;
    //prevent players from moving to a space occupied by another player or the chicken
    if (x === G.p1Position.x && y === G.p1Position.y) {
        return false;
    }
    if (x === G.p2Position.x && y === G.p2Position.y) {
        return false;
    }
    if (x === G.chickenPosition.x && y === G.chickenPosition.y) {
        return false;
    }

    if (isOutOfBounds(newPlayerPosition)) {
        return false;
    }

    return true;
}

// returns true if x and y is a square the chicken can move to on the map and false otherwise
// this function is not related to moving in a specific direction.
const isValidChickenMove = (newChickenPosition: Position, G: GameState) => {
    //prevent chicken from moving onto an egg
    const { x, y } = newChickenPosition;
    if ([-3, 3].includes(x) && y === 0) {
        return false;
    }

    //prevent chicken from moving to a space occupied by a player
    if (x === G.p1Position.x && y === G.p1Position.y) {
        return false;
    }
    if (x === G.p2Position.x && y === G.p2Position.y) {
        return false;
    }

    if (isOutOfBounds(newChickenPosition)) {
        return false;
    }

    return true;
}

const computeChickenMove = (G: GameState): Position => {
    const possibleMoves = [
        [-1, 0],   // left
        [1, 0],    // right
        [0, -1],   // down
        [0, 1],    // up
        [0, 0]     // stay
    ];

    const validMoves: Position[] = [];
    //find a set of legal moves where the chicken will also not move next to a player
    for (const move of possibleMoves) {
        const newPos: Position = {
            x: G.chickenPosition.x + move[0],
            y: G.chickenPosition.y + move[1]
        };
        const chickenNextToP1 = isPlayerAdjacentToChicken(G.p1Position, newPos);
        const chickenNextToP2 = isPlayerAdjacentToChicken(G.p2Position, newPos);
        if (isValidChickenMove(newPos, G) && !(chickenNextToP1 || chickenNextToP2)) {
            validMoves.push(newPos);
        }
    }
    // if there are no ideal moves and the only moves are to remain in place or move next to a player, then also consider those.
    if (validMoves.length === 0) {
        // I don't do this right now, but agent0 can also stay in place if no valid moves available: return G.chickenPosition;
        // Instead, I just loop through possible moves again and check grid bounds and other agent positions
        for (const move of possibleMoves) {
            const newPos: Position = {
                x: G.chickenPosition.x + move[0],
                y: G.chickenPosition.y + move[1]
            };
            if (isValidChickenMove(newPos, G)) {
                validMoves.push(newPos);
            }
        }
    }

    // Calculate the Manhattan distance for each valid move
    const distances = validMoves.map(move => {
        const dist1 = Math.abs(move.x - G.p1Position.x) + Math.abs(move.y - G.p1Position.y);
        const dist2 = Math.abs(move.x - G.p2Position.x) + Math.abs(move.y - G.p2Position.y);
        return dist1 + dist2;
    });

    // Find the maximum distance
    const maxDistance = Math.max(...distances);

    // Get all the moves with the maximum distance
    const bestMoves = validMoves.filter((_, i) => distances[i] === maxDistance);

    // Select a random move from the best moves
    const randomIndex = Math.floor(Math.random() * bestMoves.length);
    return bestMoves[randomIndex];
}

/*
    this function is a hack to check if two objects are equal
    to make checking if two positions are the same easier 
*/
const checkForSimpleObjectEquality = (obj1: Object, obj2: Object) => {
    return JSON.stringify(obj1) === JSON.stringify(obj2)
}
const isPlayerAdjacentToChicken = (playerPosition: Position, chickenPosition: Position) => {
    const aboveChickenCoords = {
        x: chickenPosition.x,
        y: chickenPosition.y + 1
    }
    const belowChickenCoords = {
        x: chickenPosition.x,
        y: chickenPosition.y - 1
    }
    const leftOfChickenCoords = {
        x: chickenPosition.x - 1,
        y: chickenPosition.y
    }
    const rightOfChickenCoords = {
        x: chickenPosition.x + 1,
        y: chickenPosition.y
    }
    if (checkForSimpleObjectEquality(playerPosition, aboveChickenCoords)
        || checkForSimpleObjectEquality(playerPosition, belowChickenCoords)
        || checkForSimpleObjectEquality(playerPosition, leftOfChickenCoords)
        || checkForSimpleObjectEquality(playerPosition, rightOfChickenCoords)) {
        return true;
    }
}


type GameState = {
    p1Position: Position,
    p2Position: Position,
    chickenPosition: Position,
    p1DirectionOfLastMove: Direction,
    p2DirectionOfLastMove: Direction,
    chickenDirectionOfLastMove: Direction,
    p1Score: number,
    p2Score: number,
    trialsPlayed: number,
    turnsMade: number,
    firstPlayer: "0" | "1",
    trialLimit: number
};

type SetupData = {
    ntrials: number,
    firstplayer: 'player1' | 'player2',
    chick_startx: number,
    chick_starty: number,
    agent1_startx: number,
    agent1_starty: number,
    agent2_startx: number,
    agent2_starty: number
}

export const EgghuntGame: Game<GameState> = {
    name: "egghunt",
    minPlayers: 2,
    maxPlayers: 2,

    setup: ({ ctx, ...plugins }, setupData: SetupData) => {
        const bgioPlayerIDMap: { [key: string]: "0" | "1" } = {
            "player1": '0',
            "player2": '1',
        };
        return {
            p1Position: {
                "x": setupData.agent1_startx,
                "y": setupData.agent1_starty
            },
            p2Position: {
                "x": setupData.agent2_startx,
                "y": setupData.agent2_starty
            },
            chickenPosition: {
                "x": setupData.chick_startx,
                "y": setupData.chick_starty
            },
            p1DirectionOfLastMove: "down",
            p2DirectionOfLastMove: "down",
            chickenDirectionOfLastMove: "down",
            p1Score: 150,
            p2Score: 150,
            trialsPlayed: 0,
            turnsMade: 0,
            firstPlayer: bgioPlayerIDMap[setupData.firstplayer],
            trialLimit: setupData.ntrials
        }
    },

    moves: {
        moveUp: ({ G, playerID }) => {
            let newPlayerPosition = {
                x: G[getPlayerPositionKey(playerID)].x,
                y: G[getPlayerPositionKey(playerID)].y + 1
            }
            if (isValidPlayerMove(newPlayerPosition, G)) {
                G[getPlayerPositionKey(playerID)].y++;
                G[getPlayerDirectionKey(playerID)] = 'up';
                G[getPlayerScoreKey(playerID)] -= 10;
            } else {
                return INVALID_MOVE;
            }
        },
        moveDown: ({ G, playerID }) => {
            let newPlayerPosition = {
                x: G[getPlayerPositionKey(playerID)].x,
                y: G[getPlayerPositionKey(playerID)].y - 1
            }
            if (isValidPlayerMove(newPlayerPosition, G)) {
                G[getPlayerPositionKey(playerID)].y--;
                G[getPlayerDirectionKey(playerID)] = 'down';
                G[getPlayerScoreKey(playerID)] -= 10;
            } else {
                return INVALID_MOVE;
            }
        },
        moveLeft: ({ G, playerID }) => {
            let newPlayerPosition = {
                x: G[getPlayerPositionKey(playerID)].x - 1,
                y: G[getPlayerPositionKey(playerID)].y
            }
            if (isValidPlayerMove(newPlayerPosition, G)) {
                G[getPlayerPositionKey(playerID)].x--;
                G[getPlayerDirectionKey(playerID)] = 'left';
                G[getPlayerScoreKey(playerID)] -= 10;
            } else {
                return INVALID_MOVE;
            }
        },
        moveRight: ({ G, playerID }) => {
            let newPlayerPosition = {
                x: G[getPlayerPositionKey(playerID)].x + 1,
                y: G[getPlayerPositionKey(playerID)].y
            }
            if (isValidPlayerMove(newPlayerPosition, G)) {
                G[getPlayerPositionKey(playerID)].x++;
                G[getPlayerDirectionKey(playerID)] = 'right';
                G[getPlayerScoreKey(playerID)] -= 10;
            } else {
                return INVALID_MOVE;
            }
        },
        stayInPlace: ({ G, playerID, events }) => {
            G[getPlayerScoreKey(playerID)] -= 10;
            G[getPlayerDirectionKey(playerID)] = 'stay';
            events.endTurn();
        },
    },

    phases: {
        chickenPhase: {
            onBegin: ({ G, events }) => {
            },
            onEnd: ({ G }) => {
            },
            start: true,
            moves: {
                moveChicken: ({ G, events }) => {
                    const newChickenPosition = computeChickenMove(G);
                    // compute the direction that the chicken moved
                    if (newChickenPosition.x < G.chickenPosition.x) {
                        G.chickenDirectionOfLastMove = "left";
                    }
                    if (newChickenPosition.x > G.chickenPosition.x) {
                        G.chickenDirectionOfLastMove = "right";
                    }
                    if (newChickenPosition.y < G.chickenPosition.y) {
                        G.chickenDirectionOfLastMove = "down";
                    }
                    if (newChickenPosition.y > G.chickenPosition.y) {
                        G.chickenDirectionOfLastMove = "up";
                    }
                    if (newChickenPosition.x === G.chickenPosition.x && newChickenPosition.y === G.chickenPosition.y) {
                        G.chickenDirectionOfLastMove = "stay";
                    }
                    G.chickenPosition = newChickenPosition
                    events.endPhase();
                }
            },
            turn: {
                // the turn order definition for the chicken MUST be the same as the players
                order: {
                    first: () => 0,
                    next: ({ ctx }) => {
                        if (ctx.playOrderPos < ctx.playOrder.length - 1) {
                            return ctx.playOrderPos + 1;
                        }
                    },
                    playOrder: ({ G }) => {
                        if (G.firstPlayer === "0") {
                            return ["0", "1"]
                        } else {
                            return ["1", "0"]
                        }
                    }
                },
                minMoves: 1,
                maxMoves: 1,
            },
            next: "playerPhase"
        },
        playerPhase: {
            onBegin: () => {
            },
            onEnd: ({ G }) => {
                G.trialsPlayed++;
            },

            turn: {
                onMove: ({ G }) => {
                    G.turnsMade++;
                },
                //each player goes once (same as TurnOrder.ONCE), but the playOrder changes based on the setup data.
                order: {
                    first: () => 0,
                    next: ({ ctx }) => {
                        if (ctx.playOrderPos < ctx.playOrder.length - 1) {
                            return ctx.playOrderPos + 1;
                        }
                    },
                    playOrder: ({ G }) => {
                        if (G.firstPlayer === "0") {
                            return ["0", "1"]
                        } else {
                            return ["1", "0"]
                        }
                    }
                },
                minMoves: 1,
                maxMoves: 1,
            },
            start: false,
            next: "chickenPhase"
        }
    },

    endIf: ({ G, ctx }) => {
        // a game can only end if all players have made an equal number of turns
        if (G.turnsMade % ctx.numPlayers === 0) {
            const p1GetsEgg = [-3, 3].includes(G.p1Position.x) && G.p1Position.y === 0;
            const p2GetsEgg = [-3, 3].includes(G.p2Position.x) && G.p2Position.y === 0
            const p1NextToChicken = isPlayerAdjacentToChicken(G.p1Position, G.chickenPosition);
            const p2NextToChicken = isPlayerAdjacentToChicken(G.p2Position, G.chickenPosition);

            // if both players are next to the chicken, the game ends
            if (p1NextToChicken && p2NextToChicken) {
                return {
                    endCondition: "Both Players Capture the Chicken",
                    outcome: "cooperate",
                    p1Score: G.p1Score + 200,
                    p2Score: G.p2Score + 200
                }
            }

            // if either player gets an egg, the game ends
            if (p1GetsEgg && p2GetsEgg) {
                return {
                    endCondition: "Both Players Collect an Egg",
                    outcome: "both defect",
                    p1Score: G.p1Score + 100,
                    p2Score: G.p2Score + 100
                }
            } else if (p1GetsEgg) {
                return {
                    endCondition: "Player 1 Collects an Egg",
                    outcome: "agent 1 defect",
                    p1Score: G.p1Score + 100,
                    p2Score: G.p2Score
                }
            } else if (p2GetsEgg) {
                return {
                    endCondition: "Player 2 Collects an Egg",
                    outcome: "agent 2 defect",
                    p1Score: G.p1Score,
                    p2Score: G.p2Score + 100
                }
            }

            /*
            if the chicken has not been captured and neither player got an egg,
            and if the trial limit has been reached, then the game ends 
            */
            if (G.trialsPlayed === G.trialLimit) {
                return {
                    endCondition: "Turn Limit Reached",
                    outcome: "round expired",
                    p1Score: G.p1Score,
                    p2Score: G.p2Score
                }
            }
        }
    },

    // make sure the chicken cannot move to an egg
    // ai: {
    //     enumerate: (G, ctx) => {
    //         return;
    //     }
    // }
}
