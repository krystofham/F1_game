import { useState } from "react";
import { useApi } from "../hooks/useApi";
import { api } from "../utils/api";
import { Link } from "react-router-dom";

const getPointsForPosition = (position) => {
  const pointsMap = {
    1: 50, 2: 45, 3: 40, 4: 35, 5: 30, 6: 25, 7: 22, 8: 20, 9: 18, 10: 15,
    11: 12, 12: 10, 13: 9, 14: 8, 15: 7, 16: 6, 17: 5, 18: 4, 19: 3, 20: 2,
    21: 1, 22: 1, 23: 1,
  };
  return pointsMap[position] || 0;
};

// Asymetrický grid layout pro top 5 týmů
const SLOT_STYLES = [
  { gridColumn: "1 / 4", gridRow: "1 / 3", heroSize: true },  // #1 - Hero (3 sloupce, 2 řádky)
  { gridColumn: "4 / 5", gridRow: "1 / 3", tallCard: true },  // #2 - Vysoká
  { gridColumn: "5 / 6", gridRow: "1 / 3", tallCard: true },  // #3 - Vysoká (stejná jako 2)
  { gridColumn: "6 / 7", gridRow: "1 / 3", tallCard: true },  // #4 - Vysoká (stejná jako 2)
  { gridColumn: "1 / 4", gridRow: "3 / 4", wideCard: true },  // #5 - Spodní široká (vyšší)
  { gridColumn: "4 / 7", gridRow: "3 / 4", wideCard: true },  // #6 - Spodní široká (stejná jako 5)
];
function TeamCard({ team, currentRank, newRank, isLive, slotStyle = {} }) {
  const [imgErr, setImgErr] = useState(false);

  const imgName = team.name
    .toLowerCase()
    .replace(/[^a-z0-9]/g, "_")
    .replace(/_+/g, "_");

  const rankDiff = currentRank - newRank;
  const displayedRank = isLive ? newRank : currentRank;
  const displayedPoints = isLive ? team.newTotalPoints : team.points || 0;

  const isHero = slotStyle.heroSize;
  const isTall = slotStyle.tallCard;
  const isWide = slotStyle.wideCard;

  let rankClass = "pn";
  let rowClass = "";
  if (displayedRank === 1) { rankClass = "p1"; rowClass = "row-gold"; }
  else if (displayedRank === 2) { rankClass = "p2"; rowClass = "row-silver"; }
  else if (displayedRank === 3) { rankClass = "p3"; rowClass = "row-bronze"; }

  return (
    <Link
      to={`/team/${team.name}`}
      style={{
        textDecoration: "none",
        color: "inherit",
        gridColumn: slotStyle.gridColumn,
        gridRow: slotStyle.gridRow,
        display: "block",
      }}
    >
      <div
        className={`team-card ${rowClass}`}
        style={{
          height: "100%",
          display: "flex",
          flexDirection: isWide ? "row" : "column",
          alignItems: isWide ? "center" : "flex-start",
          gap: isWide ? 40 : 0,
          padding: isHero ? 32 : isWide ? "16px 28px" : 20,
          overflow: "hidden",
          position: "relative",
        }}
      >
        {/* Velké číslo pozice v pozadí */}
        <div
          style={{
            position: "absolute",
            bottom: -16,
            right: isWide ? 20 : 10,
            fontFamily: "var(--font-display)",
            fontWeight: 900,
            fontSize: isHero ? 180 : isTall ? 140 : isWide ? 100 : 80,
            lineHeight: 1,
            color: "rgba(255,255,255,0.03)",
            userSelect: "none",
            pointerEvents: "none",
            letterSpacing: -6,
          }}
        >
          {String(displayedRank).padStart(2, "0")}
        </div>

        {/* Levá / horní sekce */}
        <div style={{ flex: isWide ? "0 0 auto" : undefined }}>
          {/* Rank badge */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 10,
              marginBottom: isHero ? 20 : 10,
            }}
          >
            <span className={`pos-num ${rankClass}`} style={{ fontSize: isHero ? 20 : 14 }}>
              {displayedRank}
            </span>
            <span className="text-mono" style={{ fontSize: 9, letterSpacing: 3 }}>
              P{displayedRank}
            </span>
          </div>

          {/* Obrázek týmu */}
          <div
            className="team-img-wrap"
            style={{
              height: isHero ? 110 : isTall ? 80 : isWide ? 60 : 56,
              marginBottom: isHero ? 20 : 10, 
            }}
          >
            {!imgErr ? (
              <img
                src={`http://localhost:8000/img/${imgName}.png`}
                alt={team.name}
                onError={() => setImgErr(true)}
                style={{ maxHeight: "100%", maxWidth: "100%", objectFit: "contain","borderRadius": "50%", }}
              />
            ) : (
              <span
                style={{
                  fontFamily: "var(--font-display)",
                  fontWeight: 900,
                  fontSize: isHero ? 32 : 18,
                  color: "var(--text-3)",
                  letterSpacing: 3,
                }}
              >
                {team.name.slice(0, 3).toUpperCase()}
              </span>
            )}
          </div>

          {/* Název */}
          <div
            className="team-name"
            style={{ fontSize: isHero ? 20 : isTall ? 14 : 12, marginBottom: isWide ? 0 : 4 }}
          >
            {team.name}
          </div>
        </div>

        {/* Pravá / spodní sekce */}
        <div
          style={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            justifyContent: isWide ? "center" : "flex-end",
          }}
        >
          {/* Body */}
          <div style={{ marginBottom: 4 }}>
            <span
              style={{
                fontFamily: "var(--font-display)",
                fontWeight: 900,
                fontSize: isHero ? 56 : isTall ? 40 : isWide ? 36 : 26,
                lineHeight: 1,
                color: "var(--text)",
                letterSpacing: -1,
              }}
            >
              {displayedPoints}
            </span>
            <span className="team-pts" style={{ marginLeft: 6, fontSize: isHero ? 12 : 9 }}>
              PTS
            </span>
          </div>

          {/* Live badge */}
          {isLive && (
            <div style={{ marginBottom: isWide ? 0 : 10 }}>
              {rankDiff !== 0 ? (
                <span
                  className="badge"
                  style={{
                    borderColor: rankDiff > 0 ? "var(--green)" : "var(--red)",
                    color: rankDiff > 0 ? "var(--green)" : "var(--red)",
                    fontSize: 9,
                  }}
                >
                  {rankDiff > 0 ? `▲ +${rankDiff}` : `▼ ${rankDiff}`} POS
                </span>
              ) : (<></>
              )}
            </div>
          )}

          {/* Jezdci — u wide karty horizontálně */}
          <div
            className="team-drivers"
            style={isWide ? { flexDirection: "row", gap: 8 } : {}}
          >
            {(team.drivers || []).map((d, i) => (
              <div key={d} className="driver-row" style={isWide ? { flex: "0 0 auto", minWidth: 140 } : {}}>
                <span
                  style={{
                    fontFamily: "var(--font-display)",
                    fontWeight: 600,
                    fontSize: isHero ? 13 : 11,
                    letterSpacing: 0.5,
                  }}
                >
                  {d}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Link>
  );
}

export default function TeamsPage() {
  const { data: teamsData, loading: teamsLoading, error: teamsError } =
    useApi(api.getTeams);
  const { data: stateData } = useApi(api.getState);
  const [isLive, setIsLive] = useState(true);

  let teams = [];

  if (teamsData) {
    const currentSortedTeams = [...teamsData].sort(
      (a, b) => (b.points || 0) - (a.points || 0)
    );
    const currentRankMap = {};
    currentSortedTeams.forEach((t, i) => { currentRankMap[t.name] = i + 1; });

    const driverRacePositions = {};
    if (stateData?.drivers) {
      stateData.drivers.forEach((d) => {
        driverRacePositions[d.name] =
          d.position_history?.length > 0
            ? d.position_history[d.position_history.length - 1]
            : d.position || 99;
      });
    }

    const simulatedTeams = teamsData.map((team) => {
      let racePoints = 0;
      (team.drivers || []).forEach((name) => {
        const pos = driverRacePositions[name];
        if (pos) racePoints += getPointsForPosition(pos);
      });
      return {
        ...team,
        currentRank: currentRankMap[team.name] || 99,
        newTotalPoints: (team.points || 0) + racePoints,
        simulatedRacePoints: racePoints,
      };
    });

    const newSorted = [...simulatedTeams].sort(
      (a, b) => b.newTotalPoints - a.newTotalPoints
    );
    teams = newSorted.map((team, i) => ({ ...team, newRank: i + 1 }));
  }

  const displayedTeams = [...teams].sort((a, b) =>
    isLive ? a.newRank - b.newRank : a.currentRank - b.currentRank
  );
const topTeams = displayedTeams.slice(0, 6);
const restTeams = displayedTeams.slice(6);

  return (
    <div>
      <div
        className="page-header"
        style={{ display: "flex", alignItems: "flex-end", justifyContent: "space-between" }}
      >
        <div>
          <div className="page-eyebrow">Constructor Championship</div>
          <div className="page-title">
            TEAM OVERVIEW
          </div>
        </div>

        <div
          style={{
            display: "flex",
            border: "1px solid var(--border)",
            overflow: "hidden",
            marginBottom: 4,
          }}
        >
          {[false, true].map((live) => (
            <button
              key={String(live)}
              onClick={() => setIsLive(live)}
              style={{
                padding: "8px 20px",
                cursor: "pointer",
                background: isLive === live ? "var(--accent)" : "transparent",
                color: isLive === live ? "var(--bg)" : "var(--text-3)",
                border: "none",
                borderLeft: live ? "1px solid var(--border)" : "none",
                fontFamily: "var(--font-display)",
                fontWeight: 700,
                fontSize: 11,
                letterSpacing: 2,
                textTransform: "uppercase",
                transition: "all 0.15s",
              }}
            >
              {live ? "Live" : "Normal"}
            </button>
          ))}
        </div>
      </div>

      {teamsLoading && <div className="loading">FETCHING TEAMS</div>}
      {teamsError && <div className="empty">⚠ {teamsError}</div>}

{displayedTeams.length > 0 && (
      <>
        {/* Asymetrický hero grid — top 6 týmů */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(6, 1fr)", // Změněno na 6 sloupců pro symetrii
            gridTemplateRows: "220px 220px 180px", // 3. řádek zvýšen ze 140px na 180px
            gap: 2,
            marginBottom: 2,
          }}
        >
          {topTeams.map((t, i) => (
            <TeamCard
              key={t.name}
              team={t}
              currentRank={t.currentRank}
              newRank={t.newRank}
              isLive={isLive}
              slotStyle={SLOT_STYLES[i] || {}}
            />
          ))}
        </div>

        {/* Zbytek — klasický grid */}
        {restTeams.length > 0 && (
          <div className="grid-4" style={{ gap: 2 }}>
            {restTeams.map((t) => (
              <TeamCard
                key={t.name}
                team={t}
                currentRank={t.currentRank}
                newRank={t.newRank}
                isLive={isLive}
                slotStyle={{}}
              />
            ))}
          </div>
        )}
      </>
    )}
  </div>
);
}