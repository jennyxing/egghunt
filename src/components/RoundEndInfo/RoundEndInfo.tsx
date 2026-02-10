import { useContext } from "react"
import "./RoundEndInfo.css";
import axios from "axios";
import { LobbyContext, serverURL } from "../../context/LobbyContext";
import { useNavigate, useSearchParams } from "react-router-dom";

const RoundEndInfo = (props: { endCondition: string; p1Score: number; p2Score: number }) => {
    const navigate = useNavigate();
    const lobbyClient = useContext(LobbyContext);
    const [searchParams] = useSearchParams();

    const goToNextRound = async () => {
        const resp = await axios.get(`${serverURL}/tasks/egghunt/round_setup?currentBGIOMatchID=${searchParams.get("matchID")}`)
        if (resp.data.message === "game finished") {
            navigate("/tasks/egghunt/end")
            return;
        }
        const { nextMatchID } = await lobbyClient.playAgain('egghunt', searchParams.get("matchID") || '', {
            playerID: localStorage.getItem("egghuntPlayerID") || '',
            credentials: localStorage.getItem("egghuntPlayerCredentials") || '',
            setupData: resp.data.setupData
        });
        await axios.patch(
            `${serverURL}/tasks/egghunt/matches?game_id=${resp.data.game_id}&round_index=${resp.data.round_index}`,
            {
                bgio_match_id: nextMatchID
            })

        const { playerID, playerCredentials } = await lobbyClient.joinMatch(
            'egghunt',
            nextMatchID,
            {
                playerName: localStorage.getItem("studyID") || "unknown player",
                playerID: localStorage.getItem("egghuntPlayerID") || undefined,
                data: {
                    studyID: localStorage.getItem("studyID")
                }
            },
        );

        localStorage.setItem("matchID", nextMatchID);
        localStorage.setItem("egghuntPlayerCredentials", playerCredentials);

        navigate(`/tasks/egghunt?playerID=${playerID}&matchID=${nextMatchID}`, { replace: true })
    }

    return (
        <>
            <h1>Round Completed</h1>
            <h2>{props.endCondition}</h2>
            <h3>Player 1: {props.p1Score >= 0 ? "+" : "−"}{Math.abs(props.p1Score)}</h3>
            <h3>Player 2: {props.p2Score >= 0 ? "+" : "−"}{Math.abs(props.p2Score)}</h3>

            <button className="next-button" onClick={goToNextRound}>Continue</button>
        </>
    )
}

export default RoundEndInfo