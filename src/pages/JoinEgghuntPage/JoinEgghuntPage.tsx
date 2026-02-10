import { useContext, useState, useEffect } from "react";
import { useNavigate, Link, useSearchParams } from "react-router-dom"
import { LobbyContext, serverURL } from "../../context/LobbyContext";
import axios from 'axios';
import "./JoinEgghuntPage.css";

const JoinEgghuntPage = () => {
    const navigate = useNavigate();
    const lobbyClient = useContext(LobbyContext);
    const [waitingForMatch, setWaitingForMatch] = useState(false);
    const [error, setError] = useState(false);
    //write type for searchParams to be an object with 1 optional key of pid
    const [searchParams] = useSearchParams();

    // the unload event handles cases where the user has entered the queue
    // and clicks the back button, refreshes, or closes the browser/tab.
    useEffect(() => {
        const handleUnload = async (event: {
            returnValue: string; preventDefault: () => void;
        }) => {
            event.preventDefault();
            // if the user is already in a game, do not do anything.
            if (localStorage.getItem("matchID") && localStorage.getItem("egghuntPlayerCredentials") && localStorage.getItem("egghuntPlayerID")) {
                return;
            }
            const playerQueueInfo = {
                studyID: localStorage.getItem("studyID")
            }
            axios.patch(`${serverURL}/tasks/egghunt/leave-queue`, playerQueueInfo).then(() => {
                localStorage.clear();
            });
            return (event.returnValue = '');
        };

        window.addEventListener('beforeunload', handleUnload);

        return () => {
            window.removeEventListener('beforeunload', handleUnload);
        };
    }, []);

    const joinMatch = async () => {
        const { playerID, playerCredentials } = await lobbyClient.joinMatch(
            'egghunt',
            localStorage.getItem("matchID") || '',
            {
                playerName: localStorage.getItem("studyID") || "unknown player",
                data: {
                    studyID: localStorage.getItem("studyID")
                }
            },
        );

        localStorage.setItem("egghuntPlayerCredentials", playerCredentials);
        localStorage.setItem("egghuntPlayerID", playerID);

        return { playerID };
    }

    const handleJoinQueue = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setWaitingForMatch(true);
        setError(false);
        const playerInfoForQueue = {
            studyID: e.currentTarget.studyID.value
        }
        try {
            localStorage.setItem("studyID", e.currentTarget.studyID.value);
            const res = await axios.post(`${serverURL}/tasks/egghunt/join-queue`, playerInfoForQueue);
            localStorage.setItem("matchID", res.data.matchID);

            const { playerID } = await joinMatch()
            navigate(`/tasks/egghunt?playerID=${playerID}&matchID=${localStorage.getItem("matchID")}`)
        } catch (e) {
            console.error("Error Joining Queue: ", e)
            axios.patch(`${serverURL}/tasks/egghunt/leave-queue`, playerInfoForQueue).then(() => {
                localStorage.clear();
                setError(true);
                setWaitingForMatch(false);
            }).catch(e => {
                console.error("Server Error Leaving Queue: ", e)
                localStorage.clear();
                setError(true);
                setWaitingForMatch(false);
            });

        }

    }

    if (localStorage.getItem("matchID") && localStorage.getItem("egghuntPlayerCredentials") && localStorage.getItem("egghuntPlayerID")) {
        return (
            <div>
                <h2>Existing game found.</h2>
                <Link to={`/tasks/egghunt?playerID=${localStorage.getItem("egghuntPlayerID")}&matchID=${localStorage.getItem("matchID")}`}>Return to Existing Game</Link>
            </div>
        )
    }

    //if the user is already in the queue but has not yet been put into a match
    if ((localStorage.getItem("studyID") !== null && localStorage.getItem("matchID") === null) || waitingForMatch) {
        return <h1>Matchmaking in progress...</h1>
    }

    return (
        <>
            <h1 className="join-text">Join Game</h1>
            <form onSubmit={handleJoinQueue} className="study-id-form">
                {!searchParams.get("pid") &&
                    <label className="input-label">
                        Study ID:
                    </label>
                }
                <input type="text" name="studyID" className="study-id-input" defaultValue={searchParams.get('pid') || ""} disabled={searchParams.get('pid') ? true : false} required hidden={searchParams.get('pid') ? true : false} />
                <button className="join-button">Start</button>
                {error && <h3>There was an error. Please try again later. </h3>}
            </form>
        </>
    )
}

export default JoinEgghuntPage