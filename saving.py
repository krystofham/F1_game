import json
import os
import csv
from datetime import datetime

_STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")

POINTS_TABLE = {
    1: 50, 2: 45, 3: 40, 4: 35, 5: 30,
    6: 25, 7: 22, 8: 20, 9: 18, 10: 15,
    11: 12, 12: 10, 13: 9, 14: 8, 15: 7,
    16: 6, 17: 5, 18: 4, 19: 3, 20: 2,
    21: 1, 22: 1, 23: 1
}

def _car_to_dict(car, position):
    positions = [p for p in car.position if p > 0]
    return {
        "position":      position,
        "name":          car.name,
        "team":          car.team.name if car.team else "",
        "points":        car.points,
        "rating":        round(car.ratings, 4),
        "is_player":     car.is_player,
        "dnf":           car.dnf,
        "pit_stops":     car.box,
        "pneu":          car.pneu,
        "wear":          round(car.wear, 2),
        "stints":        car.stints,
        "avg_position":  round(sum(positions) / len(positions), 2) if positions else None,
        "best_position": min(positions) if positions else None,
        "worst_position":max(positions) if positions else None,
    }

def _team_to_dict(team, position):
    return {
        "position":   position,
        "name":       team.name,
        "points":     team.points,
        "rating":     round(team.rating, 4),
        "drivers":    [d.name for d in team.drivers],
    }

def _build_standings(cars, teams):
    sorted_cars  = sorted(cars,  key=lambda x: x.points, reverse=True)
    sorted_teams = sorted(teams, key=lambda x: x.points, reverse=True)
    return {
        "drivers": [_car_to_dict(c, i+1)  for i, c in enumerate(sorted_cars)],
        "teams":   [_team_to_dict(t, i+1) for i, t in enumerate(sorted_teams)],
    }

def _save(data: dict):
    with open(_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# --- Veřejné funkce ---

def save_state_end_of_lap(cars, teams, season, race, lap):
    _save({"type": "lap", "season": season, "race": race, "lap": lap,
           **_build_standings(cars, teams)})

def save_state_end_of_race(cars, teams, season, race):
    _save({"type": "race", "season": season, "race": race,
           **_build_standings(cars, teams)})

def save_state_end_of_season(cars, teams, season):
    _save({"type": "season", "season": season,
           **_build_standings(cars, teams)})

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
                "season":        season_count,
                "position":      i,
                "name":          car.name,
                "team":          car.team.name if car.team else "",
                "points":        car.points,
                "rating":        round(car.ratings, 4),
                "is_player":     int(car.is_player),
                "dnf":           int(car.dnf),
                "pit_stops":     car.box,
                "avg_position":  round(sum(positions)/len(positions), 2) if positions else 0,
                "best_position": min(positions) if positions else 0,
                "worst_position":max(positions) if positions else 0,
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
            d = team.drivers  # ← používáš drivers, ne cars
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