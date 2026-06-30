/** Tyre compound colors — match styles.css .tyre.* */
export const PNEU_COLORS = {
  soft: "#ff4444",
  medium: "#ffd600",
  hard: "#cccccc",
  wet: "#448aff",
  inter: "#00e676",
};

/** Parse flat time_laps list into per-driver lap time arrays. */
export function parseTimeLaps(timeLaps) {
  const byDriver = {};
  for (const entry of timeLaps || []) {
    if (!entry || entry.length < 2) continue;
    const lapTime = Number(entry[0]);
    const name = entry[1];
    if (!Number.isFinite(lapTime)) continue;
    if (!byDriver[name]) byDriver[name] = [];
    byDriver[name].push(lapTime);
  }
  return byDriver;
}

/** Build gap-to-leader chart rows from state.time_laps. */
export function buildGapToLeaderData(timeLaps, driverNames) {
  const byDriver = parseTimeLaps(timeLaps);
  const names = driverNames?.length ? driverNames : Object.keys(byDriver);
  if (!names.length) return [];

  const cumulative = {};
  for (const name of names) {
    let sum = 0;
    cumulative[name] = (byDriver[name] || []).map((t) => {
      sum += t;
      return sum;
    });
  }

  const maxLaps = Math.max(...names.map((n) => cumulative[n].length), 0);
  const rows = [];

  for (let i = 0; i < maxLaps; i++) {
    let leaderTime = Infinity;
    for (const name of names) {
      const val = cumulative[name][i];
      if (val != null) leaderTime = Math.min(leaderTime, val);
    }
    if (!Number.isFinite(leaderTime)) continue;

    const row = { lap: i + 1 };
    for (const name of names) {
      const val = cumulative[name][i];
      if (val != null) row[name] = val - leaderTime;
    }
    rows.push(row);
  }

  return rows;
}

/** Map cumulative race time to 1-based lap index using lap_times. */
export function lapAtTime(lapTimes, targetTime) {
  if (!lapTimes?.length || targetTime == null) return 0;
  let sum = 0;
  for (let i = 0; i < lapTimes.length; i++) {
    sum += lapTimes[i];
    if (sum >= targetTime - 0.001) return i + 1;
  }
  return lapTimes.length;
}

/** Build stint segments { startLap, endLap, compound } for timeline UI. */
export function buildStintSegments(driver, totalLaps) {
  const lapTimes = driver.lap_times || [];
  const raceLaps = totalLaps || lapTimes.length || driver.position_history?.length || 1;
  const segments = [];

  for (const stint of driver.stints || []) {
    const startTime = Number(stint[0]);
    const duration = Number(stint[1]);
    const compound = (stint[2] || "medium").toLowerCase();
    const startLap = Math.max(1, lapAtTime(lapTimes, startTime) || 1);
    const endLap = Math.max(startLap, lapAtTime(lapTimes, startTime + duration));
    segments.push({ startLap, endLap, compound });
  }

  const lastEnd = segments.length ? segments[segments.length - 1].endLap : 0;
  const currentEnd = lapTimes.length || raceLaps;
  const compound = (driver.pneu || "medium").toLowerCase();

  if (currentEnd > lastEnd) {
    segments.push({
      startLap: lastEnd + 1,
      endLap: currentEnd,
      compound,
      current: true,
    });
  } else if (!segments.length && compound) {
    segments.push({ startLap: 1, endLap: Math.max(1, currentEnd), compound, current: true });
  }

  return segments;
}
