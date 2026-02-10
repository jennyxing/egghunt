import { createContext } from 'react';
import { LobbyClient } from "boardgame.io/client";

let { protocol, hostname, port } = window.location;
if (import.meta.env.VITE_SERVER_PORT) {
    port = import.meta.env.VITE_SERVER_PORT
}
export const serverURL = `${protocol}//${hostname}:${port}`;

const lobbyClient = new LobbyClient({ server: serverURL });

export const LobbyContext = createContext(lobbyClient);