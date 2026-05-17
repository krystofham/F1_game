import { useState } from "react";
import { useApi } from "../hooks/useApi";
import { api } from "../utils/api";
import TyreBadge from "../components/TyreBadge";
import WearBar from "../components/WearBar";

function DriverDetail({ driver }) {
  const history = driver.history || driver.lap_times || [];
  const pits = driver.pit_stops || [];

  return (
    <div
      style={{
        background: "var(--bg)",
        border: "1px solid var(--border)",
        padding: 20,
        marginTop: 4,
      }}
    >
      <div className="grid-2" style={{ gap: 12, marginBottom: 16 }}>
        <div className="card">
          <div className="card-label">Points</div>
          <div className="card-value" style={{ fontSize: 28 }}>
            {driver.points || 0}
          </div>
        </div>
        <div className="card">
          <div className="card-label">Position</div>
          <div className="card-value" style={{ fontSize: 28 }}>
            P{driver.position || "—"}
          </div>
        </div>
      </div>

      {driver.pneu && (
        <div className="flex items-center gap-4 mb-4" style={{ gap: 16 }}>
          <div>
            <div className="card-label" style={{ marginBottom: 6 }}>Tyre</div>
            <TyreBadge type={driver.pneu} />
          </div>
          <div style={{ flex: 1 }}>
            <div className="card-label" style={{ marginBottom: 6 }}>Wear</div>
            <WearBar wear={driver.wear || 0} />
          </div>
        </div>
      )}

      {pits.length > 0 && (
        <div className="mb-4">
          <div className="card-label" style={{ marginBottom: 6 }}>Pit Stops</div>
          <div className="flex" style={{ gap: 6, flexWrap: "wrap" }}>
            {pits.map((p, i) => (
              <div key={i} className="badge badge-neutral">
                LAP {p.lap ?? p}
              </div>
            ))}
          </div>
        </div>
      )}

      {history.length > 0 && (
        <div>
          <div className="card-label" style={{ marginBottom: 6 }}>
            Lap History ({history.length} laps)
          </div>
          <div
            style={{
              display: "flex",
              gap: 3,
              flexWrap: "wrap",
              maxHeight: 80,
              overflow: "hidden",
            }}
          >
            {history.map((t, i) => (
              <div
                key={i}
                style={{
                  fontFamily: "var(--font-mono)",
                  fontSize: 9,
                  padding: "3px 6px",
                  background: "var(--bg-3)",
                  color: "var(--text-2)",
                  borderLeft: "1px solid var(--border)",
                }}
              >
                {typeof t === "number" ? t.toFixed(3) : t}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default function DriversPage() {
  const { data: drivers, loading, error } = useApi(api.getDrivers);
  const [expanded, setExpanded] = useState(null);

  const sorted = drivers
    ? [...drivers].sort((a, b) => (b.points || 0) - (a.points || 0))
    : [];

  return (
    <div>
      <div className="page-header">
        <div className="page-eyebrow">Driver Championship</div>
        <div className="page-title">
          DRIVER <span>PROFILES</span>
        </div>
      </div>

      {loading && <div className="loading">FETCHING DRIVERS</div>}
      {error && <div className="empty">⚠ {error}</div>}

      <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
        {sorted.map((d, i) => (
          <div key={d.name}>
            <div
              onClick={() => setExpanded(expanded === d.name ? null : d.name)}
              style={{
                display: "grid",
                gridTemplateColumns: "40px 1fr 140px 80px 80px 100px",
                alignItems: "center",
                gap: 12,
                padding: "14px 16px",
                background:
                  expanded === d.name
                    ? "rgba(232,0,45,0.05)"
                    : "var(--bg-card)",
                border: "1px solid",
                borderColor:
                  expanded === d.name ? "var(--accent)" : "var(--border)",
                cursor: "pointer",
                transition: "all 0.15s",
              }}
            >
              {/* Position */}
              <div
                style={{
                  fontFamily: "var(--font-display)",
                  fontWeight: 700,
                  fontSize: 18,
                  color: i < 3 ? ["var(--yellow)", "#aaa", "#cd7f32"][i] : "var(--text-3)",
                }}
              >
                {i + 1}
              </div>

              {/* Name */}
              <div>
                <div
                  style={{
                    fontFamily: "var(--font-display)",
                    fontWeight: 700,
                    fontSize: 15,
                    letterSpacing: 0.5,
                    color: d.is_player ? "var(--text)" : "var(--text-2)",
                  }}
                >
                  {d.name}
                  {d.is_player && (
                    <span
                      className="badge badge-ok"
                      style={{ marginLeft: 8, fontSize: 7 }}
                    >
                      YOU
                    </span>
                  )}
                </div>
                <div style={{ fontSize: 11, color: "var(--text-3)" }}>
                  {d.team || "—"}
                </div>
              </div>

              {/* Tyre + Wear */}
              <div className="flex items-center" style={{ gap: 8 }}>
                {d.pneu ? (
                  <>
                    <TyreBadge type={d.pneu} />
                    <WearBar wear={d.wear || 0} />
                  </>
                ) : (
                  <span className="text-muted" style={{ fontSize: 11 }}>—</span>
                )}
              </div>

              {/* Avg pos */}
              <div
                style={{
                  fontFamily: "var(--font-mono)",
                  fontSize: 11,
                  color: "var(--text-2)",
                  textAlign: "center",
                }}
              >
                {d.avg_position ? `AVG P${d.avg_position.toFixed(1)}` : "—"}
              </div>

              {/* DNF */}
              <div style={{ textAlign: "center" }}>
                {d.dnf ? (
                  <span className="badge badge-err">DNF</span>
                ) : (
                  <span className="badge badge-ok">ACTIVE</span>
                )}
              </div>

              {/* Points */}
              <div style={{ textAlign: "right" }}>
                <span className="points-pill">{d.points || 0} PTS</span>
              </div>
            </div>

            {expanded === d.name && <DriverDetail driver={d} />}
          </div>
        ))}
      </div>
    </div>
  );
}
