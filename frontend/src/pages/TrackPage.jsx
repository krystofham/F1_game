import { useApi } from "../hooks/useApi";
import { api } from "../utils/api";

const COUNTRY_FLAGS = {
  spain: "🇪🇸", uk: "🇬🇧", britain: "🇬🇧", italy: "🇮🇹",
  monaco: "🇲🇨", austria: "🇦🇹", france: "🇫🇷", germany: "🇩🇪",
  netherlands: "🇳🇱", belgium: "🇧🇪", hungary: "🇭🇺", singapore: "🇸🇬",
  japan: "🇯🇵", usa: "🇺🇸", "united states": "🇺🇸", mexico: "🇲🇽",
  brazil: "🇧🇷", australia: "🇦🇺", canada: "🇨🇦", china: "🇨🇳",
  uae: "🇦🇪", dubai: "🇦🇪", bahrain: "🇧🇭", azerbaijan: "🇦🇿",
  saudi: "🇸🇦", qatar: "🇶🇦",
  czech: "🇨🇿", "czech republic": "🇨🇿", prague: "🇨🇿", ostrava: "🇨🇿",
  poland: "🇵🇱", varsava: "🇵🇱", warsaw: "🇵🇱",
  bahamas: "🇧🇸",
  bulgaria: "🇧🇬", bulgarian: "🇧🇬",
  turkey: "🇹🇷",
  spain: "🇪🇸", espana: "🇪🇸"
};

function guessFlag(name) {
  const lower = (name || "").toLowerCase();
  for (const [key, flag] of Object.entries(COUNTRY_FLAGS)) {
    if (lower.includes(key)) return flag;
  }
  return "🏁";
}

function StatBlock({ label, value, unit }) {
  return (
    <div className="card">
      <div className="card-label">{label}</div>
      <div className="card-value" style={{ fontSize: 26 }}>
        {value ?? "—"}
        {unit && <span style={{ fontSize: 14, color: "var(--text-2)", marginLeft: 6 }}>{unit}</span>}
      </div>
    </div>
  );
}

export default function TrackPage() {
  const { data: state, loading, error } = useApi(api.getState);

  const race = state?.race;
  const championship = state?.championship || [];
  const b = state?.b ?? 1;
  const currentTrack = championship[b - 1] || {};

  if (loading) return <div className="loading">LOADING TRACK</div>;
  if (error) return <div className="empty">⚠ {error}</div>;

  const flag = guessFlag(currentTrack.name || race || "");
  const dnfProb = 100 * 22 * (state?.race_state?.total_laps) / 5000
  return (
    <div>
      <div className="page-header">
        <div className="page-eyebrow">
          Race {b} of {state.championship_length || "?"}
        </div>
        <div className="page-title">
          <span style={{ fontSize: 56, marginRight: 12 }}>{flag}</span>
          <span>{(currentTrack.name || race || "CIRCUIT").toUpperCase()}</span>
        </div>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 14, marginBottom: 24 }}>
        <StatBlock label="Laps" value={currentTrack.laps ?? state?.race_state?.total_laps} />
        <StatBlock
          label="DNF Risk"
          value={dnfProb != null ? dnfProb.toFixed(1) : "—"}
          unit="%"
        />
        <StatBlock
          label="Weather"
          value={state?.race_state?.weather || "—"}
        />
        <StatBlock
          label="Season"
          value={state?.season_count || 1}
        />
      </div>

      {(currentTrack.pneu_types || currentTrack.speed_types) && (
        <div>
          <div className="section-title">Compound Profile</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
            <div className="card">
              <div className="card-label" style={{ marginBottom: 10 }}>Tyre Compounds</div>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                {(currentTrack.pneu_types || ["soft", "medium", "hard"]).map((t) => (
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
            {championship.map((race, i) => {
              const name = typeof race === "string" ? race : race?.name ?? `Race ${i + 1}`;
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