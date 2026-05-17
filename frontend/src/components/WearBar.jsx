export default function WearBar({ wear = 0 }) {
  const pct = Math.min(100, Math.max(0, wear));
  const color =
    pct > 80 ? "var(--accent)" : pct > 50 ? "var(--yellow)" : "var(--green)";
  return (
    <div className="wear-bar-wrap">
      <div className="wear-bar-bg">
        <div
          className="wear-bar-fill"
          style={{ width: `${pct}%`, background: color }}
        />
      </div>
      <span className="wear-val">{pct.toFixed(0)}%</span>
    </div>
  );
}
