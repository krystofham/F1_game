import { useApi } from "../hooks/useApi";
import { api } from "../utils/api";

const COUNTRY_FLAGS = {};

function guessFlag(name) {
  const lower = (name || "").toLowerCase();
  for (const [key, flag] of Object.entries(COUNTRY_FLAGS)) {
    if (lower.includes(key)) return flag;
  }
  return "";
}

function StatBlock({ label, value, unit, importance }) {
  return (
    <div className="card" style={importance ? { borderColor: "red" } : {}}>      
      <div className="card-label">{label}</div>
      <div className="card-value" style={{ fontSize: 26 }}>
        {value ?? "—"}
        {unit && <span style={{ fontSize: 14, color: "var(--text-2)", marginLeft: 6 }}>{unit}</span>}
      </div>
    </div>
  );
}

export default function TrackPage({ state }) {
  const { data: tracks, loading: tracksLoading, error: tracksError } = useApi(api.getTracks);

  if (!state || tracksLoading) return <div className="loading">LOADING TRACK</div>;
  if (tracksError) return <div className="empty">⚠ {tracksError}</div>;
  // 1. Všechny hooky na absolutním topu komponenty

  // 2. Loading a Error stavy až ZA hooky
  // if (loading) return <div className="loading">LOADING TRACK</div>;
  // if (error) return <div className="empty">⚠ {error}</div>;

  // 3. Bezpečné vytažení aktuálního jména závodu ze state
  const race = state?.race;
  const championship = state?.championship || [];
  const b = state?.b ?? 1;
  const rawTrack = championship[b - 1];
  
  // Zde získáme čistý string jména (podpora pro objekty i raw stringy)
  const currentTrackName = typeof rawTrack === "string" ? rawTrack : rawTrack?.name || race || "";

  // 4. Porovnání jména s polem z tracks.json (api.getTracks)
  const trackDetails = tracks?.find(t => t.name === currentTrackName) || {};

  // 5. Výpočty pravděpodobností z nalezeného okruhu
  const scProb = trackDetails.sc_prob || 5000; 
  const totalLaps = trackDetails.laps ?? state?.race_state?.total_laps ?? 0;
  const dnfProb = 100 * 28 * totalLaps / scProb;

  // Bezpečný stav pro safety car bez globálních mutací
  const isSafetyCarOut = state?.race_state?.safety_car !== false;

  const flag = guessFlag(currentTrackName);

  return (
    <div>
      <div className="page-header">
        <div className="page-eyebrow">
          Race {b} of {state.championship_length || "?"}
        </div>
        <div className="page-title">
          <span style={{ fontSize: 56, marginRight: 12 }}>{flag}</span>
          <span>{currentTrackName.toUpperCase() || "CIRCUIT"}</span>
        </div>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 14, marginBottom: 24 }}>
        <StatBlock
          label="Safety car"
          value={isSafetyCarOut ? "Safety car IS OUT" : "Safety car is not on track"}
          importance={isSafetyCarOut}        
        />
        {isSafetyCarOut && (
          <StatBlock
            label="Safety car laps remaining"
            value={state?.race_state?.safety_car_laps_remaining ?? "Error"}
            importance={true}
          />
        )}
        <StatBlock
          label="Weather"
          value={state?.race_state?.weather || "Error"}
          importance={state?.race_state?.weather !== "sunny"}
        />
        <StatBlock
          label="Wettiness of track"
          value={state?.race_state?.wettiness ?? "Error"}
          importance={state?.race_state?.wettiness > 0}        
          unit={"%"}
        />
        <StatBlock
          label="DNF Risk"
          value={dnfProb ? dnfProb.toFixed(1) : "Error"}
          unit="%"
        />
        <StatBlock
          label="Season"
          value={state?.season_count || "Error"}
        />
        <StatBlock
          label="Clima"
          value={state?.race_state?.climax || "Error"}
        />

        <StatBlock label="Laps" value={totalLaps} />
      </div>

      {/* Profil směsí se nyní renderuje na základě spárovaných detailů z tracks.json */}
      {(trackDetails.pneu_types || trackDetails.speed_types) && (
        <div>
          <div className="section-title">Compound Profile</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
            <div className="card">
              <div className="card-label" style={{ marginBottom: 10 }}>Tyre Compounds</div>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                {(trackDetails.pneu_types || ["soft", "medium", "hard"]).map((t) => (
                  <div
                    key={t}
                    className={`tyre ${t}`}
                    style={{ width: 36, height: 36, fontSize: 13 }}
                    title={t}
                  >
                    {t[0].toUpperCase()}
                  </div>
                ))}
              </div>
            </div>
            <div className="card">
              <div className="card-label" style={{ marginBottom: 10 }}>Speed / Wear Profile</div>
              <div style={{ fontFamily: "var(--font-mono)", fontSize: 12, lineHeight: 2, color: "var(--text-2)" }}>
                {["hard", "medium", "soft", "wet", "inter"].map((t, i) => {
                  const wear = state?.race_state?.k_wear?.[i];
                  const speed = state?.race_state?.k_speed?.[i];
                  if (wear == null && speed == null) return null;
                  return (
                    <div key={t} style={{ display: "flex", gap: 12 }}>
                      <span style={{ minWidth: 60, color: "var(--text-3)" }}>{t.toUpperCase()}</span>
                      {wear != null && <span>WEAR ×{wear.toFixed(3)}</span>}
                      {speed != null && <span>SPD ×{speed.toFixed(3)}</span>}
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}

      {championship.length > 0 && (
        <div>
          <div className="section-title">Season Calendar</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 3 }}>
            {championship.map((raceItem, i) => {
              const name = typeof raceItem === "string" ? raceItem : raceItem?.name ?? `Race ${i + 1}`;
              const isCurrent = i + 1 === b;
              const isDone = i + 1 < b;
              return (
                <div
                  key={i}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 16,
                    padding: "10px 14px",
                    background: isCurrent ? "rgba(232,0,45,0.06)" : "var(--bg-card)",
                    border: "1px solid",
                    borderColor: isCurrent ? "var(--accent)" : "var(--border)",
                    opacity: isDone ? 0.45 : 1,
                  }}
                >
                  <span style={{ fontFamily: "var(--font-display)", fontWeight: 700, fontSize: 18, color: "var(--text-3)", minWidth: 32 }}>
                    {String(i + 1).padStart(2, "0")}
                  </span>
                  <span style={{ fontSize: 20 }}>{guessFlag(name)}</span>
                  <span style={{ fontFamily: "var(--font-display)", fontWeight: isCurrent ? 700 : 400, fontSize: 14, flex: 1 }}>
                    {name}
                  </span>
                  {isCurrent && <span className="badge badge-warn">CURRENT</span>}
                  {isDone && <span className="badge badge-neutral">DONE</span>}
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}