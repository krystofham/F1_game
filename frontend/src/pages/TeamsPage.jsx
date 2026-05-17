import { useState } from "react";
import { useApi } from "../hooks/useApi";
import { api } from "../utils/api";

function TeamCard({ team, rank }) {
  const [imgErr, setImgErr] = useState(false);

  // Try to find team image from /engine/img
  const imgName = team.name
    .toLowerCase()
    .replace(/[^a-z0-9]/g, "_")
    .replace(/_+/g, "_");

  return (
    <div className="team-card">
      <div
        style={{
          position: "absolute",
          top: 12,
          right: 12,
          fontFamily: "var(--font-display)",
          fontSize: 40,
          fontWeight: 900,
          color: "var(--bg-3)",
          lineHeight: 1,
          userSelect: "none",
        }}
      >
        {rank}
      </div>

      <div className="team-img-wrap">
        {!imgErr ? (
          <img
            src={`http://localhost:8000/img/${imgName}.png`}
            alt={team.name}
            onError={() => setImgErr(true)}
          />
        ) : (
          <div
            style={{
              fontFamily: "var(--font-display)",
              fontSize: 28,
              fontWeight: 900,
              color: "var(--border-light)",
              letterSpacing: 2,
            }}
          >
            {team.name.slice(0, 3).toUpperCase()}
          </div>
        )}
      </div>

      <div className="team-name" style={{ fontSize: 13, marginBottom: 2 }}>
        {team.name}
      </div>
      <div className="team-pts">
        {team.points || 0} PTS
      </div>

      <div className="team-drivers">
        {(team.drivers || []).map((d, i) => (
          <div key={d} className="driver-row">
            <span style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 13 }}>{d}</span>
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: 9,
                color: "var(--text-3)",
                letterSpacing: 1,
              }}
            >
              DRV {i + 1}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function TeamsPage() {
  const { data, loading, error } = useApi(api.getTeams);
  const teams = data
    ? [...data].sort((a, b) => (b.points || 0) - (a.points || 0))
    : [];

  return (
    <div>
      <div className="page-header">
        <div className="page-eyebrow">Constructor Championship</div>
        <div className="page-title">
          TEAM <span>OVERVIEW</span>
        </div>
      </div>

      {loading && <div className="loading">FETCHING TEAMS</div>}
      {error && <div className="empty">⚠ {error}</div>}

      {teams.length > 0 && (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))",
            gap: 16,
          }}
        >
          {teams.map((t, i) => (
            <TeamCard key={t.name} team={t} rank={String(i + 1).padStart(2, "0")} />
          ))}
        </div>
      )}
    </div>
  );
}
