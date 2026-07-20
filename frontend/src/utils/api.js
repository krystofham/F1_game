import { formatApiError } from "./errors";

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
const BASE = resolveBaseUrl();

export function getApiBaseUrl() {
  return BASE || (typeof window !== "undefined" ? window.location.origin : "");
}

/** Lightweight probe used by the startup blocker screen. */
export async function checkEngine() {
  const res = await fetch(`${BASE}/api/health`, {
    method: "GET",
    headers: { Accept: "application/json" },
  });
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }
  return res.json();
}

async function req(method, path, body) {
  let res;
  try {
    res = await fetch(`${BASE}${path}`, {
      method,
      headers: { "Content-Type": "application/json" },
      body: body ? JSON.stringify(body) : undefined,
    });
  } catch (e) {
    throw new Error(formatApiError(e));
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    const detail = err.detail || `HTTP ${res.status}`;
    throw new Error(formatApiError(detail));
  }
  return res.json();
}

export const api = {
  getState: () => req("GET", "/api/get_state"),
  getWeather: () => req("GET", "/api/get_climax"),
  getDrivers: () => req("GET", "/api/get_drivers"),
  getTeams: () => req("GET", "/api/get_teams"),
  getTracks: () => req("GET", "/api/tracks"), 
  getTeam: (name) => req("GET", `/api/get_teams/${encodeURIComponent(name)}`),
  initRace: () => req("POST", "/api/init_race"),
  simLap: () => req("POST", "/api/sim_lap"),
  setInitConfig: (cfg) => req("POST", "/api/set_init_config", cfg),
  simUntil: (lap) => req("POST", "/api/sim_until", { lap }),
  simRace: () => req("POST", "/api/sim_race"),
  postRace: () => req("POST", "/api/post_race"),
  postChampionship: () => req("POST", "/api/post_championship"),
  setLapUserData: (payload) => req("POST", "/api/set_lap_user_data", payload),
  getTrackRecords: () => req("GET", "/api/stats/track_records"),
  getBiggestLaps: () => req("GET", "/api/stats/biggest_laps"),
  getTransferOffers: () => req("GET", "/api/get_transfer_offers"),
  doTransfer: (payload) => req("POST", "/api/do_transfer", payload),
};