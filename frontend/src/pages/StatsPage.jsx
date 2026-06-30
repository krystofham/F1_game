import { useEffect, useMemo, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell,
} from "recharts";
import { api } from "../utils/api";

const WEATHER_COLORS = {
  sunny: "#ffd600",
  rain: "#448aff",
  "heavy rain": "#1565c0",
  transitional: "#aa00ff",
};

function StatSummary({ records, raceHistory }) {
  const uniqueWinners = new Set(raceHistory.map((r) => r.driver)).size;
  const bestRecord = records.length
    ? records.reduce((best, r) => (parseFloat(r.lap_time) < parseFloat(best.lap_time) ? r : best))
    : null;

  const winsByDriver = raceHistory.reduce((acc, row) => {
    acc[row.driver] = (acc[row.driver] || 0) + 1;
    return acc;
  }, {});
  const topWinner = Object.entries(winsByDriver).sort((a, b) => b[1] - a[1])[0];

  return (
    <div className="stats-grid mb-6">
      <div className="stat-card">
        <div className="stat-card-label">Grand Prix Races</div>
        <div className="stat-card-value">{raceHistory.length}</div>
        <div className="stat-card-sub">recorded in CSV</div>
      </div>
      <div className="stat-card">
        <div className="stat-card-label">Unique Winners</div>
        <div className="stat-card-value">{uniqueWinners || "—"}</div>
        <div className="stat-card-sub">
          {topWinner ? `${topWinner[0].split(" ").pop()} leads (${topWinner[1]})` : "no wins yet"}
        </div>
      </div>
      <div className="stat-card">
        <div className="stat-card-label">Track Records</div>
        <div className="stat-card-value">{records.length}</div>
        <div className="stat-card-sub">circuits with data</div>
      </div>
      <div className="stat-card">
        <div className="stat-card-label">Fastest Lap Ever</div>
        <div className="stat-card-value">
          {bestRecord ? parseFloat(bestRecord.lap_time).toFixed(3) : "—"}
        </div>
        <div className="stat-card-sub">
          {bestRecord ? `${bestRecord.driver.split(" ").pop()} · ${bestRecord.track}` : "—"}
        </div>
      </div>
    </div>
  );
}

function TrackRecordsChart({ records }) {
  if (!records.length) return null;

  const data = [...records]
    .map((r) => ({
      track: r.track.replace(" Grand Prix", "").replace(" Circuit", ""),
      lap_time: parseFloat(r.lap_time),
      driver: r.driver,
    }))
    .sort((a, b) => a.lap_time - b.lap_time);

  return (
    <div className="chart-wrap mb-6">
      <div className="chart-title">Track Records by Lap Time</div>
      <ResponsiveContainer width="100%" height={Math.max(240, data.length * 28)}>
        <BarChart data={data} layout="vertical" margin={{ top: 5, right: 20, left: 80, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" horizontal={false} />
          <XAxis
            type="number"
            stroke="var(--text-3)"
            tick={{ fontSize: 10, fontFamily: "var(--font-mono)" }}
            domain={["dataMin - 2", "dataMax + 2"]}
          />
          <YAxis
            dataKey="track"
            type="category"
            stroke="var(--text-3)"
            tick={{ fontSize: 9, fontFamily: "var(--font-mono)" }}
            width={75}
          />
          <Tooltip
            content={({ active, payload }) => {
              if (!active || !payload?.length) return null;
              const row = payload[0].payload;
              return (
                <div style={{ background: "var(--bg-card)", border: "1px solid var(--border)", padding: "10px 14px" }}>
                  <div style={{ fontFamily: "var(--font-mono)", fontSize: 11 }}>{row.driver}</div>
                  <div style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--yellow)" }}>
                    {row.lap_time.toFixed(4)}s
                  </div>
                </div>
              );
            }}
          />
          <Bar dataKey="lap_time" fill="var(--yellow)" radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function WinsChart({ raceHistory }) {
  const data = useMemo(() => {
    const counts = raceHistory.reduce((acc, row) => {
      acc[row.driver] = (acc[row.driver] || 0) + 1;
      return acc;
    }, {});
    return Object.entries(counts)
      .map(([driver, wins]) => ({ driver: driver.split(" ").pop(), fullName: driver, wins }))
      .sort((a, b) => b.wins - a.wins)
      .slice(0, 12);
  }, [raceHistory]);

  if (!data.length) return null;

  return (
    <div className="chart-wrap mb-6">
      <div className="chart-title">GP Wins by Driver</div>
      <ResponsiveContainer width="100%" height={Math.max(220, data.length * 28)}>
        <BarChart data={data} layout="vertical" margin={{ top: 5, right: 20, left: 55, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" horizontal={false} />
          <XAxis type="number" stroke="var(--text-3)" tick={{ fontSize: 10, fontFamily: "var(--font-mono)" }} allowDecimals={false} />
          <YAxis dataKey="driver" type="category" stroke="var(--text-3)" tick={{ fontSize: 10, fontFamily: "var(--font-mono)" }} width={50} />
          <Tooltip
            content={({ active, payload }) => {
              if (!active || !payload?.length) return null;
              const row = payload[0].payload;
              return (
                <div style={{ background: "var(--bg-card)", border: "1px solid var(--border)", padding: "10px 14px" }}>
                  <div style={{ fontFamily: "var(--font-mono)", fontSize: 11 }}>{row.fullName}</div>
                  <div style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--accent)" }}>{row.wins} wins</div>
                </div>
              );
            }}
          />
          <Bar dataKey="wins" fill="var(--accent)" radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function WeatherBreakdown({ raceHistory }) {
  const data = useMemo(() => {
    const counts = raceHistory.reduce((acc, row) => {
      const w = (row.weather || "sunny").toLowerCase();
      acc[w] = (acc[w] || 0) + 1;
      return acc;
    }, {});
    return Object.entries(counts).map(([weather, count]) => ({ weather, count }));
  }, [raceHistory]);

  if (!data.length) return null;

  return (
    <div className="chart-wrap mb-6">
      <div className="chart-title">Race Weather Distribution</div>
      <ResponsiveContainer width="100%" height={180}>
        <BarChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
          <XAxis
            dataKey="weather"
            stroke="var(--text-3)"
            tick={{ fontSize: 10, fontFamily: "var(--font-mono)" }}
            tickFormatter={(v) => v.toUpperCase()}
          />
          <YAxis stroke="var(--text-3)" tick={{ fontSize: 10, fontFamily: "var(--font-mono)" }} allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="count" radius={[4, 4, 0, 0]}>
            {data.map((entry, i) => (
              <Cell key={i} fill={WEATHER_COLORS[entry.weather] || "var(--accent)"} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default function StatsPage() {
  const [records, setRecords] = useState([]);
  const [raceHistory, setRaceHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.getTrackRecords(), api.getBiggestLaps()])
      .then(([recordsData, historyData]) => {
        setRecords(recordsData);
        setRaceHistory(historyData.filter((item) => String(item.position) === "1"));
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load historical CSV statistics:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="loading">LOADING HISTORICAL DATA</div>;
  }

  if (records.length === 0 && raceHistory.length === 0) {
    return <div className="empty">NO RECORDED STATS FOUND IN CSV FILES</div>;
  }

  return (
    <div className="main-content">
      <div className="page-header">
        <div className="page-eyebrow">Database Records</div>
        <h1 className="page-title">
          Game <span>Statistics</span>
        </h1>
      </div>

      <StatSummary records={records} raceHistory={raceHistory} />

      <div className="stats-charts-grid">
        <TrackRecordsChart records={records} />
        <WinsChart raceHistory={raceHistory} />
      </div>

      <WeatherBreakdown raceHistory={raceHistory} />

      <div className="section-title">Absolute Track Records</div>
      <div className="card mb-6">
        <table className="data-table">
          <thead>
            <tr>
              <th>Circuit</th>
              <th>Driver</th>
              <th>Team</th>
              <th style={{ textAlign: "right" }}>Lap Time</th>
              <th style={{ textAlign: "center" }}>Season</th>
            </tr>
          </thead>
          <tbody>
            {records.map((row, index) => (
              <tr key={index}>
                <td style={{ fontWeight: "700" }}>{row.track}</td>
                <td>{row.driver}</td>
                <td className="text-muted">{row.team}</td>
                <td style={{ textAlign: "right" }} className="text-yellow text-mono">
                  {parseFloat(row.lap_time).toFixed(4)}s
                </td>
                <td style={{ textAlign: "center" }} className="text-mono">
                  {row.season}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="section-title">Historical GP Winners</div>
      <div className="card">
        <table className="data-table">
          <thead>
            <tr>
              <th style={{ textAlign: "center" }}>Season</th>
              <th>Grand Prix Event</th>
              <th>Winner</th>
              <th>Team Name</th>
              <th>Weather</th>
              <th style={{ textAlign: "right" }}>Total Time</th>
            </tr>
          </thead>
          <tbody>
            {raceHistory.map((row, index) => (
              <tr key={index}>
                <td style={{ textAlign: "center" }} className="text-mono">
                  {row.season}
                </td>
                <td style={{ fontWeight: "700" }}>{row.race}</td>
                <td>{row.driver}</td>
                <td className="text-muted">{row.team}</td>
                <td className="text-mono" style={{ textTransform: "uppercase" }}>
                  {row.weather}
                </td>
                <td style={{ textAlign: "right" }} className="text-mono">
                  {parseFloat(row.total_time).toFixed(3)}s
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
