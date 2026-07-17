/** Turn network/API failures into plain-language messages for players. */
export function formatApiError(err, context) {
  const raw = typeof err === "string" ? err : err?.message || "Unknown error";
  const lower = raw.toLowerCase();

  if (
    lower.includes("failed to fetch") ||
    lower.includes("networkerror") ||
    lower.includes("network request failed") ||
    lower.includes("load failed")
  ) {
    return "Cannot reach the game engine. Wait a few seconds, then try again. If this keeps happening, restart MMRAC1NG.";
  }

  if (lower.includes("init_race") || lower.includes("race_state missing")) {
    return "No race is set up yet. Open Race Control and click INIT RACE.";
  }

  if (lower.includes("state.json") || lower.includes("not initialized")) {
    return "Your season has not been started yet. Go to Race Control and click INIT RACE.";
  }

  if (lower.includes("http 404") || lower.includes("not found")) {
    return context === "team"
      ? "That team could not be found."
      : "The game could not find the requested data.";
  }

  if (lower.includes("http 500") || lower.includes("internal server")) {
    return "The game engine hit an unexpected error. Try again, or restart the app.";
  }

  if (lower.includes("http 503") || lower.includes("http 502")) {
    return "The game engine is temporarily unavailable. Please wait and retry.";
  }

  if (lower.startsWith("http ")) {
    return "Something went wrong while talking to the game engine. Try again or restart the app.";
  }

  return raw.length > 120
    ? "Something went wrong. Try again or restart the app."
    : raw;
}

/** True when the player still needs to run INIT RACE (fresh install or new weekend). */
export function needsWelcome(state) {
  if (!state || Object.keys(state).length === 0) return true;
  if (!state.drivers?.length || !state.teams?.length) return true;
  if (!state.race_state) return true;
  return false;
}
