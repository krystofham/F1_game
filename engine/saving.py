import json
import os
import csv
from datetime import datetime
import random
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
    # Extrahuj per-driver lap times z globálního time_laps listu
    # time_laps je list of lists: [[name, lap_time], ...] nebo [[name, lap, time], ...]
    driver_lap_times = []
    if time_laps:
        for entry in time_laps:
            if entry and entry[0] == car.name:
                driver_lap_times.append(float(entry[-1]))
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

def _save(data: dict):
    # Zachovej b a season_count z existujícího state
    if os.path.exists(_STATE_FILE):
        try:
            with open(_STATE_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
            for key in ("b", "season_count", "championship_length"):
                if key in existing and key not in data:
                    data[key] = existing[key]
        except (json.JSONDecodeError, IOError):
            pass
    with open(_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

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
        "total_laps":                random.randint(45, 70),
        # time_laps NENÍ součástí race_ctx — ukládá se zvlášť na root úrovni
    }


# ---------------------------------------------------------------------------
# Veřejné funkce
# ---------------------------------------------------------------------------

def save_state_end_of_lap(cars, teams, season, race, lap, race_ctx: dict = None, time_laps=None):
    """
    race_ctx je volitelný — pokud ho nepředáš, uloží se jen standings (zpětná kompatibilita).
    time_laps se ukládá na root úrovni state.json (ne uvnitř race_ctx) aby přežil každé kolo.
    """
    # time_laps z race_ctx (zpětná kompatibilita) nebo z parametru
    tl = time_laps
    if tl is None and race_ctx is not None:
        # Bezpečně vyjmout bez mutace — race_ctx zůstane neporušený
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
        # Uložit race_ctx BEZ time_laps (time_laps patří na root)
        ctx_to_save = {k: v for k, v in race_ctx.items() if k != "time_laps"}
        data["race_state"] = ctx_to_save
    _save(data)

def save_state_end_of_race(cars, teams, season, race, time_laps=None):
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
    _save(data)
def save_state_end_of_season(cars, teams, season):
    _save({
        "type":   "season",
        "season": season,
        **_build_standings(cars, teams),
    })

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

    print(f"📁 Uloženo: {drivers_file}, {teams_file}")