import { BrowserRouter, Routes, Route, NavLink, useLocation } from "react-router-dom";
import TeamsPage from "./pages/TeamsPage";
import DriversPage from "./pages/DriversPage";
import RacePage from "./pages/RacePage";
import TrackPage from "./pages/TrackPage";
import StandingsPage from "./pages/StandingsPage";
import GraphsPage from "./pages/GraphsPage";
import "./styles.css";

const NAV_ITEMS = [
  { to: "/", label: "STANDINGS", icon: "▲" },
  { to: "/race", label: "RACE CONTROL", icon: "◉" },
  { to: "/teams", label: "TEAMS", icon: "◈" },
  { to: "/drivers", label: "DRIVERS", icon: "◆" },
  { to: "/track", label: "TRACK", icon: "◎" },
  { to: "/graphs", label: "TELEMETRY", icon: "∿" },
];

function Sidebar() {
  return (
    <nav className="sidebar">
      <div className="sidebar-header">
        <div className="logo-mark">F1</div>
        <div className="logo-text">
          <span className="logo-title">APEX</span>
          <span className="logo-sub">MANAGER</span>
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
      <div className="sidebar-footer">
        <div className="api-status">
          <span className="status-dot" />
          ENGINE LIVE
        </div>
      </div>
    </nav>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<StandingsPage />} />
            <Route path="/race" element={<RacePage />} />
            <Route path="/teams" element={<TeamsPage />} />
            <Route path="/drivers" element={<DriversPage />} />
            <Route path="/track" element={<TrackPage />} />
            <Route path="/graphs" element={<GraphsPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
