import { useApi } from "../hooks/useApi";
import { api } from "../utils/api";

function PosBadge({ pos }) {
  const cls = pos === 1 ? "p1" : pos === 2 ? "p2" : pos === 3 ? "p3" : "";
  return <div className={`pos-badge ${cls}`}>{pos}</div>;
}

export default function StandingsPage() {
  const { data: teams, loading: tLoad, error: tErr } = useApi(api.getTeams);
  const { data: drivers, loading: dLoad, error: dErr } = useApi(api.getDrivers);

  return (
    <div>
      <div className="page-header">
        <div className="page-eyebrow">Championship</div>
        <div className="page-title">
          DRIVER <span>&amp;</span> CONSTRUCTOR<br />STANDINGS
        </div>
      </div>

      <div className="grid-2" style={{ gap: 32, alignItems: "start" }}>
        {/* DRIVERS */}
        <div>
          <div className="section-title" style={{ marginTop: 0 }}>Drivers</div>
          {dLoad && <div className="loading">LOADING</div>}
          {dErr && <div className="empty">⚠ {dErr}</div>}
          {drivers && (
            <table className="data-table">
              <thead>
                <tr>
                  <th>POS</th>
                  <th>DRIVER</th>
                  <th>TEAM</th>
                  <th>PTS</th>
                </tr>
              </thead>
              <tbody>
                {[...drivers]
                  .sort((a, b) => (b.points || 0) - (a.points || 0))
                  .map((d, i) => (
                    <tr key={d.name}>
                      <td><PosBadge pos={i + 1} /></td>
                      <td style={{ fontWeight: d.is_player ? 700 : 400, color: d.is_player ? "var(--text)" : "var(--text-2)" }}>
                        {d.name}
                        {d.is_player && (
                          <span className="badge badge-ok" style={{ marginLeft: 8, fontSize: 8 }}>YOU</span>
                        )}
                        {d.dnf && <span className="text-muted" style={{ marginLeft: 6, fontSize: 10 }}>DNF</span>}
                      </td>
                      <td className="text-muted" style={{ fontSize: 12 }}>{d.team || "—"}</td>
                      <td><span className="points-pill">{d.points || 0}</span></td>
                    </tr>
                  ))}
              </tbody>
            </table>
          )}
        </div>

        {/* CONSTRUCTORS */}
        <div>
          <div className="section-title" style={{ marginTop: 0 }}>Constructors</div>
          {tLoad && <div className="loading">LOADING</div>}
          {tErr && <div className="empty">⚠ {tErr}</div>}
          {teams?.teams && (
            <table className="data-table">
              <thead>
                <tr>
                  <th>POS</th>
                  <th>TEAM</th>
                  <th>RATING</th>
                  <th>PTS</th>
                </tr>
              </thead>
              <tbody>
                {[...teams.teams]
                  .sort((a, b) => (b.points || 0) - (a.points || 0))
                  .map((t, i) => (
                    <tr key={t.name}>
                      <td><PosBadge pos={i + 1} /></td>
                      <td>
                        <div style={{ fontFamily: "var(--font-display)", fontWeight: 700, fontSize: 14 }}>{t.name}</div>
                        <div style={{ fontSize: 11, color: "var(--text-3)", marginTop: 2 }}>
                          {(t.drivers || []).join(" · ")}
                        </div>
                      </td>
                      <td className="text-mono">{t.rating?.toFixed(4) ?? "—"}</td>
                      <td><span className="points-pill">{t.points || 0}</span></td>
                    </tr>
                  ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}
