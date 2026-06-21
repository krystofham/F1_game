import json
import os
from collections import Counter
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime
import atexit

# --- Konfigurace logování ---
_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "info.log")

# PRODUCTION/DEBUG
PRODUCTION = "prod" # or deb

# --- Buffer a flush ---
_buffer: list[str] = []
_FLUSH_EVERY = 20
DEBUG_MODE = False

def _flush() -> None:
    if not _buffer:
        return
    try:
        with open(_LOG_PATH, "a", encoding="utf-8") as f:
            f.write("\n".join(_buffer) + "\n")
        _buffer.clear()
    except OSError:
        pass

atexit.register(_flush)

# --- Kontext pro funkce ---
_fn_ctx: ContextVar[str | None] = ContextVar("log_fn", default=None)

@contextmanager
def log_context(fn: str):
    token = _fn_ctx.set(fn)
    try:
        yield
    finally:
        _fn_ctx.reset(token)

def _inject_fn(payload: dict) -> dict:
    if "fn" not in payload:
        fn = _fn_ctx.get()
        if fn:
            payload["fn"] = fn
    return payload

# --- Logovací funkce (kompatibilní) ---
def log(event: str, **payload) -> dict:
    entry = {"ts": datetime.now().isoformat(timespec="seconds"), "event": event, **_inject_fn(payload)}
    line = json.dumps(entry, ensure_ascii=False)

    if DEBUG_MODE:
        print(line)

    _buffer.append(line)
    if len(_buffer) >= _FLUSH_EVERY:
        _flush()

    return entry

def _is_prod() -> bool:
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_input/settings.json")
        with open(path) as f:
            return not json.load(f).get("show_logs", False)
    except Exception:
        return True

def dlog(**payload) -> dict:
    if _is_prod():
        return
    return log("[DEBUG]", **payload)

def ilog(**payload) -> dict:
    if _is_prod():
        return
    return log("[INFO]", **payload)

def wlog(**payload) -> dict:
    return log("[WARNING]", **payload)

def elog(**payload) -> dict:
    return log("[ERROR]", **payload)

# --- Čtení a mazání logů ---
def read_log(max_lines: int = 200) -> list[dict]:
    if not os.path.exists(_LOG_PATH):
        return []
    try:
        with open(_LOG_PATH, encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        return []
    out = []
    for line in lines[-max_lines:]:
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            out.append({"raw": line})
    return out

def clear_log() -> None:
    try:
        with open(_LOG_PATH, "w", encoding="utf-8") as f:
            f.write("")
    except OSError:
        pass

# --- Snapshoty (původní) ---
def snapshot_state(state: dict, label: str) -> dict:
    drivers = state.get("drivers", [])
    teams = state.get("teams", [])
    names = [d.get("name") for d in drivers if d.get("name")]
    counts = Counter(names)
    p1 = state.get("player.name", "")
    p2 = state.get("player_2.name", "")

    player_names = {p1, p2} - {""}

    return {
        "label": label,
        "player_1_name": p1,
        "player_2_name": p2,
        "players_in_drivers": [
            {
                "name": d.get("name"),
                "team": d.get("team"),
                "points": d.get("points"),
            }
            for d in drivers
            if d.get("is_player")
        ],
        "duplicate_names": [n for n, c in counts.items() if c > 1],
        "players_missing_from_drivers": [
            name for name in player_names
            if not any(d.get("name") == name and d.get("is_player") for d in drivers)
        ],
        "players_in_teams": {
            name: next(
                (t.get("name") for t in teams if name in t.get("drivers", [])),
                None,
            )
            for name in player_names
        },
        "team_rosters": {
            t.get("name"): t.get("drivers", [])
            for t in teams
        },
        "driver_count": len(drivers),
        "team_count": len(teams),
    }

def snapshot_cars(cars: list, init_player, init_player_2) -> dict:
    return {
        "init_slot_player_1": getattr(init_player, "name", None),
        "init_slot_player_2": getattr(init_player_2, "name", None),
        "player_cars": [
            {
                "name": c.name,
                "team": c.team.name if c.team else None,
                "is_player": c.is_player,
                "pneu": getattr(c, "pneu", None),
                "wear": round(getattr(c, "wear", 0.0), 3),
            }
            for c in cars
            if c.is_player
        ],
        "no_team": [
            {"name": c.name, "is_player": c.is_player}
            for c in cars
            if c.team is None
        ],
        "shadow_duplicates": [
            c.name
            for c in cars
            if c.team is None and not c.is_player
        ],
        "total_cars": len(cars),
    }

def snapshot_init_config(cfg: dict, label: str) -> dict:
    return {
        "label": label,
        "pneu_driver_1": cfg.get("pneu_driver_1"),
        "pneu_driver_2": cfg.get("pneu_driver_2"),
        "training_mode": cfg.get("training_mode"),
        "length": cfg.get("length"),
        "keys": sorted(cfg.keys()),
    }

def snapshot_race_ctx(race_ctx: dict, label: str) -> dict:
    return {
        "label": label,
        "weather": race_ctx.get("weather"),
        "climax": race_ctx.get("climax"),
        "wettiness": race_ctx.get("wettiness"),
        "total_laps": race_ctx.get("total_laps"),
        "training_type": race_ctx.get("training_type"),
        "speed_bonus": race_ctx.get("speed_bonus"),
        "pneu_type": race_ctx.get("pneu_type"),
        "speed_type": race_ctx.get("speed_type"),
        "forecast_len": len(race_ctx.get("forecast", [])),
        "safety_car": race_ctx.get("safety_car"),
    }