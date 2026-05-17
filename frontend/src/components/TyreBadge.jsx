export default function TyreBadge({ type }) {
  const t = (type || "").toLowerCase();
  const labels = { soft: "S", medium: "M", hard: "H", wet: "W", inter: "I" };
  return (
    <span className={`tyre ${t}`} title={type}>
      {labels[t] || "?"}
    </span>
  );
}
