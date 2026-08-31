import List from "./pages/List.js";
import Leaderboard from "./pages/Leaderboard.js";

export default [
    { path: "/", component: List },
    {
        path: "/challenges-list",
        component: List,
        props: { listType: "challenges" },
    },
    {
        path: "/extremes-list",
        component: List,
        props: { listType: "extremes" },
    },
    { path: "/leaderboard", component: Leaderboard },
    { path: "/roulette", component: Roulette },
];
