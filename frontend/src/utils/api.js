function resolveBaseUrl() {
  const runtimeDesktopBase =
    typeof window !== "undefined" &&
    window.desktopEnv &&
    typeof window.desktopEnv.getApiBaseUrl === "function"
      ? window.desktopEnv.getApiBaseUrl()
      : "";

  if (runtimeDesktopBase) {
    return runtimeDesktopBase;
  }

  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }

  // Keep Vite proxy behavior in browser development mode.
  if (import.meta.env.DEV) {
    return "";
  }
  return "http://127.0.0.1:8000";

}
// const BASE = resolveBaseUrl();
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
  simUntil: (lap) => req("POST", "/api/sim_until", { lap }),
  simRace: () => req("POST", "/api/sim_race"),
  postRace: () => req("POST", "/api/post_race"),
  postChampionship: () => req("POST", "/api/post_championship"),
  setLapUserData: (payload) => req("POST", "/api/set_lap_user_data", payload),
};
