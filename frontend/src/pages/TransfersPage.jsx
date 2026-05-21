import { useState } from "react";

const API = "http://localhost:8000/api";

export default function TransferMarket() {
  const [offers, setOffers] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selected, setSelected] = useState({ driver: null, pilot: null, league: "MMR1" });
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function fetchOffers() {
    setLoading(true);
    setError(null);
    setResult(null);
    setSelected({ driver: null, pilot: null, league: "MMR1" });
    try {
      const res = await fetch(`${API}/get_transfer_offers`);
      if (!res.ok) throw new Error(await res.text());
      setOffers(await res.json());
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function doTransfer() {
    if (!selected.driver || !selected.pilot) return;
    setLoading(true);
    setError(null);
    try {
      const body = {
        want: "yes",
        where: selected.league,
        pilot_to_change: selected.driver,
        chosen_pilot: selected.pilot,
      };
      const res = await fetch(`${API}/do_transfer`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setResult(data);
      setOffers(null);
    } catch (e) {
      setError(typeof e.message === "string" ? e.message : JSON.stringify(e.message));
    } finally {
      setLoading(false);
    }
  }

  const canConfirm = selected.driver && selected.pilot;

  return (
    <div className="main-content" style={{ padding: 0 }}>
      {/* Header */}
      <div
        className="flex items-center justify-between"
        style={{
          padding: "24px 32px",
          borderBottom: "1px solid var(--border)",
          background: "var(--bg-2)",
        }}
      >
        <div className="flex items-center gap-4">
          <div className="logo-mark">⇄</div>
          <div className="logo-text">
            <span className="logo-title">TRANSFER</span>
            <span className="logo-sub">DRIVER EXCHANGE BUREAU</span>
          </div>
        </div>
        <button className="btn btn-primary" onClick={fetchOffers} disabled={loading}>
          {loading ? "SCANNING..." : "SCAN MARKET"}
        </button>
      </div>

      <div style={{ padding: "28px 32px" }}>
        {/* Error */}
        {error && (
          <div
            className="mb-4"
            style={{
              padding: "14px 20px",
              border: "1px solid var(--accent)",
              background: "rgba(232,0,45,0.07)",
              fontFamily: "var(--font-mono)",
              fontSize: "12px",
            }}
          >
            <span className="text-accent">⚠ ERROR:</span>{" "}
            <span style={{ color: "var(--text-2)" }}>{error}</span>
          </div>
        )}

        {/* Success */}
        {result && (
          <div
            style={{
              maxWidth: 420,
              margin: "40px auto",
              textAlign: "center",
              padding: "40px",
              border: "1px solid var(--border-light)",
              background: "var(--bg-card)",
            }}
          >
            <div
              className="mb-4"
              style={{
                fontFamily: "var(--font-display)",
                fontSize: "20px",
                fontWeight: 700,
                letterSpacing: "4px",
                color: "var(--green)",
              }}
            >
              ✓ TRANSFER COMPLETE
            </div>
            <div className="flex gap-2 mb-6" style={{ justifyContent: "center" }}>
              <span className="badge badge-ok">{result.driver_1}</span>
              <span className="badge badge-ok">{result.driver_2}</span>
            </div>
            <button className="btn btn-success" onClick={fetchOffers}>
              SCAN AGAIN
            </button>
          </div>
        )}

        {/* Market content */}
        {offers && !result && (
          <>
            {/* League tabs */}
            <div className="flex gap-2 mb-6">
              {["MMR1", "MMR2"].map((l) => (
                <button
                  key={l}
                  className={`btn ${selected.league === l ? "btn-primary" : ""}`}
                  onClick={() => setSelected((s) => ({ ...s, league: l, pilot: null }))}
                >
                  {l}
                </button>
              ))}
            </div>

            {selected.league === "MMR1" ? (
              <div className="grid-2">
                {[
                  { label: "DRIVER 1", key: "driver_1" },
                  { label: "DRIVER 2", key: "driver_2" },
                ].map(({ label, key }) => {
                  const section = offers[key];
                  return (
                    <div key={key} className="card" style={{ padding: 0 }}>
                      {/* Column header */}
                      <div
                        className="flex items-center justify-between"
                        style={{
                          padding: "14px 18px",
                          borderBottom: "1px solid var(--border)",
                        }}
                      >
                        <span
                          style={{
                            fontFamily: "var(--font-mono)",
                            fontSize: "9px",
                            letterSpacing: "4px",
                            color: "var(--text-3)",
                            textTransform: "uppercase",
                          }}
                        >
                          {label}
                        </span>
                        <span
                          style={{
                            fontFamily: "var(--font-display)",
                            fontSize: "14px",
                            fontWeight: 700,
                            letterSpacing: "1px",
                            color: "var(--accent)",
                          }}
                        >
                          {section.name}
                        </span>
                      </div>

                      {/* Offer list */}
                      <div style={{ padding: "12px" }}>
                        {section.offers.length === 0 && (
                          <div className="empty" style={{ padding: "20px" }}>
                            No offers available
                          </div>
                        )}
                        {section.offers.map((o) => {
                          const isSelected =
                            selected.driver === section.name && selected.pilot === o.name;
                          return (
                            <div
                              key={o.name}
                              onClick={() =>
                                setSelected((s) => ({
                                  ...s,
                                  driver: section.name,
                                  pilot: isSelected ? null : o.name,
                                }))
                              }
                              style={{
                                padding: "14px 16px",
                                marginBottom: "8px",
                                border: isSelected
                                  ? "1px solid var(--accent)"
                                  : "1px solid var(--border)",
                                background: isSelected
                                  ? "var(--accent-glow)"
                                  : "var(--bg-3)",
                                cursor: "pointer",
                                position: "relative",
                                transition: "border-color 0.15s, background 0.15s",
                              }}
                            >
                              <div
                                style={{
                                  fontFamily: "var(--font-display)",
                                  fontSize: "15px",
                                  fontWeight: 700,
                                  letterSpacing: "1px",
                                  marginBottom: "6px",
                                  color: "var(--text)",
                                }}
                              >
                                {o.name}
                              </div>
                              <div
                                className="flex items-center justify-between mb-2"
                              >
                                <span className="text-mono">{o.team}</span>
                                <span className="text-mono">★ {o.rating}</span>
                              </div>
                              <div
                                style={{
                                  fontFamily: "var(--font-mono)",
                                  fontSize: "11px",
                                  color: "var(--accent)",
                                }}
                              >
                                {o.points} pts
                              </div>
                              {isSelected && (
                                <span
                                  className="badge badge-err"
                                  style={{
                                    position: "absolute",
                                    top: "8px",
                                    right: "10px",
                                  }}
                                >
                                  SELECTED
                                </span>
                              )}
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              /* MMR2 */
              <div className="card" style={{ maxWidth: 480 }}>
                <div className="card-label">Best MMR2 Driver Available</div>
                {offers.mmr2_best ? (
                  <>
                    <div
                      className="mb-2"
                      style={{
                        fontFamily: "var(--font-display)",
                        fontSize: "28px",
                        fontWeight: 900,
                        color: "var(--accent)",
                      }}
                    >
                      {offers.mmr2_best.name}
                    </div>
                    <div className="text-mono mb-4">
                      Rating: {offers.mmr2_best.rating}
                    </div>

                    <div
                      className="section-title"
                      style={{ marginTop: 0 }}
                    >
                      Replace which driver?
                    </div>

                    <div className="flex gap-2">
                      {[
                        { label: offers.driver_1.name },
                        { label: offers.driver_2.name },
                      ].map(({ label }) => {
                        const isSelected =
                          selected.pilot === offers.mmr2_best.name &&
                          selected.driver === label;
                        return (
                          <button
                            key={label}
                            className={`btn ${isSelected ? "btn-primary" : ""}`}
                            style={{ flex: 1 }}
                            onClick={() =>
                              setSelected((s) => ({
                                ...s,
                                driver: label,
                                pilot: offers.mmr2_best.name,
                              }))
                            }
                          >
                            {label}
                          </button>
                        );
                      })}
                    </div>
                  </>
                ) : (
                  <div className="empty">MMR2 data unavailable</div>
                )}
              </div>
            )}

            {/* Confirm row */}
            <div
              className="flex items-center justify-between mt-6"
              style={{
                borderTop: "1px solid var(--border)",
                paddingTop: "20px",
              }}
            >
              <div className="text-mono">
                {canConfirm ? (
                  <>
                    Replacing{" "}
                    <span style={{ color: "var(--text)" }}>{selected.driver}</span>
                    {" → "}
                    <span style={{ color: "var(--accent)" }}>{selected.pilot}</span>
                  </>
                ) : (
                  <span className="text-muted">Select a driver to continue</span>
                )}
              </div>
              <button
                className="btn btn-danger"
                onClick={doTransfer}
                disabled={!canConfirm || loading}
              >
                {loading ? "PROCESSING..." : "CONFIRM TRANSFER"}
              </button>
            </div>
          </>
        )}

        {/* Idle state */}
        {!offers && !result && !loading && (
          <div className="empty">
            Press <span style={{ color: "var(--text-2)" }}>SCAN MARKET</span> to view available
            drivers
          </div>
        )}

        {/* Loading */}
        {loading && <div className="loading">SCANNING MARKET</div>}
      </div>
    </div>
  );
}