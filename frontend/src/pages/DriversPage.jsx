import { useState } from "react";
import { useApi } from "../hooks/useApi";
import { api } from "../utils/api";
import TyreBadge from "../components/TyreBadge";
import WearBar from "../components/WearBar";

// Pomocná funkce v JS, která simuluje tvé bodování z Pythonu
const getPointsForPosition = (position) => {
  const pointsMap = {
    1: 50, 2: 45, 3: 40, 4: 35, 5: 30, 6: 25, 7: 22, 8: 20, 9: 18, 10: 15,
    11: 12, 12: 10, 13: 9, 14: 8, 15: 7, 16: 6, 17: 5, 18: 4, 19: 3, 20: 2,
    21: 1, 22: 1, 23: 1
  };
  return pointsMap[position] || 0;
};

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
          <div className="card-label">Current Championship Points</div>
          <div className="card-value" style={{ fontSize: 28 }}>
            {driver.points || 0}
          </div>
        </div>
        <div className="card">
          <div className="card-label">Projected Total Points</div>
          <div className="card-value" style={{ fontSize: 28, color: "var(--accent)" }}>
            {driver.newTotalPoints || driver.points || 0}
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
  const { data: globalDrivers, loading: driversLoading, error: driversError } = useApi(api.getDrivers);
  const { data: stateData } = useApi(api.getState); // Zde bereme position_history pro live výpočet
  const [expanded, setExpanded] = useState(null);

  let processedDrivers = [];

  if (globalDrivers) {
    // 1. Zjistíme aktuální seřazení v šampionátu před započtením rozjetého závodu
    const baseSorted = [...globalDrivers].sort((a, b) => (b.points || 0) - (a.points || 0));
    const currentRankMap = {};
    baseSorted.forEach((d, index) => {
      currentRankMap[d.name] = index + 1;
    });

    // 2. Propojíme globální data s daty z live závodu (podle position_history)
    processedDrivers = globalDrivers.map((driver) => {
      // Najdeme odpovídajícího jezdce v živém stavu závodu
      const liveDriver = stateData?.drivers?.find((ld) => ld.name === driver.name);
      
      let liveRacePos = driver.position || 99;
      if (liveDriver && liveDriver.position_history && liveDriver.position_history.length > 0) {
        // Vezmeme poslední známé kolo ze závodu
        liveRacePos = liveDriver.position_history[liveDriver.position_history.length - 1];
      }

      // Spočítáme body za tento závod a projektovaný nový součet
      const racePoints = getPointsForPosition(liveRacePos);
      const newTotalPoints = (driver.points || 0) + racePoints;

      return {
        ...driver,
        // Pokud má liveDriver čerstvější pneu a opotřebení ze simulace, ukážeme je
        pneu: liveDriver?.pneu || driver.pneu,
        wear: liveDriver?.wear !== undefined ? liveDriver.wear : driver.wear,
        dnf: liveDriver?.dnf !== undefined ? liveDriver.dnf : driver.dnf,
        history: liveDriver?.position_history || liveDriver?.lap_times || [],
        pit_stops: liveDriver?.pit_stops || [],
        
        currentRank: currentRankMap[driver.name] || 99,
        liveRacePosition: liveRacePos,
        newTotalPoints: newTotalPoints,
        earnedPoints: racePoints
      };
    });

    // 3. Seřadíme jezdce podle NOVÉHO celkového počtu bodů (Projektované pořadí)
    const newSorted = [...processedDrivers].sort((a, b) => b.newTotalPoints - a.newTotalPoints);
    processedDrivers = newSorted.map((d, index) => ({
      ...d,
      newRank: index + 1
    }));
  }

  return (
    <div>
      <div className="page-header">
        <div className="page-eyebrow">Driver Championship</div>
        <div className="page-title">
          DRIVER <span>LIVE PROJECTION</span>
        </div>
      </div>

      {driversLoading && <div className="loading">FETCHING DRIVERS</div>}
      {driversError && <div className="empty">⚠ {driversError}</div>}

      <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
        {processedDrivers.map((d, i) => {
          // Výpočet posunu v celkovém šampionátu
          const rankDiff = d.currentRank - d.newRank;
          let rankIndicator = "▬";
          let indicatorColor = "var(--text-3)";
          if (rankDiff > 0) {
            rankIndicator = `▲ +${rankDiff}`;
            indicatorColor = "#28a745";
          } else if (rankDiff < 0) {
            rankIndicator = `▼ ${rankDiff}`;
            indicatorColor = "#dc3545";
          }

          return (
            <div key={d.name}>
              <div
                onClick={() => setExpanded(expanded === d.name ? null : d.name)}
                style={{
                  display: "grid",
                  // Změněno mapování sloupců pro zachování zarovnání (odstraněno avg pos, přidáno live pos a rank indicator)
                  gridTemplateColumns: "50px 1fr 140px 100px 80px 140px",
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
                {/* Nová projektovaná pozice v šampionátu */}
                <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-start" }}>
                  <span
                    style={{
                      fontFamily: "var(--font-display)",
                      fontWeight: 700,
                      fontSize: 18,
                      color: i < 3 ? ["var(--yellow)", "#aaa", "#cd7f32"][i] : "var(--text-3)",
                      lineHeight: 1
                    }}
                  >
                    #{d.newRank}
                  </span>
                  <span style={{ fontSize: 9, fontFamily: "var(--font-mono)", color: indicatorColor, marginTop: 2 }}>
                    {rankIndicator}
                  </span>
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

                {/* NAHRAZENO: Live Position v aktuálním závodě */}
                <div
                  style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: 12,
                    color: "var(--text)",
                    textAlign: "center",
                    background: "var(--bg)",
                    border: "1px solid var(--border)",
                    padding: "4px 8px",
                    borderRadius: 4
                  }}
                >
                  RACE: <span style={{ fontWeight: 700, color: "var(--accent)" }}>P{d.liveRacePosition}</span>
                </div>

                {/* DNF / Status */}
                <div style={{ textAlign: "center" }}>
                  {d.dnf ? (
                    <span className="badge badge-err">DNF</span>
                  ) : (
                    <span className="badge badge-ok"></span>
                  )}
                </div>

                {/* Points projection */}
                <div style={{ textAlign: "right", fontFamily: "var(--font-mono)" }}>
                  <span className="points-pill">{d.newTotalPoints} PTS</span>
                  <div style={{ fontSize: 9, color: "var(--text-3)", marginTop: 2 }}>
                    was {d.points} (+{d.earnedPoints})
                  </div>
                </div>
              </div>

              {expanded === d.name && <DriverDetail driver={d} />}
            </div>
          );
        })}
      </div>
    </div>
  );
}