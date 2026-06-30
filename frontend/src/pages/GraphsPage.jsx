import { useMemo, useState } from "react";
import { useApi } from "../hooks/useApi";
import { api } from "../utils/api";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  Legend, ResponsiveContainer, BarChart, Bar, Cell,
} from "recharts";

const COLORS = [
  "#e8002d", "#448aff", "#00e676", "#ffd600", "#ff6b35",
  "#aa00ff", "#00b0ff", "#76ff03", "#ff4081", "#18ffff",
  "#ffab40", "#ea80fc", "#b9f6ca", "#80d8ff", "#ccff90",
  "#ff9e80", "#e040fb", "#40c4ff", "#69f0ae", "#ffff00",
];

const PLAYER_COLOR = "#fb8500";

const CustomTooltip = ({ active, payload, label, suffix = "" }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: "var(--bg-card)", border: "1px solid var(--border)", padding: "10px 14px" }}>
      <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-3)", marginBottom: 6 }}>
        LAP {label}
      </div>
      {payload
        .filter((p) => p.value != null)
        .sort((a, b) => (a.value ?? 99) - (b.value ?? 99))
        .map((p, i) => (
          <div key={i} style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: p.color, marginBottom: 2 }}>
            {p.name}: {typeof p.value === "number" ? `${p.value.toFixed(3)}${suffix}` : p.value}
          </div>
        ))}
    </div>
  );
};

function filterDrivers(drivers, mode) {
  if (mode === "players") return drivers.filter((d) => d.is_player);
  if (mode === "top10") {
    return [...drivers]
      .sort((a, b) => (a.best_position ?? 99) - (b.best_position ?? 99))
      .slice(0, 10);
  }
  return drivers;
}

function SummaryCards({ drivers, teams, state }) {
  const leader = [...drivers].sort((a, b) => (b.points || 0) - (a.points || 0))[0];
  const teamLeader = [...(teams || [])].sort((a, b) => (b.points || 0) - (a.points || 0))[0];
  const maxLaps = Math.max(...drivers.map((d) => (d.position_history || []).length), 0);
  const players = drivers.filter((d) => d.is_player);

  return (
    <div className="stats-grid mb-6">
      <div className="stat-card">
        <div className="stat-card-label">Championship Leader</div>
        <div className="stat-card-value">{leader?.name?.split(" ").pop() ?? "—"}</div>
        <div className="stat-card-sub">{leader?.points ?? 0} pts</div>
      </div>
      <div className="stat-card">
        <div className="stat-card-label">Top Constructor</div>
        <div className="stat-card-value">{teamLeader?.name ?? "—"}</div>
        <div className="stat-card-sub">{teamLeader?.points ?? 0} pts</div>
      </div>
      <div className="stat-card">
        <div className="stat-card-label">Race Progress</div>
        <div className="stat-card-value">{maxLaps || "—"}</div>
        <div className="stat-card-sub">
          {state?.race_state?.total_laps
            ? `of ${state.race_state.total_laps} laps`
            : "laps completed"}
        </div>
      </div>
      <div className="stat-card">
        <div className="stat-card-label">Your Drivers</div>
        <div className="stat-card-value">{players.length || "—"}</div>
        <div className="stat-card-sub">
          {players.map((p) => `${p.name.split(" ").pop()} P${p.position ?? "?"}`).join(" · ") || "—"}
        </div>
      </div>
    </div>
  );
}

function PositionChart({ drivers, driverCount }) {
  if (!drivers?.length) return <div className="empty">No position data yet</div>;

  const maxLaps = Math.max(...drivers.map((d) => (d.position_history || []).length));
  if (!maxLaps) return <div className="empty">No position history yet</div>;

  const yMax = Math.max(driverCount || drivers.length, 10);

  const data = Array.from({ length: maxLaps }, (_, i) => {
    const row = { lap: i + 1 };
    drivers.forEach((d) => {
      const hist = d.position_history || [];
      if (hist[i] != null) row[d.name] = hist[i];
    });
    return row;
  });

  return (
    <ResponsiveContainer width="100%" height={340}>
      <LineChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
        <XAxis dataKey="lap" stroke="var(--text-3)" tick={{ fontSize: 10, fontFamily: "var(--font-mono)" }} />
        <YAxis
          stroke="var(--text-3)"
          tick={{ fontSize: 10, fontFamily: "var(--font-mono)" }}
          reversed
          domain={[1, yMax]}
          allowDecimals={false}
        />
        <Tooltip content={<CustomTooltip />} />
        <Legend wrapperStyle={{ fontFamily: "var(--font-mono)", fontSize: 10 }} />
        {drivers.map((d, i) => (
          <Line
            key={d.name}
            type="stepAfter"
            dataKey={d.name}
            stroke={d.is_player ? PLAYER_COLOR : COLORS[i % COLORS.length]}
            dot={false}
            strokeWidth={d.is_player ? 2.5 : 1}
            strokeOpacity={d.is_player ? 1 : 0.75}
            connectNulls
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}

function LapTimeChart({ drivers }) {
  const withTimes = drivers.filter((d) => (d.lap_times || []).length > 0);
  if (!withTimes.length) return <div className="empty">No lap time data yet — simulate a race first</div>;

  const maxLaps = Math.max(...withTimes.map((d) => d.lap_times.length));
  const data = Array.from({ length: maxLaps }, (_, i) => {
    const row = { lap: i + 1 };
    withTimes.forEach((d) => {
      if (d.lap_times[i] != null) row[d.name] = d.lap_times[i];
    });
    return row;
  });

  return (
    <ResponsiveContainer width="100%" height={340}>
      <LineChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
        <XAxis dataKey="lap" stroke="var(--text-3)" tick={{ fontSize: 10, fontFamily: "var(--font-mono)" }} />
        <YAxis
          stroke="var(--text-3)"
          tick={{ fontSize: 10, fontFamily: "var(--font-mono)" }}
          domain={["auto", "auto"]}
          reversed
        />
        <Tooltip content={<CustomTooltip suffix="s" />} />
        <Legend wrapperStyle={{ fontFamily: "var(--font-mono)", fontSize: 10 }} />
        {withTimes.map((d, i) => (
          <Line
            key={d.name}
            type="monotone"
            dataKey={d.name}
            stroke={d.is_player ? PLAYER_COLOR : COLORS[i % COLORS.length]}
            dot={false}
            strokeWidth={d.is_player ? 2.5 : 1}
            connectNulls
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}

function DriverPointsChart({ drivers }) {
  if (!drivers?.length) return <div className="empty">No points data</div>;
  const sorted = [...drivers].sort((a, b) => (b.points || 0) - (a.points || 0)).slice(0, 15);
  const data = sorted.map((d) => ({
    name: d.name.split(" ").pop(),
    fullName: d.name,
    pts: d.points || 0,
    is_player: d.is_player,
  }));

  return (
    <ResponsiveContainer width="100%" height={Math.max(260, data.length * 28)}>
      <BarChart data={data} layout="vertical" margin={{ top: 5, right: 20, left: 60, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" horizontal={false} />
        <XAxis type="number" stroke="var(--text-3)" tick={{ fontSize: 10, fontFamily: "var(--font-mono)" }} />
        <YAxis dataKey="name" type="category" stroke="var(--text-3)" tick={{ fontSize: 10, fontFamily: "var(--font-mono)" }} width={55} />
        <Tooltip
          content={({ active, payload }) => {
            if (!active || !payload?.length) return null;
            const row = payload[0].payload;
            return (
              <div style={{ background: "var(--bg-card)", border: "1px solid var(--border)", padding: "10px 14px" }}>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: 11 }}>{row.fullName}</div>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--accent)" }}>{row.pts} pts</div>
              </div>
            );
          }}
        />
        <Bar dataKey="pts" radius={[0, 4, 4, 0]}>
          {data.map((entry, i) => (
            <Cell key={i} fill={entry.is_player ? PLAYER_COLOR : "var(--accent)"} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}

function TeamPointsChart({ teams }) {
  if (!teams?.length) return <div className="empty">No constructor data</div>;
  const sorted = [...teams].sort((a, b) => (b.points || 0) - (a.points || 0));
  const data = sorted.map((t) => ({ name: t.name, pts: t.points || 0 }));

  return (
    <ResponsiveContainer width="100%" height={Math.max(220, data.length * 32)}>
      <BarChart data={data} layout="vertical" margin={{ top: 5, right: 20, left: 90, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" horizontal={false} />
        <XAxis type="number" stroke="var(--text-3)" tick={{ fontSize: 10, fontFamily: "var(--font-mono)" }} />
        <YAxis dataKey="name" type="category" stroke="var(--text-3)" tick={{ fontSize: 9, fontFamily: "var(--font-mono)" }} width={85} />
        <Tooltip content={<CustomTooltip suffix=" pts" />} />
        <Bar dataKey="pts" fill="var(--accent-2)" radius={[0, 4, 4, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}

const TABS = ["POSITIONS", "LAP TIMES", "DRIVERS", "CONSTRUCTORS"];
const FILTERS = [
  { id: "top10", label: "Top 10" },
  { id: "players", label: "Players" },
  { id: "all", label: "All" },
];

export default function GraphsPage() {
  const [tab, setTab] = useState(0);
  const [filter, setFilter] = useState("top10");
  const { data: state, loading, error } = useApi(api.getState);

  const drivers = state?.drivers || [];
  const teams = state?.teams || [];
  const driverCount = drivers.length;

  const filteredDrivers = useMemo(
    () => filterDrivers(drivers, filter),
    [drivers, filter]
  );

  if (loading) return <div className="loading">LOADING TELEMETRY</div>;
  if (error) return <div className="empty">⚠ {error}</div>;

  return (
    <div>
      <div className="page-header">
        <div className="page-eyebrow">Data Analysis</div>
        <div className="page-title">
          TELE<span>METRY</span>
        </div>
      </div>

      <SummaryCards drivers={drivers} teams={teams} state={state} />

      <div className="chart-controls">
        <div className="tab-row">
          {TABS.map((t, i) => (
            <button
              key={t}
              type="button"
              className={`tab-btn${i === tab ? " active" : ""}`}
              onClick={() => setTab(i)}
            >
              {t}
            </button>
          ))}
        </div>
        {(tab === 0 || tab === 1) && (
          <div className="filter-row">
            {FILTERS.map((f) => (
              <button
                key={f.id}
                type="button"
                className={`filter-btn${filter === f.id ? " active" : ""}`}
                onClick={() => setFilter(f.id)}
              >
                {f.label}
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="chart-wrap">
        {tab === 0 && (
          <>
            <div className="chart-title">Position History</div>
            <PositionChart drivers={filteredDrivers} driverCount={driverCount} />
          </>
        )}
        {tab === 1 && (
          <>
            <div className="chart-title">Lap Times (seconds, lower = faster)</div>
            <LapTimeChart drivers={filteredDrivers} />
          </>
        )}
        {tab === 2 && (
          <>
            <div className="chart-title">Driver Championship Points</div>
            <DriverPointsChart drivers={drivers} />
          </>
        )}
        {tab === 3 && (
          <>
            <div className="chart-title">Constructor Championship Points</div>
            <TeamPointsChart teams={teams} />
          </>
        )}
      </div>
    </div>
  );
}
