import json
import os
import csv
from datetime import datetime

_STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")

def _build_standings(cars, teams):
    return {
        "standings": [
            {"driver": c.driver, "points": c.points, "team": c.team}
            for c in sorted(cars, key=lambda x: x.points, reverse=True)
        ],
        "teams": [
            {"name": t.name, "points": t.points}
            for t in sorted(teams, key=lambda x: x.points, reverse=True)
        ]
    }

def _save(data: dict):
    with open(_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def save_state_end_of_lap(cars, teams, season, race, lap):
    _save({"type": "lap", "season": season, "race": race, "lap": lap, **_build_standings(cars, teams)})

def save_state_end_of_race(cars, teams, season, race):
    _save({"type": "race", "season": season, "race": race, **_build_standings(cars, teams)})

def save_state_end_of_season(cars, teams, season):
    _save({"type": "season", "season": season, **_build_standings(cars, teams)})

def save_season_csv(cars, teams, season_count, championship):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # --- Drivers CSV ---
    drivers_file = f"data/season_{season_count}_drivers_{timestamp}.csv"
    os.makedirs("data", exist_ok=True)
    with open(drivers_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "season", "position", "driver", "team", "points",
            "rating", "is_player", "races", "dnf_count",
            "avg_position", "best_position", "worst_position",
            "pit_stops", "championships_raced"
        ])
        writer.writeheader()
        for i, car in enumerate(sorted(cars, key=lambda x: x.points, reverse=True), 1):
            positions = [p for p in car.position if p > 0]
            writer.writerow({
                "season":               season_count,
                "position":             i,
                "driver":               car.name,
                "team":                 car.team.name if car.team else "",
                "points":               car.points,
                "rating":               round(car.ratings, 4),
                "is_player":            int(car.is_player),
                "races":                len(championship),
                "dnf_count":            getattr(car, "dnf_count", 0),
                "avg_position":         round(sum(positions)/len(positions), 2) if positions else 0,
                "best_position":        min(positions) if positions else 0,
                "worst_position":       max(positions) if positions else 0,
                "pit_stops":            getattr(car, "pit_count", 0),
                "championships_raced":  season_count,
            })

    # --- Teams CSV ---
    teams_file = f"data/season_{season_count}_teams_{timestamp}.csv"
    with open(teams_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "season", "position", "team", "points", "performance",
            "driver_1", "driver_2", "driver_1_points", "driver_2_points"
        ])
        writer.writeheader()
        for i, team in enumerate(sorted(teams, key=lambda x: x.points, reverse=True), 1):
            d = team.cars  # předpokládám že team.cars je list dvou Car objektů
            writer.writerow({
                "season":           season_count,
                "position":         i,
                "team":             team.name,
                "points":           team.points,
                "performance":      round(getattr(team, "performance", 0), 4),
                "driver_1":         d[0].name if len(d) > 0 else "",
                "driver_2":         d[1].name if len(d) > 1 else "",
                "driver_1_points":  d[0].points if len(d) > 0 else 0,
                "driver_2_points":  d[1].points if len(d) > 1 else 0,
            })

    print(f"📁 Data saved: {drivers_file}, {teams_file}")