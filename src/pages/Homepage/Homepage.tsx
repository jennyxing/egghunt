import { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import { LobbyContext } from "../../context/LobbyContext";
import "./Homepage.css";

const HomePage = () => {
    const lobbyClient = useContext(LobbyContext);

    const [tasks, setTasks]: [string[], any] = useState([])
    useEffect(() => {
        const getGames = async () => {
            const games = await lobbyClient.listGames();
            setTasks(games);
        }
        getGames();
    }, [])

    return (
        <>
            <h1>Choose a Task</h1>
            {tasks.map((task, i) => {
                return (<Link key={i} to={`/tasks/${task}`}><button>{task}</button></Link>)
            })}
        </>
    )
}

export default HomePage;