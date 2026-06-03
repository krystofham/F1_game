import { useState, useCallback, useRef, useEffect, useMemo } from "react";
import { useApi } from "../hooks/useApi";
import { api } from "../utils/api";
import TyreBadge from "../components/TyreBadge";
import WearBar from "../components/WearBar";

const TYRE_OPTS = ["soft", "medium", "hard", "wet", "inter"];

function PitForm({ drivers, onSubmit, disabled }) {
  const playerDrivers = useMemo(
    () => (drivers || []).filter((d) => d.is_player).sort((a, b) => a.name.localeCompare(b.name)),
    []
  );

  const buildDefault = (list) => {
    const init = {};
    list.forEach((d) => {
      init[d.name] = { action: "1", new_pneu: "medium" };
    });
    return init;
  };

  const [actions, setActions] = useState(() => buildDefault(playerDrivers));

  const setField = (name, field, value) =>
    setActions((prev) => ({ ...prev, [name]: { ...prev[name], [field]: value } }));

  const handleSubmit = () => {
      const payload = { commands: [] };
      playerDrivers.forEach((d) => {
          payload[d.name] = actions[d.name] ?? { action: "1", new_pneu: "medium" };
      });
      onSubmit(payload);
      setActions(buildDefault(playerDrivers));
  };

  if (playerDrivers.length === 0) return null;

  return (
    <div className="card" style={{ marginBottom: 24 }}>
      <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
        {playerDrivers.map((d) => {
          const act = actions[d.name] ?? { action: "1", new_pneu: "medium" };
          const isPit = act.action === "2";

          return (
            <div key={d.name} style={{
              flex: "1 1 200px",
              padding: "12px 14px",
              border: `1px solid ${isPit ? "var(--accent)" : "var(--border)"}`,
              background: isPit ? "color-mix(in srgb, var(--accent) 8%, transparent)" : "var(--bg)",
              transition: "border-color .2s, background .2s",
            }}>
              <div style={{ fontFamily: "var(--font-display)", fontWeight: 700, fontSize: 13, marginBottom: 10, display: "flex", alignItems: "center", gap: 8 }}>
                {d.name}
                {isPit && <span className="badge badge-err" style={{ fontSize: 7 }}>PIT</span>}
              </div>

              <div style={{ display: "flex", gap: 6, marginBottom: 10 }}>
                {[{ val: "1", label: "CONTINUE" }, { val: "2", label: "PIT STOP" }].map(({ val, label }) => (
                  <button
                    key={val}
                    className={`btn${act.action === val ? " btn-primary" : ""}`}
                    style={{ flex: 1, fontSize: 10, padding: "6px 0" }}
                    onClick={() => setField(d.name, "action", val)}
                    disabled={disabled}
                  >
                    {label}
                  </button>
                ))}
              </div>

              <div className="field" style={{ opacity: isPit ? 1 : 0.3, pointerEvents: isPit ? "auto" : "none" }}>
                <label style={{ fontSize: 9 }}>New Tyre</label>
                <select
                  value={act.new_pneu}
                  onChange={(e) => setField(d.name, "new_pneu", e.target.value)}
                  disabled={disabled || !isPit}
                >
                  {TYRE_OPTS.map((t) => <option key={t} value={t}>{t.toUpperCase()}</option>)}
                </select>
              </div>
            </div>
          );
        })}
      </div>

      <button
        className="btn btn-success"
        style={{ marginTop: 14, fontSize: 11, letterSpacing: 2 }}
        onClick={handleSubmit}
        disabled={disabled}
      >
        CONFIRM INSTRUCTIONS
      </button>
    </div>
  );
}

function InitForm({ onInit }) {
  const [cfg, setCfg] = useState({
    length: 2,
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
      await api.setInitConfig({
        pneu_driver_1: cfg.pneu_driver_1,
        pneu_driver_2: cfg.pneu_driver_2,
        training_mode: cfg.training_mode,
      });
      const res = await api.initRace();
      onInit(res);  // předá jen výsledek initRace, config už je uložen
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
            value={cfg.length}
            onChange={(e) => set("length", +e.target.value)}
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

      <div style={{
        padding: "10px 14px",
        background: "var(--bg)",
        border: "1px solid var(--border)",
        marginBottom: 16,
        fontFamily: "var(--font-mono)",
        fontSize: 10,
        color: "var(--text-3)",
        letterSpacing: 1,
      }}>
        FRONT_WING · REAR_WING · BRAKES · STABILIZATORS · SPRINGS — currently not active in engine
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
          {err}
        </div>
      )}

      <button className="btn btn-primary" onClick={handleInit} disabled={loading}>
        {loading ? "INITIALIZING" : "INIT RACE"}
      </button>
    </div>
  );
}

function RaceTable({ drivers }) {
  const getCurrentRacePos = (driver) => {
    if (driver.position_history && driver.position_history.length > 0) {
      return driver.position_history[driver.position_history.length - 1];
    }
    return driver.position || 99;
  };

  const playerDrivers = (drivers || []).filter(d => d.is_player);
  const otherDrivers = (drivers || []).filter(d => !d.is_player);

  const sortedPlayers = [...playerDrivers].sort((a, b) => getCurrentRacePos(a) - getCurrentRacePos(b));
  const sortedOthers = [...otherDrivers].sort((a, b) => getCurrentRacePos(a) - getCurrentRacePos(b));
  const sorted = [...sortedPlayers, ...sortedOthers];

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
        </tr>
      </thead>
      <tbody>
        {sorted.map((d, index) => {
          const currentPos = getCurrentRacePos(d);

          let gapDisplay = "—";

          if (index > 0) {
            const previousDriver = sorted[index - 1];
            if (d.time != null && previousDriver.time != null) {
              const gap = d.time - previousDriver.time;
              gapDisplay = `+${Math.max(0, gap).toFixed(3)}`;
            }
          }

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
                {d.drs && <span className="badge badge" style={{ marginLeft: 6, fontSize: 7, borderColor: "var(--green)", color: "var(--green)"}}>DRS open</span>}
              </td>
              <td><TyreBadge type={d.pneu} /></td>
              <td style={{ minWidth: 120 }}><WearBar wear={d.wear || 0} /></td>
              <td className="text-mono">{gapDisplay}</td>
              <td className="text-mono">{d.pit_stops}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

const simEverything = (deps) => {
  const { finished, raceState, postDone, running, isLastRace, api, addLog, setPostDone, refetchState, setRaceState, setLap, setTotalLaps, handleInit } = deps;
  return // comment this for production !! 
  if (!finished || !raceState || postDone || running) return;

  const run = async () => {
    try {
      const res = await api.postRace();
      addLog(`Post-race done: ${res.race}`, "good");
      setPostDone(true);
      await refetchState();

      if (isLastRace) {
        await api.postChampionship();
        addLog("Season ended. New season begun.", "highlight");
        setRaceState(null);
        setPostDone(false);
        setLap(0);
        setTotalLaps(null);
        await refetchState();
      } else {
        const next = await api.initRace();
        await handleInit(next);
      }
    } catch (e) {
      addLog(`Auto post-race error: ${e.message}`, "danger");
    }
  };

  run();
};

export default function RacePage() {
  const [raceState, setRaceState] = useState(null);
  const [lap, setLap] = useState(0);
  const [totalLaps, setTotalLaps] = useState(null);
  const [running, setRunning] = useState(false);
  const [postDone, setPostDone] = useState(false);
  const [log, setLog] = useState([]);
  const [drivers, setDrivers] = useState([]);
  const [simUntil, setSimUntil] = useState("");
  const [pitSaved, setPitSaved] = useState(false);
  const logRef = useRef(null);
  const { data: state, refetch: refetchState } = useApi(api.getState);
  const isLastRace = state?.b != null && state?.championship_length != null
    ? state.b >= state.championship_length
    : false;

  const finished = !!totalLaps && lap >= totalLaps;

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

  const handlePitSubmit = async (payload) => {
      try {
          await api.setLapUserData(payload);
          setPitSaved(true);
          addLog(
              `Instructions: ${Object.entries(payload)
                  .filter(([k]) => k !== "commands")
                  .map(([k, v]) => `${k} -> ${v.action === "2" ? "PIT (" + v.new_pneu + ")" : "GO"}`)
                  .join(" | ")}`,
              "good"
          );
      } catch (e) {
          addLog(`Pit instruction error: ${e.message}`, "danger");
      }
  };

  const handleInit = async (res) => {
    setRaceState(res);
    setLap(res.lap ?? 0);
    setTotalLaps(res.total_laps);
    setPostDone(false);
    setLog([]);
    setPitSaved(false);
    addLog(`Race initialised: ${res.race}`, "good");
    await refetchState();
  };

  const doSimLap = useCallback(async () => {
    if (finished) return;
    setPitSaved(false);
    try {
      const res = await api.simLap();
      setLap(res.lap);
      setTotalLaps(res.total_laps);
      addLog(`Lap ${res.lap - 1} complete`, "");
      await refetchState();
      if (res.lap >= res.total_laps) {
        addLog("CHEQUERED FLAG", "good");
      }
      return res.lap >= res.total_laps;
    } catch (e) {
      addLog(`Error: ${e.message}`, "danger");
      return true;
    }
  }, [finished, lap, totalLaps]);

  const handleSimOne = async () => {
    setRunning(true);
    await doSimLap();
    setRunning(false);
  };

  const playSnapshots = async (snapshots, delayMs = 0) => {
      for (const snap of snapshots) {
          setLap(snap.lap);
          setDrivers(snap.drivers);
          await new Promise((r) => setTimeout(r, delayMs));
      }
  };

  const handleSimAll = async () => {
      setRunning(true);
      try {
          const res = await api.simRace();          // 1 request místo 70
          await playSnapshots(res.snapshots);        // animace lokálně
          setLap(res.final_state.lap);
          setDrivers(res.final_state.drivers ?? []);
          addLog("CHEQUERED FLAG", "good");
          await refetchState();
      } catch (e) {
          addLog(`Error: ${e.message}`, "danger");
      }
      setRunning(false);
  };

  const handleSimUntil = async () => {
      const target = parseInt(simUntil, 10);
      if (!target || target <= lap) return;
      setRunning(true);
      try {
          const res = await api.simUntil(target);  // nový call
          await playSnapshots(res.snapshots);
          setLap(res.lap);
          setDrivers(res.final_state.drivers ?? []);
          await refetchState();
      } catch (e) {
          addLog(`Error: ${e.message}`, "danger");
      }
      setRunning(false);
  };

  const handlePostRace = async () => {
    try {
      const res = await api.postRace();
      addLog(`Post-race done: ${res.race}`, "good");
      setPostDone(true);
      await refetchState();
    } catch (e) {
      addLog(`Post-race error: ${e.message}`, "danger");
    }
  };

  const handlePostChampionship = async () => {
    try {
      await api.postChampionship();
      addLog("Season ended. New season begun.", "highlight");
      setRaceState(null);
      setPostDone(false);
      setLap(0);
      setTotalLaps(null);
      await refetchState();
    } catch (e) {
      addLog(`Championship error: ${e.message}`, "danger");
    }
  };

  const progress = totalLaps ? Math.min(100, (lap / totalLaps) * 100) : 0;
  const [showTrack, setShowTrack] = useState(true);
  const deps = { finished, raceState, postDone, running, isLastRace, api, addLog, setPostDone, refetchState, setRaceState, setLap, setTotalLaps, handleInit };
  useEffect(() => simEverything(deps), [finished, raceState, postDone, isLastRace, running]);  return (
    <div>
      <div className="page-header">
        <div className="page-eyebrow">
          {raceState ? (state?.race || "Race") : "Race Control"}
        </div>
        <div className="page-title">
          RACE CONTROL
        </div>
      </div>

      {!raceState && <InitForm onInit={handleInit} />}

      {raceState && (
        <div>
          <div className="race-progress">
            <div className="race-progress-fill" style={{ width: `${progress}%` }} />
            <span className="race-progress-label">
              {lap}/{totalLaps ?? "?"} LAPS
            </span>
          </div>

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
                  <button className="btn btn-primary" onClick={handleSimOne} disabled={running}>
                    {running ? "SIMMING" : "SIM LAP"}
                  </button>

                  <div className="flex items-center" style={{ gap: 6 }}>
                    <div className="field" style={{ gap: 0 }}>
                      <input
                        type="number"
                        placeholder="Until lap"
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

                  <button className="btn" onClick={handleSimAll} disabled={running}>
                    SIM ALL
                  </button>
                </>
              )}
              {finished && (
                <>
                  <button className="btn btn-success" onClick={handlePostRace} disabled={postDone}>
                    {postDone ? "DONE" : "POST RACE"}
                  </button>

                  <button className="btn btn-danger" onClick={handlePostChampionship}>
                    END SEASON
                  </button>
                </>
              )}
              {postDone && !isLastRace && (
                <button className="btn btn-primary" onClick={() => setRaceState(null)}>
                  RECONFIGURE
                </button>
              )}
            </div>
          </div>

          {!finished && (
            <>
              <PitForm
                drivers={drivers}
                onSubmit={handlePitSubmit}
                disabled={running}
              />
              {pitSaved && (
                <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--accent)", marginBottom: 12, letterSpacing: 1 }}>
                  Instructions saved — will apply on next sim lap
                </div>
              )}
            </>
          )}

          <div className="grid" style={{ gap: 24, alignItems: "start" }}>
            <div>
              <div className="section-title" style={{ marginTop: 0 }}>Live Positions</div>
              <RaceTable drivers={drivers} />
              <div style={{"margin": "10px"}}>
                <button
                  className="btn"
                  style={{ fontSize: 10, letterSpacing: 1, padding: "7px 14px" }}
                  onClick={() => setRaceState(null)}
                >
                  RECONFIGURE RACE
                </button>
              </div>
            </div>
            <button
              className="btn"
              style={{
                position: "fixed",
                bottom: showTrack ? 432 : 24,
                right: 24,
                zIndex: 101,
                fontSize: 10,
                letterSpacing: 1,
                padding: "6px 12px",
                transition: "bottom .2s",
              }}
              onClick={() => setShowTrack(p => !p)}
            >
              {showTrack ? "HIDE TRACK" : "SHOW TRACK"}
            </button>

            {showTrack && (
              <iframe
                src={`http://localhost:3001/iframe_track?lap=${lap}`}
                title="Track stats"
                style={{
                  position: "fixed",
                  bottom: 24,
                  right: 24,
                  width: 600,
                  height: 400,
                  border: "1px solid var(--border)",
                  zIndex: 100,
                }}
              />
            )}

          </div>
        </div>
      )}
    </div>
  );
}