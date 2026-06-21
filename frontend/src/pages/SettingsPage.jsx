import { useState, useEffect } from "react";
import { api } from "../utils/api";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function Section({ title, children }) {
  return (
    <div style={{ marginBottom: 40 }}>
      <div style={{
        fontFamily: "var(--font-display)",
        fontWeight: 700,
        fontSize: 10,
        letterSpacing: 3,
        color: "var(--text-3)",
        textTransform: "uppercase",
        marginBottom: 16,
        paddingBottom: 8,
        borderBottom: "1px solid var(--border)",
      }}>
        {title}
      </div>
      {children}
    </div>
  );
}

function Field({ label, hint, children }) {
  return (
    <div style={{ marginBottom: 16 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 6 }}>
        <label style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-2)", letterSpacing: 1 }}>
          {label}
        </label>
        {hint && (
          <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-3)" }}>{hint}</span>
        )}
      </div>
      {children}
    </div>
  );
}

function Toast({ msg, type }) {
  if (!msg) return null;
  return (
    <div style={{
      position: "fixed", bottom: 32, left: "50%", transform: "translateX(-50%)",
      background: type === "err" ? "var(--accent)" : "var(--green, #22c55e)",
      color: "#000",
      fontFamily: "var(--font-mono)",
      fontSize: 11,
      letterSpacing: 2,
      padding: "10px 24px",
      zIndex: 999,
      pointerEvents: "none",
    }}>
      {msg}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Colour tokens the user can tweak
// ---------------------------------------------------------------------------
const DEFAULT_COLORS = {
  "--accent":  "#8ecae6",
  "--bg":      "#0D1B2A",
  "--bg-2":    "#1B263B",
  "--border":  "#48bfe38f",
  "--text":    "#f0f0f8",
  "--text-2":  "#bdbdd1",
  "--text-3":  "#a1a1b3",
};

const COLOR_LABELS = {
  "--accent":  "Accent",
  "--bg":      "Background",
  "--bg-2":    "Card background",
  "--border":  "Border",
  "--text":    "Primary text",
  "--text-2":  "Secondary text",
  "--text-3":  "Muted text",
};

function readCSSVar(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

function setCSSVar(name, value) {
  document.documentElement.style.setProperty(name, value);
}

// ---------------------------------------------------------------------------
// Main page
// ---------------------------------------------------------------------------
export default function SettingsPage() {
  const [state, setState] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [toast, setToast] = useState(null);

  // Editable copies
  const [drivers, setDrivers] = useState([]);
  const [teams, setTeams]     = useState([]);
  const [colors, setColors]   = useState({});
  const [apiUrl, setApiUrl]   = useState("http://localhost:8000");
  const [stopOnEvent, setStopOnEvent] = useState(true);
  const [showLogs, setShowLogs]       = useState(false);

  // Load state
  useEffect(() => {
    api.getState().then((s) => {
      setState(s);
      setDrivers((s.drivers || []).map((d) => ({ ...d })));
      setTeams((s.teams || []).map((t) => ({ ...t })));
      setLoading(false);
    }).catch(() => setLoading(false));

    // Load colours from CSS vars
    const current = {};
    Object.keys(DEFAULT_COLORS).forEach((k) => {
      current[k] = readCSSVar(k) || DEFAULT_COLORS[k];
    });
    setColors(current);

    // Load persisted settings
    try {
      const saved = JSON.parse(localStorage.getItem("mmr_settings") || "{}");
      if (saved.apiUrl) setApiUrl(saved.apiUrl);
      if (saved.stopOnEvent !== undefined) setStopOnEvent(saved.stopOnEvent);
      if (saved.showLogs !== undefined) setShowLogs(saved.showLogs);
      if (saved.colors) {
        Object.entries(saved.colors).forEach(([k, v]) => setCSSVar(k, v));
        setColors((p) => ({ ...p, ...saved.colors }));
      }
    } catch {}
  }, []);

  const showToast = (msg, type = "ok") => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 2500);
  };

  // Apply colour change live
  const handleColorChange = (key, val) => {
    setColors((p) => ({ ...p, [key]: val }));
    setCSSVar(key, val);
  };

  const resetColors = () => {
    Object.entries(DEFAULT_COLORS).forEach(([k, v]) => {
      setCSSVar(k, v);
    });
    setColors({ ...DEFAULT_COLORS });
  };

  // Save everything
  const handleSave = async () => {
    setSaving(true);
    try {
      await fetch("http://localhost:8000/api/patch_state", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ drivers, teams }),
      });
      await fetch("http://localhost:8000/api/settings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ stop_on_event: stopOnEvent, show_logs: showLogs }),
      });
      localStorage.setItem("mmr_settings", JSON.stringify({ apiUrl, stopOnEvent, showLogs, colors }));
      showToast("SETTINGS SAVED");
    } catch (e) {
      showToast("SAVE FAILED", "err");
    } finally {
      setSaving(false);
    }
  };

  const playerDrivers = drivers.filter((d) => d.is_player);
  const aiDrivers     = drivers.filter((d) => !d.is_player);

  if (loading) return (
    <div style={{ padding: 40, fontFamily: "var(--font-mono)", color: "var(--text-3)", fontSize: 11 }}>
      LOADING...
    </div>
  );

  return (
    <div style={{ maxWidth: 1020, padding: "0 0 80px 0" }}>
      <div className="page-header">
        <div className="page-eyebrow">CONFIGURATION</div>
        <div className="page-title">SETTINGS</div>
      </div>

      {/* ── APPEARANCE ── */}
      <Section title="Appearance">
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
          {Object.entries(COLOR_LABELS).map(([key, label]) => (
            <Field key={key} label={label} hint={colors[key]}>
              <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                <input
                  type="color"
                  value={colors[key] || DEFAULT_COLORS[key]}
                  onChange={(e) => handleColorChange(key, e.target.value)}
                  style={{ width: 36, height: 28, border: "1px solid var(--border)", background: "none", cursor: "pointer", padding: 2 }}
                />
                <input
                  type="text"
                  value={colors[key] || ""}
                  onChange={(e) => handleColorChange(key, e.target.value)}
                  style={{ flex: 1, fontFamily: "var(--font-mono)", fontSize: 11 }}
                />
              </div>
            </Field>
          ))}
        </div>
        <button className="btn" style={{ fontSize: 10, marginTop: 8 }} onClick={resetColors}>
          RESET TO DEFAULT
        </button>
      </Section>

      {/* ── HARDCORE / ENGINE ── */}
      <Section title="Engine">
        <Field label="FastAPI server URL" hint="restart required">
          <input
            type="text"
            value={apiUrl}
            onChange={(e) => setApiUrl(e.target.value)}
            style={{ width: "100%", fontFamily: "var(--font-mono)", fontSize: 11 }}
          />
        </Field>

        <Field label="Stop simulation when event occurs">
          <div style={{ display: "flex", gap: 8, marginTop: 4 }}>
            {[true, false].map((v) => (
              <button
                key={String(v)}
                className={`btn${stopOnEvent === v ? " btn-primary" : ""}`}
                style={{ fontSize: 10, padding: "6px 16px" }}
                onClick={() => setStopOnEvent(v)}
              >
                {v ? "ON" : "OFF"}
              </button>
            ))}
          </div>
        </Field>

        <Field label="Show debug logs in console">
          <div style={{ display: "flex", gap: 8, marginTop: 4 }}>
            {[true, false].map((v) => (
              <button
                key={String(v)}
                className={`btn${showLogs === v ? " btn-primary" : ""}`}
                style={{ fontSize: 10, padding: "6px 16px" }}
                onClick={() => setShowLogs(v)}
              >
                {v ? "ON" : "OFF"}
              </button>
            ))}
          </div>
        </Field>
      </Section>

      {/* ── YOUR DRIVERS ── */}
      <Section title="Your Drivers">
        {playerDrivers.length === 0 && (
          <div style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-3)" }}>
            No player drivers found. Start a race first.
          </div>
        )}
      {playerDrivers.map((d) => {
        const globalIdx = drivers.findIndex((x) => x === d);
        return (
          <Field key={globalIdx} label={`Driver — ${d.name}`} hint={`rating ${d.rating}`}>
            <div style={{ display: "flex", gap: 8 }}>
              <input
                type="text"
                value={d.name}
                onChange={(e) => setDrivers((prev) => {
                  const next = [...prev];
                  next[globalIdx] = { ...next[globalIdx], name: e.target.value };
                  return next;
                })}
                style={{ flex: 2, fontFamily: "var(--font-mono)", fontSize: 11 }}
              />
              <input
                type="number"
                value={d.rating}
                step={0.01} min={1} max={10}
                onChange={(e) => setDrivers((prev) => {
                  const next = [...prev];
                  next[globalIdx] = { ...next[globalIdx], rating: parseFloat(e.target.value) };
                  return next;
                })}
                style={{ flex: 1, fontFamily: "var(--font-mono)", fontSize: 11 }}
              />
            </div>
          </Field>
        );
      })}
      </Section>

      {/* ── ALL DRIVERS ── */}
      <Section title={`All Drivers (${aiDrivers.length} AI)`}>
        <div style={{ maxHeight: 300, overflowY: "auto", paddingRight: 4 }}>
        {aiDrivers.map((d, idx) => {
          const globalIdx = drivers.indexOf(d);
          return (
            <div key={globalIdx} style={{ display: "flex", gap: 8, marginBottom: 8 }}>
              <input
                type="text"
                value={d.name}
                onChange={(e) => setDrivers((prev) => {
                  const next = [...prev];
                  next[globalIdx] = { ...next[globalIdx], name: e.target.value };
                  return next;
                })}
                style={{ flex: 2, fontFamily: "var(--font-mono)", fontSize: 10 }}
              />
              <input
                type="number"
                value={d.rating}
                step={0.01} min={1} max={10}
                onChange={(e) => setDrivers((prev) => {
                  const next = [...prev];
                  next[globalIdx] = { ...next[globalIdx], rating: parseFloat(e.target.value) };
                  return next;
                })}
                style={{ flex: 1, fontFamily: "var(--font-mono)", fontSize: 10 }}
              />
              <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-3)", alignSelf: "center", minWidth: 80 }}>
                {d.team}
              </span>
            </div>
          );
        })}
        </div>
      </Section>

      {/* ── TEAMS ── */}
      <Section title="Teams">
        {teams.map((t, idx) => (
          <Field key={idx} label={t.name} hint={`rating ${t.rating}`}>
            <input
              type="text"
              value={t.name}
              onChange={(e) => setTeams((prev) => {
                const next = [...prev];
                next[idx] = { ...next[idx], name: e.target.value };
                return next;
              })}
              style={{ width: "100%", fontFamily: "var(--font-mono)", fontSize: 11 }}
            />
          </Field>
        ))}
      </Section>

      {/* ── SAVE ── */}
      <button
        className="btn btn-primary"
        style={{ fontSize: 11, letterSpacing: 2, padding: "12px 32px", marginTop: 8 }}
        onClick={handleSave}
        disabled={saving}
      >
        {saving ? "SAVING..." : "SAVE SETTINGS"}
      </button>

      <Toast msg={toast?.msg} type={toast?.type} />
    </div>
  );
}