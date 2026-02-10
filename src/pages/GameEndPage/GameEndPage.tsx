import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const GameEndPage = () => {
    const navigate = useNavigate();
    useEffect(() => {
        if (!localStorage.getItem("p1TotalScore") || !localStorage.getItem("p2TotalScore")) {
            navigate("/tasks/egghunt")
        }
    }, [])

    return (
        <>
            <h1>Thanks for playing!</h1>
            <h2>Player 1 earned {localStorage.getItem("p1TotalScore")} points.</h2>
            <h2>Player 2 earned {localStorage.getItem("p2TotalScore")} points.</h2>

            <a onClick={() => { localStorage.clear() }} href={`https://redcap.mountsinai.org/INSERT_STUDY_ID/pid=${localStorage.getItem("studyID")}`} > Return to Study</a >
        </>
    )
}

export default GameEndPage;