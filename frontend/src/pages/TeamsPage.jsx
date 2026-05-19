import { useState } from "react";
import { useApi } from "../hooks/useApi";
import { api } from "../utils/api";
import { Link } from "react-router-dom";

// Pomocná funkce v JS, která simuluje tvé bodování z Pythonu
const getPointsForPosition = (position) => {
  const pointsMap = {
    1: 50, 2: 45, 3: 40, 4: 35, 5: 30, 6: 25, 7: 22, 8: 20, 9: 18, 10: 15,
    11: 12, 12: 10, 13: 9, 14: 8, 15: 7, 16: 6, 17: 5, 18: 4, 19: 3, 20: 2,
    21: 1, 22: 1, 23: 1
  };
  return pointsMap[position] || 0;
};

function TeamCard({ team, currentRank, newRank, isLive }) {
  const [imgErr, setImgErr] = useState(false);

  const imgName = team.name
    .toLowerCase()
    .replace(/[^a-z0-9]/g, "_")
    .replace(/_+/g, "_");

  // Výpočet změny pozice pro zobrazení šipky
  const rankDiff = currentRank - newRank; 
  let rankIndicator = "▬";
  let indicatorColor = "var(--text-3)";
  if (rankDiff > 0) {
    rankIndicator = `▲ +${rankDiff}`;
    indicatorColor = "var(--accent-ok, #28a745)";
  } else if (rankDiff < 0) {
    rankIndicator = `▼ ${rankDiff}`;
    indicatorColor = "var(--accent-err, #dc3545)";
  }

  // Rozhodnutí o tom, co zobrazit na základě režimu
  const displayedRank = isLive ? newRank : currentRank;
  const displayedPoints = isLive ? team.newTotalPoints : (team.points || 0);

  return (
    <Link to={`/team/${team.name}`} style={{ textDecoration: "none", color: "white" }}>
      <div className="team-card" style={{ position: "relative" }}>
        {/* Původní vs Nová pozice */}
        <div
          style={{
            position: "absolute",
            top: 12,
            right: 12,
            fontFamily: "var(--font-display)",
            textAlign: "right",
            lineHeight: 1.1,
          }}
        >
          <div style={{ fontSize: 32, fontWeight: 900, color: "var(--text)" }}>
            #{String(displayedRank).padStart(2, "0")}
          </div>
          {/* Šipku ukazujeme jen v Live režimu */}
          {isLive && (
            <div style={{ fontSize: 10, fontFamily: "var(--font-mono)", color: indicatorColor, fontWeight: 700 }}>
              {rankIndicator}
            </div>
          )}
        </div>

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

        <div className="team-img-wrap">
          {!imgErr ? (
            <img
              style={{ borderRadius: "50%" }}
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

        <div className="team-name" style={{ fontSize: 13, marginBottom: 2, paddingRight: 60 }}>
          {team.name}
        </div>
        <div className="team-pts">
          {displayedPoints} PTS 
          {/* Nasimulované body ukazujeme jen v Live režimu */}
          {isLive && (
            <span style={{ fontSize: 11, color: "var(--text-3)", marginLeft: 6 }}>
              (+{team.simulatedRacePoints || 0} fresh)
            </span>
          )}
        </div>

        <div className="team-drivers">
          {(team.drivers || []).map((d, i) => (
            <div key={d} className="driver-row">
              <span style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 13 }}>{d}</span>
              <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-3)", letterSpacing: 1 }}>
                DRV {i + 1}
              </span>
            </div>
          ))}
        </div>
      </div>
    </Link>
  );
}

export default function TeamsPage() {
  const { data: teamsData, loading: teamsLoading, error: teamsError } = useApi(api.getTeams);
  const { data: stateData } = useApi(api.getState);
  
  // Stav pro přepínání mezi normálním zobrazením a live timingem
  const [isLive, setIsLive] = useState(true);

  let teams = [];

  if (teamsData) {
    const currentSortedTeams = [...teamsData].sort((a, b) => (b.points || 0) - (a.points || 0));
    
    const currentRankMap = {};
    currentSortedTeams.forEach((t, index) => {
      currentRankMap[t.name] = index + 1;
    });

    const driverRacePositions = {};
    if (stateData && stateData.drivers) {
      stateData.drivers.forEach((d) => {
        if (d.position_history && d.position_history.length > 0) {
          driverRacePositions[d.name] = d.position_history[d.position_history.length - 1];
        } else {
          driverRacePositions[d.name] = d.position || 99;
        }
      });
    }

    const simulatedTeams = teamsData.map((team) => {
      let racePointsForTeam = 0;

      (team.drivers || []).forEach((driverName) => {
        const finalPosition = driverRacePositions[driverName];
        if (finalPosition) {
          racePointsForTeam += getPointsForPosition(finalPosition);
        }
      });

      return {
        ...team,
        currentRank: currentRankMap[team.name] || 99,
        newTotalPoints: (team.points || 0) + racePointsForTeam,
        simulatedRacePoints: racePointsForTeam 
      };
    });

    const newSortedTeams = [...simulatedTeams].sort((a, b) => b.newTotalPoints - a.newTotalPoints);

    teams = newSortedTeams.map((team, index) => ({
      ...team,
      newRank: index + 1
    }));
  }

  // Řazení na základě vybraného režimu
  const displayedTeams = [...teams].sort((a, b) => {
    return isLive ? a.newRank - b.newRank : a.currentRank - b.currentRank;
  });

  return (
    <div>
      <div className="page-header">
        <div className="page-eyebrow">Constructor Championship</div>
        <div className="page-title">
          TEAM <span>OVERVIEW</span>
        </div>
      </div>

      {/* Navigační přepínač režimů */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '24px' }}>
        <button 
          onClick={() => setIsLive(false)}
          style={{
            padding: '8px 16px',
            cursor: 'pointer',
            backgroundColor: !isLive ? 'var(--accent, #007bff)' : 'transparent',
            color: !isLive ? '#fff' : 'var(--text-3, #ccc)',
            border: '1px solid var(--accent, #007bff)',
            borderRadius: '4px',
            fontFamily: 'var(--font-display)',
            fontWeight: 700
          }}
        >
          NORMAL
        </button>
        <button 
          onClick={() => setIsLive(true)}
          style={{
            padding: '8px 16px',
            cursor: 'pointer',
            backgroundColor: isLive ? 'var(--accent, #007bff)' : 'transparent',
            color: isLive ? '#fff' : 'var(--text-3, #ccc)',
            border: '1px solid var(--accent, #007bff)',
            borderRadius: '4px',
            fontFamily: 'var(--font-display)',
            fontWeight: 700
          }}
        >
          LIVE TIMING
        </button>
      </div>

      {teamsLoading && <div className="loading">FETCHING TEAMS</div>}
      {teamsError && <div className="empty">⚠ {teamsError}</div>}

      {displayedTeams.length > 0 && (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))",
            gap: 16,
          }}
        >
          {displayedTeams.map((t) => (
            <TeamCard 
              key={t.name} 
              team={t} 
              currentRank={t.currentRank} 
              newRank={t.newRank}
              isLive={isLive}
            />
          ))}
        </div>
      )}
    </div>
  );
}