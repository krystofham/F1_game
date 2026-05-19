import { Link, useParams, useNavigate } from "react-router-dom";
import { useApi } from "../hooks/useApi";
import { api } from "../utils/api";

function RatingBar({ value }) {
  // Rating appears to be ~4-7 range, normalize to 0-10
  const pct = Math.min(100, (value / 10) * 100);
  const color =
    value >= 6 ? "var(--green)" : value >= 5 ? "var(--yellow)" : "var(--accent)";
  return (
    <div className="wear-bar-wrap">
      <div className="wear-bar-bg" style={{ flex: 1 }}>
        <div
          className="wear-bar-fill"
          style={{ width: `${pct}%`, background: color }}
        />
      </div>
    </div>
  );
}

function StatBlock({ label, value, accent }) {
  return (
    <div className="card" style={{ flex: 1 }}>
      <div className="card-label">{label}</div>
      <div
        className="card-value"
        style={{ color: accent || "var(--text)", fontSize: 28 }}
      >
        {value}
      </div>
    </div>
  );
}

function DriverCard({ name, index }) {
  const num = index + 1;
  return (
    <div
      style={{
        background: "var(--bg-3)",
        border: "1px solid var(--border)",
        borderLeft: `3px solid ${index === 0 ? "var(--accent)" : "var(--blue)"}`,
        padding: "18px 20px",
        display: "flex",
        alignItems: "center",
        gap: 16,
      }}
    >
      <div
        style={{
          fontFamily: "var(--font-display)",
          fontWeight: 900,
          fontSize: 36,
          color: index === 0 ? "var(--accent)" : "var(--blue)",
          opacity: 0.25,
          lineHeight: 1,
          minWidth: 40,
        }}
      >
        {num < 10 ? `0${num}` : num}
      </div>
      <div style={{ flex: 1 }}>
        <div
          style={{
            fontFamily: "var(--font-display)",
            fontWeight: 700,
            fontSize: 20,
            letterSpacing: 1,
            textTransform: "uppercase",
            color: "var(--text)",
          }}
        >
          {name}
        </div>
        <div
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: 9,
            letterSpacing: 2,
            color: "var(--text-3)",
            marginTop: 4,
          }}
        >
          DRIVER {index === 0 ? "01 · PRIMARY" : "02 · SECONDARY"}
        </div>
      </div>
      <div
        style={{
          fontFamily: "var(--font-display)",
          fontWeight: 700,
          fontSize: 11,
          letterSpacing: 2,
          padding: "4px 10px",
          border: `1px solid ${index === 0 ? "var(--accent)" : "var(--blue)"}`,
          color: index === 0 ? "var(--accent)" : "var(--blue)",
          textTransform: "uppercase",
        }}
      >
        ACTIVE
      </div>
    </div>
  );
}

export default function TeamPage() {
  const { teamId } = useParams();
  const navigate = useNavigate();
  const name = decodeURIComponent(teamId);

  const { data: team, loading, error } = useApi(() => api.getTeam(name), [name]);
  const { data: allTeams } = useApi(() => api.getTeams(), []);

  if (loading) return <div className="loading">LOADING TEAM DATA</div>;
  if (error)
    return (
      <div className="empty">
        <div style={{ color: "var(--accent)", marginBottom: 12 }}>⚠ {error}</div>
        <button className="btn" onClick={() => navigate("/teams")}>
          ← BACK TO TEAMS
        </button>
      </div>
    );
  if (!team) return null;

  const totalTeams = allTeams ? allTeams.length : "—";
  const ratingPct = Math.min(100, (team.rating / 10) * 100);
  const ratingColor =
    team.rating >= 6
      ? "var(--green)"
      : team.rating >= 5
      ? "var(--yellow)"
      : "var(--accent)";

  // Championship gap
  const leader = allTeams
    ? allTeams.reduce((a, b) => (a.points > b.points ? a : b), allTeams[0])
    : null;
  const gap =
    leader && leader.name !== team.name ? leader.points - team.points : 0;

  return (
    <>
      {/* ── BACK ── */}
      <button
        className="btn"
        onClick={() => navigate("/teams")}
        style={{ marginBottom: 24 }}
      >
        ← TEAMS
      </button>

      {/* ── HEADER ── */}
      <div className="page-header" style={{ marginBottom: 28 }}>
        <div className="page-eyebrow">TEAM PROFILE</div>
        <div
          className="page-title"
          style={{ fontSize: 36, letterSpacing: 0, lineHeight: 1.1 }}
        >
          {team.name
            .split(" ")
            .map((w, i) =>
              i === 0 ? (
                <span key={i} style={{ color: "var(--accent)" }}>
                  {w}{" "}
                </span>
              ) : (
                <span key={i}>{w} </span>
              )
            )}
        </div>
      </div>

      {/* ── POSITION BANNER ── */}
      <div
        style={{
          background: "var(--bg-card)",
          border: "1px solid var(--border)",
          borderLeft: "4px solid var(--accent)",
          padding: "16px 24px",
          display: "flex",
          alignItems: "center",
          gap: 32,
          marginBottom: 24,
        }}
      >
        <div>
          <div className="card-label" style={{ marginBottom: 4 }}>
            CHAMPIONSHIP POSITION
          </div>
          <div
            style={{
              fontFamily: "var(--font-display)",
              fontSize: 64,
              fontWeight: 900,
              lineHeight: 1,
              color:
                team.position === 1
                  ? "var(--yellow)"
                  : team.position <= 3
                  ? "var(--text)"
                  : "var(--text-2)",
            }}
          >
            P{team.position}
          </div>
        </div>

        <div
          style={{
            width: 1,
            height: 60,
            background: "var(--border)",
          }}
        />

        <div style={{ flex: 1 }}>
          <div className="card-label" style={{ marginBottom: 8 }}>
            TEAM RATING
          </div>
          <RatingBar value={team.rating} />
        </div>

        <div
          style={{
            width: 1,
            height: 60,
            background: "var(--border)",
          }}
        />

        <div style={{ textAlign: "right" }}>
          <div className="card-label" style={{ marginBottom: 4 }}>
            {gap > 0 ? "GAP TO LEADER" : "CHAMPIONSHIP LEAD"}
          </div>
          <div
            style={{
              fontFamily: "var(--font-display)",
              fontSize: 32,
              fontWeight: 700,
              color: gap > 0 ? "var(--accent)" : "var(--green)",
            }}
          >
            {gap > 0 ? `-${gap} PTS` : "LEADER"}
          </div>
        </div>
      </div>

      {/* ── STATS GRID ── */}
      <div className="section-title">STATISTICS</div>
      <div className="grid-3" style={{ marginBottom: 24 }}>
        <StatBlock label="POINTS" value={team.points} accent="var(--accent)" />
        <StatBlock
          label="POSITION"
          value={`P${team.position}`}
          accent={team.position === 1 ? "var(--yellow)" : undefined}
        />
        <StatBlock label="DRIVERS" value={team.drivers.length} />
      </div>

      {/* ── RATING VISUAL ── */}


      {/* ── DRIVERS ── */}
      <div className="section-title">DRIVER LINEUP</div>
      <div style={{ display: "flex", flexDirection: "column", gap: 10, marginBottom: 24 }}>
        {team.drivers.map((name, i) => (
          <DriverCard key={name} name={name} index={i} />
        ))}
      </div>

      {/* ── CHAMPIONSHIP CONTEXT ── */}
      {allTeams && (
        <>
          <div className="section-title">CHAMPIONSHIP STANDINGS</div>
          <div
            style={{
              background: "var(--bg-card)",
              border: "1px solid var(--border)",
            }}
          >
            <table className="data-table">
              <thead>
                <tr>
                  <th>POS</th>
                  <th>TEAM</th>
                  <th>RATING</th>
                  <th>POINTS</th>
                  <th>GAP</th>
                </tr>
              </thead>
              <tbody>
                {allTeams
                  .slice()
                  .sort((a, b) => a.position - b.position)
                  .map((t) => {
                    const isThis = t.name === team.name;
                    const g = leader ? leader.points - t.points : 0;
                    return (
                      <tr
                        key={t.name}
                        style={{
                          background: isThis
                            ? "rgba(232,0,45,0.06)"
                            : undefined,
                          cursor: "pointer",
                        }}
                        onClick={() =>
                          !isThis &&
                          navigate(
                            `/team/${encodeURIComponent(t.name)}`
                          )
                        }
                      >
                        <td>
                          <div
                            className={`pos-badge ${
                              t.position === 1
                                ? "p1"
                                : t.position === 2
                                ? "p2"
                                : t.position === 3
                                ? "p3"
                                : ""
                            }`}
                          >
                            {t.position}
                          </div>
                        </td>
                        <td>
                          <span
                            style={{
                              color: isThis ? "var(--accent)" : "var(--text)",
                              fontWeight: isThis ? 600 : 400,
                            }}
                          >
                            {t.name}
                          </span>
                          {isThis && (
                            <span
                              className="badge badge-err"
                              style={{ marginLeft: 10, fontSize: 8 }}
                            >
                              YOU
                            </span>
                          )}
                        </td>
                        <td>
                          <span className="text-mono">{t.rating.toFixed(4)}</span>
                        </td>
                        <td>
                          <span className="points-pill">{t.points}</span>
                        </td>
                        <td>
                          <span
                            style={{
                              fontFamily: "var(--font-mono)",
                              fontSize: 11,
                              color: g === 0 ? "var(--green)" : "var(--text-3)",
                            }}
                          >
                            {g === 0 ? "LEADER" : `-${g}`}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
              </tbody>
            </table>
          </div>
        </>
      )}
    </>
  );
}