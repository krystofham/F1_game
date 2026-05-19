import { useState, useCallback, useRef, useEffect } from "react";
import { useApi } from "../hooks/useApi";
import { api } from "../utils/api";
import TyreBadge from "../components/TyreBadge";
import WearBar from "../components/WearBar";

// ── Init Race Form ──────────────────────────────────────────────────────────
function InitForm({ onInit }) {
  const [cfg, setCfg] = useState({
    lenght: 2,
    pneu_driver_1: "hard",
    pneu_driver_2: "hard",
    training_mode: 1,
    front_wing: 5,
    rear_wing: 5,
    brakes: 55,
    stabilizators: 1,
    springs: 1,
  });
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState(null);

  const set = (k, v) => setCfg((p) => ({ ...p, [k]: v }));

  const handleInit = async () => {
    setLoading(true);
    setErr(null);
    try {
      // Write init.json via the engine's endpoint (or proxy)
      // For now we call initRace directly; init.json must be pre-set
      const res = await api.initRace();
      onInit(res);
    } catch (e) {
      setErr(e.message);
    } finally {
      setLoading(false);
    }
  };

  const tyreOpts = ["soft", "medium", "hard", "wet", "inter"];

  return (
    <div className="card" style={{ maxWidth: 620 }}>
      <div style={{ fontFamily: "var(--font-display)", fontWeight: 700, fontSize: 18, letterSpacing: 2, marginBottom: 20, textTransform: "uppercase" }}>
        Race Configuration
      </div>

      <div className="grid-2" style={{ gap: 14, marginBottom: 14 }}>
        <div className="field">
          <label>Season Length</label>
          <input
            type="number"
            min={1} max={24}
            value={cfg.lenght}
            onChange={(e) => set("lenght", +e.target.value)}
          />
        </div>
        <div className="field">
          <label>Training Mode</label>
          <select value={cfg.training_mode} onChange={(e) => set("training_mode", +e.target.value)}>
            <option value={1}>1 — Debug / Full</option>
            <option value={2}>2 — Short</option>
            <option value={3}>3 — None</option>
          </select>
        </div>
        <div className="field">
          <label>Driver 1 Tyre</label>
          <select value={cfg.pneu_driver_1} onChange={(e) => set("pneu_driver_1", e.target.value)}>
            {tyreOpts.map((t) => <option key={t} value={t}>{t.toUpperCase()}</option>)}
          </select>
        </div>
        <div className="field">
          <label>Driver 2 Tyre</label>
          <select value={cfg.pneu_driver_2} onChange={(e) => set("pneu_driver_2", e.target.value)}>
            {tyreOpts.map((t) => <option key={t} value={t}>{t.toUpperCase()}</option>)}
          </select>
        </div>
      </div>

      <div
        style={{
          padding: "10px 14px",
          background: "var(--bg)",
          border: "1px solid var(--border)",
          marginBottom: 16,
          fontFamily: "var(--font-mono)",
          fontSize: 10,
          color: "var(--text-3)",
          letterSpacing: 1,
        }}
      >
        ⚠ FRONT_WING · REAR_WING · BRAKES · STABILIZATORS · SPRINGS — currently not active in engine
      </div>

      <div className="grid-3" style={{ gap: 12, marginBottom: 20 }}>
        {[
          { k: "front_wing", label: "Front Wing", min: 1, max: 11 },
          { k: "rear_wing", label: "Rear Wing", min: 1, max: 11 },
          { k: "brakes", label: "Brakes", min: 10, max: 100 },
          { k: "stabilizators", label: "Stabilizators", min: 1, max: 10 },
          { k: "springs", label: "Springs", min: 1, max: 10 },
        ].map(({ k, label, min, max }) => (
          <div key={k} className="field">
            <label>{label}</label>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <input
                type="range"
                min={min} max={max}
                value={cfg[k]}
                onChange={(e) => set(k, +e.target.value)}
                style={{ flex: 1, accentColor: "var(--accent)" }}
              />
              <span style={{ fontFamily: "var(--font-mono)", fontSize: 12, minWidth: 28 }}>
                {cfg[k]}
              </span>
            </div>
          </div>
        ))}
      </div>

      {err && (
        <div style={{ color: "var(--accent)", fontFamily: "var(--font-mono)", fontSize: 11, marginBottom: 12 }}>
          ✕ {err}
        </div>
      )}

      <button className="btn btn-primary" onClick={handleInit} disabled={loading}>
        {loading ? "INITIALIZING…" : "INIT RACE"}
      </button>
    </div>
  );
}

// ── Race live table ─────────────────────────────────────────────────────────
function RaceTable({ drivers }) {
  
  // Pomocná funkce pro získání aktuální pozice v závodě
  const getCurrentRacePos = (driver) => {
    if (driver.position_history && driver.position_history.length > 0) {
      // Vrátí poslední zapsanou pozici z historie závodu
      return driver.position_history[driver.position_history.length - 1];
    }
    // Pokud závod ještě nezačal a historie je prázdná, použijeme jako fallback pozici z kvalifikace/šampionátu
    return driver.position || 99;
  };

  // Seřadíme pole jezdců podle aktuálního pořadí v tomto závodě
  const sorted = [...(drivers || [])].sort((a, b) => {
    return getCurrentRacePos(a) - getCurrentRacePos(b);
  });

  return (
    <table className="data-table">
      <thead>
        <tr>
          <th>POS</th>
          <th>DRIVER</th>
          <th>TYRE</th>
          <th>WEAR</th>
          <th>GAP</th>
          <th>PITS</th>
          <th>STATUS</th>
        </tr>
      </thead>
      <tbody>
        {sorted.map((d) => {
          // Zjistíme přesné číslo pozice pro zobrazení v tabulce
          const currentPos = getCurrentRacePos(d);

          return (
            <tr key={d.name} className={d.dnf ? "dnf" : ""}>
              <td>
                <span style={{ fontFamily: "var(--font-display)", fontWeight: 700, fontSize: 16 }}>
                  P{currentPos}
                </span>
              </td>
              <td>
                <span style={{ fontFamily: "var(--font-display)", fontWeight: 700, color: d.is_player ? "var(--text)" : "var(--text-2)" }}>
                  {d.name}
                </span>
                {d.is_player && <span className="badge badge-ok" style={{ marginLeft: 6, fontSize: 7 }}>YOU</span>}
              </td>
              <td><TyreBadge type={d.pneu} /></td>
              <td style={{ minWidth: 120 }}><WearBar wear={d.wear || 0} /></td>
              <td className="text-mono">{d.gap != null ? `+${d.gap.toFixed(3)}` : "—"}</td>
              <td className="text-mono">{d.pit_stops?.length ?? 0}</td>
              <td>
                {d.dnf ? (
                  <span className="badge badge-err">DNF</span>
                ) : (
                  <span className="badge badge-ok">RACING</span>
                )}
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

// ── Main Race Page ──────────────────────────────────────────────────────────
export default function RacePage() {
  const [raceState, setRaceState] = useState(null); // null = not init
  const [lap, setLap] = useState(0);
  const [totalLaps, setTotalLaps] = useState(null);
  const [running, setRunning] = useState(false);
  const [finished, setFinished] = useState(false);
  const [postDone, setPostDone] = useState(false);
  const [log, setLog] = useState([]);
  const [drivers, setDrivers] = useState([]);
  const [simUntil, setSimUntil] = useState("");
  const logRef = useRef(null);
  const { data: state, refetch: refetchState } = useApi(api.getState);
  const isLastRace = state?.b != null && state?.championship_length != null
  ? state.b >= state.championship_length
  : false;

  useEffect(() => {
    if (state?.race_state) {
      setRaceState(state.race_state);
      setLap(state.lap ?? 0);
      setTotalLaps(state.race_state.total_laps);
    }
    if (state?.drivers) setDrivers(state.drivers);
  }, [state]);

  useEffect(() => {
    if (logRef.current) {
      logRef.current.scrollTop = logRef.current.scrollHeight;
    }
  }, [log]);

  const addLog = (msg, type = "") => {
    setLog((p) => [...p, { lap, msg, type, time: Date.now() }]);
  };

  const handleInit = async (res) => {
    setRaceState(res);
    setLap(res.lap ?? 0);
    setTotalLaps(res.total_laps);
    setFinished(false);
    setPostDone(false);
    setLog([]);
    addLog(`Race initialised: ${res.race}`, "good");
    await refetchState();
  };

  const doSimLap = useCallback(async () => {
    if (finished) return;
    try {
      const res = await api.simLap();
      setLap(res.lap);
      setTotalLaps(res.total_laps);
      addLog(`Lap ${res.lap - 1} complete`, "");
      await refetchState();
      if (res.finished) {
        setFinished(true);
        addLog("CHEQUERED FLAG 🏁", "good");
      }
      return res.finished;
    } catch (e) {
      addLog(`Error: ${e.message}`, "danger");
      return true;
    }
  }, [finished, lap]);

  const handleSimOne = async () => {
    setRunning(true);
    await doSimLap();
    setRunning(false);
  };

  const handleSimUntil = async () => {
    const target = parseInt(simUntil, 10);
    if (!target || target <= lap) return;
    setRunning(true);
    for (let i = lap; i < target && !finished; i++) {
      const done = await doSimLap();
      if (done) break;
      await new Promise((r) => setTimeout(r, 120));
    }
    setRunning(false);
  };

  const handleSimAll = async () => {
    setRunning(true);
    let done = false;
    while (!done) {
      done = await doSimLap();
      await new Promise((r) => setTimeout(r, 80));
    }
    setRunning(false);
  };

  const handlePostRace = async () => {
    try {
      const res = await api.postRace();
      addLog(`Post-race done: ${res.race}`, "good");
      setPostDone(true);
      await refetchState();
      const fresh = await api.getState();
      const last = fresh?.b >= fresh?.championship_length;
      setIsLastRace(last);
      addLog(`DEBUG b=${fresh?.b} len=${fresh?.championship_length} isLast=${last}`, "highlight");
    } catch (e) {
      addLog(`Post-race error: ${e.message}`, "danger");
    }
  };

  const handlePostChampionship = async () => {
    try {
      await api.postChampionship();
      addLog("Season ended. New season begun.", "highlight");
      setRaceState(null);
      setFinished(false);
      setPostDone(false);
      setLap(0);
      await refetchState();
    } catch (e) {
      addLog(`Championship error: ${e.message}`, "danger");
    }
  };

  const progress = totalLaps ? Math.min(100, (lap / totalLaps) * 100) : 0;

  return (
    <div>
      <div className="page-header">
        <div className="page-eyebrow">
          {raceState ? (state?.race || "Race") : "Race Control"}
        </div>
        <div className="page-title">
          RACE <span>CONTROL</span>
        </div>
      </div>

      {/* No race init yet */}
      {!raceState && <InitForm onInit={handleInit} />}

      {/* Race in progress / done */}
      {raceState && (
        <div>
          {/* Progress bar */}
          <div className="race-progress">
            <div className="race-progress-fill" style={{ width: `${progress}%` }} />
            <span className="race-progress-label">
              {lap}/{totalLaps ?? "?"} LAPS
            </span>
          </div>

          {/* Lap counter + controls */}
          <div className="flex items-center justify-between mb-6" style={{ marginBottom: 24, flexWrap: "wrap", gap: 16 }}>
            <div className="lap-counter">
              <span className="lap-num">{lap}</span>
              <span className="lap-sep">/</span>
              <span className="lap-total">{totalLaps ?? "?"}</span>
              <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-3)", marginLeft: 12, letterSpacing: 2 }}>LAPS</span>
            </div>

            <div className="flex" style={{ gap: 10, alignItems: "center", flexWrap: "wrap" }}>
              {!finished && (
                <>
                  <button
                    className="btn btn-primary"
                    onClick={handleSimOne}
                    disabled={running}
                  >
                    {running ? "SIMMING…" : "SIM LAP"}
                  </button>

                  <div className="flex items-center" style={{ gap: 6 }}>
                    <div className="field" style={{ gap: 0 }}>
                      <input
                        type="number"
                        placeholder="Until lap…"
                        value={simUntil}
                        onChange={(e) => setSimUntil(e.target.value)}
                        style={{ width: 100 }}
                        min={lap + 1}
                        max={totalLaps}
                      />
                    </div>
                    <button className="btn" onClick={handleSimUntil} disabled={running || !simUntil}>
                      SIM TO
                    </button>
                  </div>

                  <button
                    className="btn"
                    onClick={handleSimAll}
                    disabled={running}
                  >
                    SIM ALL
                  </button>
                </>
              )}

              { (
                <button className="btn btn-success" onClick={handlePostRace}>
                  POST RACE
                </button>
              )}

              { (
                <button className="btn btn-primary" onClick={() => setRaceState(null)}>
                  NEXT RACE
                </button>
              )}

              {(
                <button className="btn btn-danger" onClick={handlePostChampionship}>
                  END SEASON
                </button>
              )}

              {postDone && !isLastRace && (
                <button className="btn btn-primary" onClick={() => setRaceState(null)}>
                  RECONFIGURE
                </button>
              )}
            </div>
          </div>

          <div className="grid-2" style={{ gap: 24, alignItems: "start" }}>
            {/* Race table */}
            <div>
              <div className="section-title" style={{ marginTop: 0 }}>Live Positions</div>
              <RaceTable drivers={drivers} />
            </div>

            {/* Log */}
            <div>
              <div className="section-title" style={{ marginTop: 0 }}>Race Log</div>
              <div className="race-log" ref={logRef}>
                {log.length === 0 && (
                  <span style={{ color: "var(--text-3)" }}>Waiting for race events…</span>
                )}
                {log.map((entry, i) => (
                  <div key={i} className="log-entry">
                    <span className="log-lap">LAP {String(entry.lap).padStart(2, "0")}</span>
                    <span className={`log-msg ${entry.type}`}>{entry.msg}</span>
                  </div>
                ))}
              </div>

              {/* Re-init option */}
              <div style={{ marginTop: 12 }}>
                <button
                  className="btn"
                  style={{ fontSize: 10, letterSpacing: 1, padding: "7px 14px" }}
                  onClick={() => setRaceState(null)}
                >
                  ↺ RECONFIGURE RACE
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
