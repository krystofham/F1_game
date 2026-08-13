import { useState } from "react";
import { BrowserRouter, HashRouter, Routes, Route, NavLink } from "react-router-dom";
import TeamsPage from "./pages/TeamsPage";
import DriversPage from "./pages/DriversPage";
import RacePage from "./pages/RacePage";
import TrackPage from "./pages/TrackPage";
import StandingsPage from "./pages/StandingsPage";
import GraphsPage from "./pages/GraphsPage";
import TeamPage from "./pages/TeamPage";
import TransferMarket from "./pages/TransfersPage";
import SettingsPage from "./pages/SettingsPage";
import StatsPage from "./pages/StatsPage";
import { useApi } from "./hooks/useApi";
import { api } from "./utils/api";
import EngineGate from "./components/EngineGate";
import WelcomeModal from "./components/WelcomeModal";
import "./styles.css";

// Packaged Electron build is loaded via mainWindow.loadFile(), i.e. the
// `file://` protocol. Under file://, window.location.pathname is the actual
// filesystem path to index.html (e.g. "/C:/.../dist/index.html"), not "/" —
// so BrowserRouter never matches any route and the app gets stuck with a
// blank content area (only the layout/sidebar renders, nothing navigates).
// HashRouter keeps routing state after a "#" and doesn't depend on the real
// path at all, so it works correctly under file://. In the browser / Vite
// dev server (real http(s) origin) we keep BrowserRouter as before.
const Router =
  typeof window !== "undefined" && window.location.protocol === "file:"
    ? HashRouter
    : BrowserRouter;

const NAV_ITEMS = [
  { to: "/", label: "STANDINGS", icon: "" },
  { to: "/race", label: "RACE CONTROL", icon: "" },
  { to: "/teams", label: "TEAMS", icon: "" },
  { to: "/drivers", label: "DRIVERS", icon: "" },
  { to: "/track", label: "TRACK", icon: "" },
  { to: "/graphs", label: "TELEMETRY", icon: "" },
  { to: "/stats", label: "STATS", icon: "" },
  { to: "/transfer", label: "TRANSFERS", icon: "" },
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

      <div style={{ marginTop: "auto", paddingTop: 12, borderTop: "1px solid var(--border)" }}>
        <NavLink
          to="/settings"
          className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
        >
          <span className="nav-icon">⚙</span>
          <span className="nav-label">SETTINGS</span>
          <span className="nav-indicator" />
        </NavLink>
      </div>
    </nav>
  );
}

function AppShell() {
  const { data: state, loading, refetch } = useApi(api.getState);
  const [welcomeDismissed, setWelcomeDismissed] = useState(false);

  return (
    <div className="app-shell">
      <Sidebar />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<StandingsPage />} />
          <Route path="/race" element={<RacePage onSeasonChange={refetch} />} />
          <Route path="/teams" element={<TeamsPage />} />
          <Route path="/drivers" element={<DriversPage />} />
          <Route path="/track" element={<TrackPage state={state} />} />
          <Route path="/graphs" element={<GraphsPage />} />
          <Route path="/team/:teamId" element={<TeamPage />} />
          <Route path="/transfer" element={<TransferMarket />} />
          <Route path="/stats" element={<StatsPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </main>
      <WelcomeModal
        state={state}
        loading={loading}
        dismissed={welcomeDismissed}
        onDismiss={() => setWelcomeDismissed(true)}
      />
    </div>
  );
}

export default function App() {
  return (
    <EngineGate>
      <BrowserRouter>
        <Routes>
          <Route path="/*" element={<AppShell />} />
        </Routes>
      </BrowserRouter>
    </EngineGate>
  );
}
