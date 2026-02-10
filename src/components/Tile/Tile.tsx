import "./Tile.css"
import Egg from "../../assets/egg.png";
import ChickenDown from "../../assets/chicken_down.png";
import ChickenUp from "../../assets/chicken_up.png";
import ChickenLeft from "../../assets/chicken_left.png";
import ChickenRight from "../../assets/chicken_right.png";

import P1Down from "../../assets/p1_down.png";
import P1Up from "../../assets/p1_up.png";
import P1Left from "../../assets/p1_left.png";
import P1Right from "../../assets/p1_right.png";

import P2Down from "../../assets/p2_down.png";
import P2Up from "../../assets/p2_up.png";
import P2Left from "../../assets/p2_left.png";
import P2Right from "../../assets/p2_right.png";
import { useState, useEffect } from "react";
import { Direction } from "../../game-logic/EgghuntGame";

const Tile = ({ sprite, direction, currentPlayer, ctx, inPlayerAssignmentPage }: { sprite: "p1" | "p2" | "chicken" | "egg" | undefined; direction: Direction; currentPlayer: string | null; ctx: any; inPlayerAssignmentPage?: boolean }) => {
    const p1SpriteDirectionMap = {
        "up": P1Up,
        "down": P1Down,
        "left": P1Left,
        "right": P1Right,
        "stay": P1Down,
    }
    const p2SpriteDirectionMap = {
        "up": P2Up,
        "down": P2Down,
        "left": P2Left,
        "right": P2Right,
        "stay": P2Down,
    }
    const chickenSpriteDirectionMap = {
        "up": ChickenUp,
        "down": ChickenDown,
        "left": ChickenLeft,
        "right": ChickenRight,
        "stay": ChickenDown,
    }

    const [currentImage, setCurrentImage] = useState(getDirectionalSprite());

    useEffect(() => {
        const timer = setTimeout(() => {
            setCurrentImage(getDownSprite());
        }, 1000);

        return () => clearTimeout(timer);
    }, []);

    function getDirectionalSprite() {
        switch (sprite) {
            case "p1":
                return p1SpriteDirectionMap[direction]
            case "p2":
                return p2SpriteDirectionMap[direction]
            case "chicken":
                return chickenSpriteDirectionMap[direction]
            case "egg":
                return Egg
        }
    }
    function getDownSprite() {
        switch (sprite) {
            case "p1":
                return P1Down
            case "p2":
                return P2Down
            case "chicken":
                return ChickenDown
            case "egg":
                return Egg
        }
    }
    const getSpriteClassName = () => {
        switch (sprite) {
            case "p1":
                return "p1-sprite"
            case "p2":
                return "p2-sprite"
            case "chicken":
                return "chicken-sprite"
            case "egg":
                return "egg-sprite"
        }
    }

    const getSpriteLabel = () => {
        switch (sprite) {
            case "p1":
                return "PLAYER 1"
            case "p2":
                return "PLAYER 2"
            default:
                return "";
        }
    }

    const getSpriteTextClassName = () => {
        if (currentPlayer === "0" && sprite === "p1") {
            return "sprite-text sprite-text--active"
        }
        if (currentPlayer === "1" && sprite === "p2") {
            return "sprite-text sprite-text--active"
        }
        return "sprite-text"
    }
    if (!sprite) {
        return <div className="game-tile"></div>
    }
    if (inPlayerAssignmentPage) {
        return (
            <div className="game-tile game-tile--large">
                <div className="sprite-container">
                    <img src={getDownSprite()} className={getSpriteClassName()} />
                </div>
                <div className={"sprite-text"}>{getSpriteLabel()}</div>
            </div>
        )
    }
    if (ctx?.gameover) {
        // this is a little hacky to just render the down sprite on the last move that would
        // result in the game being over. This causes the last move to not animate, which is a minor bug.
        return (
            <div className="game-tile">
                <div className="sprite-container">
                    <img src={getDownSprite()} className={getSpriteClassName()} />
                </div>
                <div className={getSpriteTextClassName()}>{getSpriteLabel()}</div>
            </div>
        )
    }
    return (
        <div className="game-tile">
            <div className="sprite-container">
                <img src={currentImage} className={getSpriteClassName()} />
            </div>
            <div className={getSpriteTextClassName()}>{getSpriteLabel()}</div>
        </div>
    )
}

export default Tile