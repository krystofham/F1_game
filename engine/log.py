"""Debug log pro transfery a načítání hráčů — soubor engine/info.log"""
import json
import os
from collections import Counter
from datetime import datetime

_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "info.log")

def dlog (**payload) -> dict:
    entry = dlog( **payload)
    return entry
def ilog (**payload) -> dict:
    entry = log("[INFO]" **payload)
    return entry
def wlog (**payload) -> dict:
    entry = log("[WARNING]" **payload)
    return entry
def elog (**payload) -> dict:
    entry = log("[ERROR]" **payload)
    return entry
def log(event: str, **payload) -> dict:
    entry = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "event": event,
        **payload,
    }
    try:
        print(f"[TRANSFER_DEBUG] {json.dumps(entry, ensure_ascii=False)}")
    except Exception:
        print(f"[TRANSFER_DEBUG] {event}")
    try:
        with open(_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass
    return entry


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


def snapshot_state(state: dict, label: str) -> dict:
    drivers = state.get("drivers", [])
    names = [d.get("name") for d in drivers]
    counts = Counter(names)
    p1 = state.get("player.name", "")
    p2 = state.get("player_2.name", "")
    return {
        "label": label,
        "player.name": p1,
        "player_2.name": p2,
        "players_in_drivers": [
            {"name": d.get("name"), "team": d.get("team"), "points": d.get("points")}
            for d in drivers
            if d.get("is_player")
        ],
        "max_in_drivers": "Max Verstappen" in names,
        "max_in_teams": any(
            "Max Verstappen" in t.get("drivers", [])
            for t in state.get("teams", [])
        ),
        "duplicate_driver_names": [n for n, c in counts.items() if c > 1 and n],
        "teams_mysql": next(
            (t.get("drivers") for t in state.get("teams", [])
             if t.get("name") == "MySql AWS Maxim racing team"),
            None,
        ),
        "teams_f10": next(
            (t.get("drivers") for t in state.get("teams", [])
             if t.get("name") == "Formula 1.0 racing team"),
            None,
        ),
        "driver_count": len(drivers),
    }


def snapshot_cars(cars, init_player, init_player_2) -> dict:
    return {
        "init_player_slot": getattr(init_player, "name", None),
        "init_player_2_slot": getattr(init_player_2, "name", None),
        "player_cars": [
            {
                "name": c.name,
                "team": c.team.name if c.team else None,
                "is_player": c.is_player,
                "id": id(c),
            }
            for c in cars
            if c.is_player
        ],
        "no_team": [c.name for c in cars if c.team is None],
        "shadow_candidates": [
            c.name
            for c in cars
            if c.team is None and not c.is_player
        ],
    }
