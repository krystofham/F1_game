import { useState } from "react";
import { useApi } from "../hooks/useApi";
import { api } from "../utils/api";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  Legend, ResponsiveContainer, BarChart, Bar,
} from "recharts";

const COLORS = [
  "#e8002d", "#448aff", "#00e676", "#ffd600", "#ff6b35",
  "#aa00ff", "#00b0ff", "#76ff03", "#ff4081", "#18ffff",
  "#ffab40", "#ea80fc", "#b9f6ca", "#80d8ff", "#ccff90",
  "#ff9e80", "#e040fb", "#40c4ff", "#69f0ae", "#ffff00",
];

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: "var(--bg-card)", border: "1px solid var(--border)", padding: "10px 14px" }}>
      <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-3)", marginBottom: 6 }}>
        LAP {label}
      </div>
      {payload.map((p, i) => (
        <div key={i} style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: p.color, marginBottom: 2 }}>
          {p.name}: {typeof p.value === "number" ? p.value.toFixed(3) : p.value}
        </div>
      ))}
    </div>
  );
};

function PositionChart({ drivers }) {
  if (!drivers?.length) return <div className="empty">No position data yet</div>;

  const maxLaps = Math.max(...drivers.map((d) => (d.position_history || []).length));
  if (!maxLaps) return <div className="empty">No position history yet</div>;

  const data = Array.from({ length: maxLaps }, (_, i) => {
    const row = { lap: i + 1 };
    drivers.forEach((d) => {
      const hist = d.position_history || [];
      if (hist[i] != null) row[d.name] = hist[i];
    });
    return row;
  });

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
        <XAxis dataKey="lap" stroke="var(--text-3)" tick={{ fontSize: 10, fontFamily: "var(--font-mono)" }} />
        <YAxis stroke="var(--text-3)" tick={{ fontSize: 10, fontFamily: "var(--font-mono)" }} reversed domain={[1, 20]} />
        <Tooltip content={<CustomTooltip />} />
        <Legend wrapperStyle={{ fontFamily: "var(--font-mono)", fontSize: 10 }} />
        {drivers.map((d, i) => (
          <Line
            key={d.name}
            type="stepAfter"
            dataKey={d.name}
            stroke={COLORS[i % COLORS.length]}
            dot={false}
            strokeWidth={d.is_player ? 2 : 1}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}

function PointsChart({ drivers }) {
  if (!drivers?.length) return <div className="empty">No points data</div>;
  const sorted = [...drivers].sort((a, b) => (b.points || 0) - (a.points || 0)).slice(0, 10);
  const data = sorted.map((d) => ({ name: d.name.split(" ").pop(), pts: d.points || 0 }));

  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={data} layout="vertical" margin={{ top: 5, right: 20, left: 60, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" horizontal={false} />
        <XAxis type="number" stroke="var(--text-3)" tick={{ fontSize: 10, fontFamily: "var(--font-mono)" }} />
        <YAxis dataKey="name" type="category" stroke="var(--text-3)" tick={{ fontSize: 10, fontFamily: "var(--font-mono)" }} />
        <Tooltip content={<CustomTooltip />} />
        <Bar dataKey="pts" fill="var(--accent)" />
      </BarChart>
    </ResponsiveContainer>
  );
}

const TABS = ["POSITIONS", "CHAMPIONSHIP"];

export default function GraphsPage() {
  const [tab, setTab] = useState(0);
  const { data: state, loading, error } = useApi(api.getState);

  const drivers = state?.drivers || [];

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

      <div
        style={{
          display: "flex",
          gap: 3,
          marginBottom: 24,
          borderBottom: "1px solid var(--border)",
          paddingBottom: 0,
        }}
      >
        {TABS.map((t, i) => (
          <button
            key={t}
            onClick={() => setTab(i)}
            style={{
              fontFamily: "var(--font-display)",
              fontWeight: 700,
              fontSize: 11,
              letterSpacing: 2,
              padding: "9px 18px",
              border: "none",
              borderBottom: i === tab ? "2px solid var(--accent)" : "2px solid transparent",
              background: "none",
              color: i === tab ? "var(--text)" : "var(--text-3)",
              cursor: "pointer",
              transition: "color 0.15s",
            }}
          >
            {t}
          </button>
        ))}
      </div>

      <div className="chart-wrap">
        {tab === 0 && (
          <>
            <div className="chart-title">POSITION HISTORY</div>
            <PositionChart drivers={drivers} />
          </>
        )}
        {tab === 1 && (
          <>
            <div className="chart-title">CHAMPIONSHIP POINTS</div>
            <PointsChart drivers={drivers} />
          </>
        )}
      </div>

      <div className="section-title">Training Analysis</div>
      <div className="card" style={{ padding: 20 }}>
        <div style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-3)", letterSpacing: 1 }}>
          Training telemetry (understeer / oversteer graphs) will appear here once training data is available in the engine state.
        </div>
        {state?.training && (
          <div style={{ marginTop: 16 }}>
            <pre style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-2)" }}>
              {JSON.stringify(state.training, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}