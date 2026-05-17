const BASE = "http://localhost:8000";

async function req(method, path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

export const api = {
  getState: () => req("GET", "/api/get_state"),
  getDrivers: () => req("GET", "/api/get_drivers"),
  getTeams: () => req("GET", "/api/get_teams"),
  getTeam: (name) => req("GET", `/api/get_teams/${encodeURIComponent(name)}`),
  initRace: () => req("POST", "/api/init_race"),
  simLap: () => req("POST", "/api/sim_lap"),
  postRace: () => req("POST", "/api/post_race"),
  postChampionship: () => req("POST", "/api/post_championship"),
};
