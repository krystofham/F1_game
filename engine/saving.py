import json
import os
import csv
from datetime import datetime
from log import dlog, elog, ilog, wlog, snapshot_race_ctx

_STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")

POINTS_TABLE = {
    1: 50, 2: 45, 3: 40, 4: 35, 5: 30,
    6: 25, 7: 22, 8: 20, 9: 18, 10: 15,
    11: 12, 12: 10, 13: 9, 14: 8, 15: 7,
    16: 6, 17: 5, 18: 4, 19: 3, 20: 2,
    21: 1, 22: 1, 23: 1
}

def _car_to_dict(car, position, time_laps=None):
    positions = [p for p in car.position if p > 0]
    # time_laps entries: (lap_time, driver_name, team_name, s1, s2, s3)
    driver_lap_times = []
    if time_laps:
        for entry in time_laps:
            # (lap_time, driver_name, team_name, s1, s2, s3)
            if entry and len(entry) >= 3 and entry[1] == car.name:
                driver_lap_times.append(float(entry[0]))
    return {
        "position":         position,
        "name":             car.name,
        "team":             car.team.name if car.team else "",
        "points":           car.points,
        "rating":           round(car.ratings, 4),
        "is_player":        car.is_player,
        "dnf":              car.dnf,
        "pit_stops":        car.box,
        "pneu":             car.pneu,
        "wear":             round(car.wear, 2),
        "stints":           car.stints,
        "avg_position":     round(sum(positions) / len(positions), 2) if positions else None,
        "best_position":    min(positions) if positions else None,
        "worst_position":   max(positions) if positions else None,
        # potřebné pro obnovu simulace
        "time":             round(getattr(car, "time", 0.0), 4),
        "drs":              getattr(car, "drs", False),
        "pit":              getattr(car, "pit", False),
        "position_history": list(car.position),
        "lap_times":        driver_lap_times,
    }

def _team_to_dict(team, position):
    return {
        "position": position,
        "name":     team.name,
        "points":   team.points,
        "rating":   round(team.rating, 4),
        "drivers":  [d.name for d in team.drivers],
    }

def _build_standings(cars, teams, time_laps=None):
    sorted_cars  = sorted(cars,  key=lambda x: x.points, reverse=True)
    sorted_teams = sorted(teams, key=lambda x: x.points, reverse=True)
    return {
        "drivers": [_car_to_dict(c, i + 1, time_laps)  for i, c in enumerate(sorted_cars)],
        "teams":   [_team_to_dict(t, i + 1) for i, t in enumerate(sorted_teams)],
    }

def _save(data: dict, caller: str = "_save"):
    if os.path.exists(_STATE_FILE):
        try:
            with open(_STATE_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
            for key in ("b", "season_count", "championship_length", "player.name", "player_2.name"):
                if key in existing and key not in data:
                    data[key] = existing[key]
        except (json.JSONDecodeError, IOError) as e:
            wlog(fn=caller, msg="could not merge existing state keys", error=str(e))
    try:
        with open(_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        dlog(fn=caller, msg="state.json written",
             type=data.get("type"), lap=data.get("lap"), race=data.get("race"),
             time_laps_count=len(data.get("time_laps", [])))
    except OSError as e:
        elog(fn=caller, msg="state.json write failed", error=str(e))
        raise

# ---------------------------------------------------------------------------
# Sestavení race_ctx — zavolej jednou před závodem, předávej do save funkcí
# ---------------------------------------------------------------------------

def build_race_ctx(
    weather, climax, wettiness,
    safety_car, safety_car_laps_remaining,
    forecast, training_type, speed_bonus,
    pneu_type, speed_type,
    k_wear, k_speed, total_laps, time_laps=None
) -> dict:
    return {
        "weather":                   weather,
        "climax":                    climax,
        "wettiness":                 wettiness,
        "safety_car":                safety_car,
        "safety_car_laps_remaining": safety_car_laps_remaining,
        "forecast":                  list(forecast),
        "training_type":             training_type,
        "speed_bonus":               speed_bonus,
        "pneu_type":                 pneu_type,
        "speed_type":                speed_type,
        "k_wear":                    list(k_wear),
        "k_speed":                   list(k_speed),
        "total_laps":                total_laps,
        # time_laps NENÍ součástí race_ctx — ukládá se zvlášť na root úrovni
    }


# ---------------------------------------------------------------------------
# Veřejné funkce
# ---------------------------------------------------------------------------

def save_state_end_of_lap(cars, teams, season, race, lap, race_ctx=None, time_laps=None, player_name=None, player_2_name=None):
    player_cars = [c.name for c in cars if c.is_player]
    dlog(fn="save_state_end_of_lap", msg="saving lap state",
         lap=lap, race=race,
         player_name_arg=player_name, player_2_name_arg=player_2_name,
         player_cars_in_memory=player_cars,
         race_ctx=snapshot_race_ctx(race_ctx, "save_state_end_of_lap") if race_ctx else None)

    tl = time_laps
    if tl is None and race_ctx is not None:
        tl = race_ctx.get("time_laps", [])

    data = {
        "type":      "lap",
        "season":    season,
        "race":      race,
        "lap":       lap,
        "time_laps": tl or [],
        **_build_standings(cars, teams, tl),
    }
    if race_ctx is not None:
        ctx_to_save = {k: v for k, v in race_ctx.items() if k != "time_laps"}
        data["race_state"] = ctx_to_save
    if player_name:
        data["player.name"] = player_name
    if player_2_name:
        data["player_2.name"] = player_2_name
    _save(data, "save_state_end_of_lap")

def save_state_end_of_race(cars, teams, season, race, time_laps=None):
    ilog(fn="save_state_end_of_race", msg="saving end-of-race state",
         race=race, season=season, time_laps_count=len(time_laps or []))
    data = {
        "type":      "race",
        "season":    season,
        "race":      race,
        "time_laps": time_laps or [],
        **_build_standings(cars, teams, time_laps),
    }
    # Zachovej race_state (potřebuje post_race pro climax)
    if os.path.exists(_STATE_FILE):
        try:
            with open(_STATE_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
            if "race_state" in existing:
                data["race_state"] = existing["race_state"]
        except (json.JSONDecodeError, IOError):
            pass
    _save(data, "save_state_end_of_race")

def save_state_end_of_season(cars, teams, season):
    ilog(fn="save_state_end_of_season", msg="saving end-of-season state", season=season)
    _save({
        "type":   "season",
        "season": season,
        **_build_standings(cars, teams),
    }, "save_state_end_of_season")

def save_season_csv(cars, teams, season_count):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("data", exist_ok=True)

    # Drivers CSV
    drivers_file = f"data/season_{season_count}_drivers_{timestamp}.csv"
    sorted_cars = sorted(cars, key=lambda x: x.points, reverse=True)
    with open(drivers_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "season", "position", "name", "team", "points", "rating",
            "is_player", "dnf", "pit_stops", "avg_position",
            "best_position", "worst_position"
        ])
        writer.writeheader()
        for i, car in enumerate(sorted_cars, 1):
            positions = [p for p in car.position if p > 0]
            writer.writerow({
                "season":         season_count,
                "position":       i,
                "name":           car.name,
                "team":           car.team.name if car.team else "",
                "points":         car.points,
                "rating":         round(car.ratings, 4),
                "is_player":      int(car.is_player),
                "dnf":            int(car.dnf),
                "pit_stops":      car.box,
                "avg_position":   round(sum(positions) / len(positions), 2) if positions else 0,
                "best_position":  min(positions) if positions else 0,
                "worst_position": max(positions) if positions else 0,
            })

    # Teams CSV
    teams_file = f"data/season_{season_count}_teams_{timestamp}.csv"
    sorted_teams = sorted(teams, key=lambda x: x.points, reverse=True)
    with open(teams_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "season", "position", "team", "points", "rating",
            "driver_1", "driver_2", "driver_1_points", "driver_2_points"
        ])
        writer.writeheader()
        for i, team in enumerate(sorted_teams, 1):
            d = team.drivers
            writer.writerow({
                "season":          season_count,
                "position":        i,
                "team":            team.name,
                "points":          team.points,
                "rating":          round(team.rating, 4),
                "driver_1":        d[0].name if len(d) > 0 else "",
                "driver_2":        d[1].name if len(d) > 1 else "",
                "driver_1_points": d[0].points if len(d) > 0 else 0,
                "driver_2_points": d[1].points if len(d) > 1 else 0,
            })

    ilog(fn="save_season_csv", msg="season CSV exported",
         season=season_count, drivers_file=drivers_file, teams_file=teams_file)

# ---------------------------------------------------------------------------
# CSV helpers — auto-rotation
# ---------------------------------------------------------------------------

CSV_MAX_BYTES = 50 * 1024 * 1024  # 50 MB

def _rotate_if_needed(filepath: str):
    if not os.path.exists(filepath):
        return
    if os.path.getsize(filepath) < CSV_MAX_BYTES:
        return
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if len(lines) <= 1:
        return
    # Zachovej hlavičku + spodní polovinu řádků
    header = lines[0]
    keep = lines[len(lines) // 2:]
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(header)
        f.writelines(keep)
    ilog(fn="_rotate_if_needed", msg="CSV rotated", filepath=filepath, removed_lines=len(lines) - len(keep))


def save_race_csv(drivers: list, race: str, season: int, race_ctx: dict):
    os.makedirs("data", exist_ok=True)
    filepath = "data/races.csv"

    _rotate_if_needed(filepath)

    fieldnames = [
        "season", "race", "position", "name", "team",
        "points", "rating", "is_player", "dnf",
        "pit_stops", "total_time", "avg_position",
        "best_position", "worst_position",
        "stints_count", "weather", "wettiness", "total_laps",
    ]

    file_exists = os.path.exists(filepath)
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for d in drivers:
            writer.writerow({
                "season":         season,
                "race":           race,
                "position":       d.get("position", ""),
                "name":           d.get("name", ""),
                "team":           d.get("team", ""),
                "points":         d.get("points", 0),
                "rating":         round(d.get("rating", 0), 4),
                "is_player":      int(d.get("is_player", False)),
                "dnf":            int(d.get("dnf", False)),
                "pit_stops":      d.get("pit_stops", 0),
                "total_time":     round(d.get("time", 0.0), 4),
                "avg_position":   d.get("avg_position", ""),
                "best_position":  d.get("best_position", ""),
                "worst_position": d.get("worst_position", ""),
                "stints_count":   len(d.get("stints", [])),
                "weather":        race_ctx.get("weather", ""),
                "wettiness":      race_ctx.get("wettiness", ""),
                "total_laps":     race_ctx.get("total_laps", ""),
            })

    ilog(fn="save_race_csv", msg="race CSV appended",
         race=race, season=season, drivers_count=len(drivers))

RECORDS_FILE = "data/track_records.csv"
_RECORDS_FIELDS = ["track", "driver", "team", "lap_time", "season", "race"]

def _load_records() -> dict:
    if not os.path.exists(RECORDS_FILE):
        return {}
    records = {}
    with open(RECORDS_FILE, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            records[row["track"]] = row
    return records

def _write_records(records: dict):
    os.makedirs("data", exist_ok=True)
    with open(RECORDS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_RECORDS_FIELDS)
        writer.writeheader()
        writer.writerows(records.values())

def update_track_record(time_laps: list, track: str, season: int) -> bool:
    if not time_laps:
        return False

    # Nejrychlejší kolo závodu
    best = min(time_laps, key=lambda x: x[0])
    best_time, best_driver, best_team = best[0], best[1], best[2]

    records = _load_records()
    current = records.get(track)

    if current is None or best_time < float(current["lap_time"]):
        records[track] = {
            "track":    track,
            "driver":   best_driver,
            "team":     best_team,
            "lap_time": round(best_time, 4),
            "season":   season,
            "race":     track,
        }
        _write_records(records)
        ilog(fn="update_track_record", msg="track record broken",
             track=track, driver=best_driver, lap_time=round(best_time, 4),
             season=season, previous=current["lap_time"] if current else "none")
        return True

    return False