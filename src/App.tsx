import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/Homepage/Homepage";
import EgghuntGamePage from "./pages/EgghuntGamePage/EgghuntGamePage";
import JoinEgghuntPage from "./pages/JoinEgghuntPage/JoinEgghuntPage";
import "./reset.css";
import "./App.css";
import GameEndPage from "./pages/GameEndPage/GameEndPage";
import { isMobile } from 'react-device-detect';

const App = () => {
    if (isMobile) {
        return <h1>Sorry, your device is not supported by this study. If you would like to participate, please use a desktop or laptop device with a keyboard.</h1>
    }
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<HomePage />} />
                {/* this path needs to be made dynamic if it's to support more tasks */}
                <Route path="/tasks/egghunt" element={<EgghuntGamePage />} />
                <Route path="/tasks/egghunt/join" element={<JoinEgghuntPage />} />
                <Route path="/tasks/egghunt/end" element={<GameEndPage />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App
