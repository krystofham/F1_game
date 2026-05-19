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

function TeamCard({ team, currentRank, newRank }) {
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
            #{String(newRank).padStart(2, "0")}
          </div>
          <div style={{ fontSize: 10, fontFamily: "var(--font-mono)", color: indicatorColor, fontWeight: 700 }}>
            {rankIndicator}
          </div>
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

        <div className="team-name" style={{ fontSize: 13, marginBottom: 2, pr: 60 }}>
          {team.name}
        </div>
        <div className="team-pts">
          {team.points || 0} PTS 
          <span style={{ fontSize: 11, color: "var(--text-3)", marginLeft: 6 }}>
            (+{team.simulatedRacePoints || 0} fresh)
          </span>
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
  const { data: stateData } = useApi(api.getState); // Potřebujeme pro získání position_history řidičů

  let teams = [];

  if (teamsData) {
    // 1. Nejprve seřadíme týmy podle aktuálních bodů, abychom znali jejich STÁRE/AKTUÁLNÍ pořadí (Rank)
    const currentSortedTeams = [...teamsData].sort((a, b) => (b.points || 0) - (a.points || 0));
    
    // Vytvoříme mapu původního pořadí podle jména týmu
    const currentRankMap = {};
    currentSortedTeams.forEach((t, index) => {
      currentRankMap[t.name] = index + 1;
    });

    // 2. Extrahujeme aktuální pozice jezdců ze state.json z posledního kola závodu
    const driverRacePositions = {};
    if (stateData && stateData.drivers) {
      stateData.drivers.forEach((d) => {
        if (d.position_history && d.position_history.length > 0) {
          // Vezmeme poslední prvek z pole historie = pozice v cíli / aktuálním kole
          driverRacePositions[d.name] = d.position_history[d.position_history.length - 1];
        } else {
          // Fallback, pokud závod ještě vůbec neodstartoval
          driverRacePositions[d.name] = d.position || 99;
        }
      });
    }

    // 3. Nasimulujeme přičtení bodů jednotlivým týmům v JS
    const simulatedTeams = teamsData.map((team) => {
      let racePointsForTeam = 0;

      // Projdeme oba jezdce daného týmu
      (team.drivers || []).forEach((driverName) => {
        const finalPosition = driverRacePositions[driverName];
        if (finalPosition) {
          racePointsForTeam += getPointsForPosition(finalPosition);
        }
      });

      return {
        ...team,
        currentRank: currentRankMap[team.name] || 99,
        // Nové celkové body = staré body + nově získané body ze simulace
        newTotalPoints: (team.points || 0) + racePointsForTeam,
        simulatedRacePoints: racePointsForTeam // abychom mohli v UI ukázat, kolik bodů získali v závodě
      };
    });

    // 4. Seřadíme týmy znovu podle NOVÝCH nasimulovaných celkových bodů
    const newSortedTeams = [...simulatedTeams].sort((a, b) => b.newTotalPoints - a.newTotalPoints);

    // Přiřadíme do objektů jejich finální nové pořadí (New Rank)
    teams = newSortedTeams.map((team, index) => ({
      ...team,
      newRank: index + 1
    }));
  }

  // Chceme stránku primárně zobrazovat seřazenou podle NOVÉHO pořadí po tomto závodě
  // Pokud chceš zachovat staré řazení, změň na: .sort((a, b) => a.currentRank - b.currentRank)
  const displayedTeams = [...teams].sort((a, b) => a.newRank - b.newRank);

  return (
    <div>
      <div className="page-header">
        <div className="page-eyebrow">Constructor Championship</div>
        <div className="page-title">
          TEAM <span>OVERVIEW</span>
        </div>
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
            />
          ))}
        </div>
      )}
    </div>
  );
}