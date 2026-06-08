import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import TeamsPage from "./pages/TeamsPage";
import DriversPage from "./pages/DriversPage";
import RacePage from "./pages/RacePage";
import TrackPage from "./pages/TrackPage";
import StandingsPage from "./pages/StandingsPage";
import GraphsPage from "./pages/GraphsPage";
import TeamPage from "./pages/TeamPage";
import TransferMarket from "./pages/TransfersPage";
import { useApi } from "./hooks/useApi";
import { api } from "./utils/api"; 
import "./styles.css";

const NAV_ITEMS = [
  { to: "/", label: "STANDINGS", icon: "▲" },
  { to: "/race", label: "RACE CONTROL", icon: "◉" },
  { to: "/teams", label: "TEAMS", icon: "◈" },
  { to: "/drivers", label: "DRIVERS", icon: "◆" },
  { to: "/track", label: "TRACK", icon: "◎" },
  { to: "/graphs", label: "TELEMETRY", icon: "∿" },
  { to: "/transfer", label: "TRANSFERS", icon: "⇄" },
];

function Sidebar() {
  return (
    <nav className="sidebar">
      <div className="sidebar-header">
        <div className="logo-text">
          <span className="logo-title">MMRAC1NG</span>
        </div>
      </div>
      <div className="nav-items">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === "/"}
            className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
            <span className="nav-indicator" />
          </NavLink>
        ))}
      </div>
    </nav>
  );
}
export default function App() {
  const { data: state } = useApi(api.getState);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/*" element={
          <div className="app-shell">
            <Sidebar />
            <main className="main-content">
              <Routes>
                <Route path="/" element={<StandingsPage />} />
                <Route path="/race" element={<RacePage />} />
                <Route path="/teams" element={<TeamsPage />} />
                <Route path="/drivers" element={<DriversPage />} />
                <Route path="/track" element={<TrackPage state={state }/>} />
                <Route path="/graphs" element={<GraphsPage />} />
                <Route path="/team/:teamId" element={<TeamPage />} />
                <Route path="/transfer" element={<TransferMarket />} />
              </Routes>
            </main>
          </div>
        } />
      </Routes>
    </BrowserRouter>
  );
}