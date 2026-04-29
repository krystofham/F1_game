from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os, json, random
from engine.big_functions import *

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

_CONFIG = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_game_objects():
    from engine.init import (
        cars, teams, player, player_2, championship, tracks,
        DRIVER_1, DRIVER_2, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING
    )
    state = load_state()
    b = state.get("b", 1)
    season_count = state.get("season_count", 1)
    return cars, teams, player, player_2, championship, tracks, \
           DRIVER_1, DRIVER_2, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count
def _load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def _state():
    try:
        with open(f"engine/state.json", "r") as input_file:
            data = json.load(input_file)
        return data  # engine/state.json
    except:
        return {} 

# ---------------------------------------------------------------------------
# GET endpointy — data
# ---------------------------------------------------------------------------

@app.get("/api/get_state")
async def get_state():
    return _state()

@app.get("/api/get_drivers")
async def get_drivers():
    return _load_json(os.path.join(_CONFIG, "config/drivers.json"))

@app.get("/api/get_teams")
async def get_teams():
    return _load_json(os.path.join(_CONFIG, "config/teams.json"))

@app.get("/api/get_teams/{team_id}")
async def get_team(team_id: int):
    teams = _load_json(os.path.join(_CONFIG, "config/teams.json"))
    if team_id >= len(teams["teams"]):
        raise HTTPException(status_code=404, detail="Team index out of range")
    return teams["teams"][team_id]

# ---------------------------------------------------------------------------
# POST /api/init_race  — zavolej jednou před závodem
# ---------------------------------------------------------------------------

@app.post("/api/init_race")
async def api_init_race():
    """
    Inicializuje závod: načte objekty z engine, zavolá init_race(),
    uloží state. Vrátí race_ctx pro frontend.
    """
    cars, teams, player, player_2, championship, tracks, \
    DRIVER_1, DRIVER_2, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count = load_game_objects()

    state = _state()
    race = championship[b - 1]

    speed_bonus, season_count, time_laps, k_speed, k_wear, training_type, \
    WETTINESS, lap, forecast, weather, climax, pneu, speed, PNEU_types, \
    weather_1, weather_2, weather_3, weather_4, weather = init_race(
        tracks, race, cars, teams, championship,
        player, player_2, b, season_count
    )

    return {"status": "ok", "race": race, "lap": lap, "total_laps": state.get("race_state", {}).get("total_laps")}

# ---------------------------------------------------------------------------
# POST /api/sim_lap  — zavolej každé kolo
# ---------------------------------------------------------------------------

@app.post("/api/sim_lap")
async def api_sim_lap():
    """
    Odsimuluje jedno kolo. Čte vše ze state.json, uloží nový stav.
    Frontend posílá akce hráče přes lap_user_data.json a deal.json před voláním.
    """
    state = _state()
    race_ctx = state.get("race_state")
    if not race_ctx:
        raise HTTPException(status_code=400, detail="Race not initialized. Call /api/init_race first.")

    lap = state["lap"]
    if lap > race_ctx["total_laps"]:
        raise HTTPException(status_code=400, detail="Race already finished. Call /api/post_race.")

    cars, teams, player, player_2, championship, tracks, \
    DRIVER_1, DRIVER_2, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count = load_game_objects()

    time_laps = state.get("time_laps", [])
    race = state["race"]

    lap, cars, teams = sim_the_lap(
        cars, teams, player, player_2, lap,
        SAFETY_CAR, LAPS_REMAINING,
        race_ctx["wettiness"], race_ctx["forecast"], race_ctx["weather"],
        race_ctx["total_laps"], race_ctx["climax"],
        DRIVER_1, DRIVER_2,
        race_ctx["pneu_type"], race_ctx["speed_type"],
        {
            "hard":   {"wear": race_ctx["k_wear"][0], "speed": race_ctx.get("k_speed", [1,1,1,1,1])[0]},
            "medium": {"wear": race_ctx["k_wear"][1], "speed": race_ctx.get("k_speed", [1,1,1,1,1])[1]},
            "soft":   {"wear": race_ctx["k_wear"][2], "speed": race_ctx.get("k_speed", [1,1,1,1,1])[2]},
            "wet":    {"wear": race_ctx["k_wear"][3], "speed": race_ctx.get("k_speed", [1,1,1,1,1])[3]},
            "inter":  {"wear": race_ctx["k_wear"][4], "speed": race_ctx.get("k_speed", [1,1,1,1,1])[4]},
        },
        race_ctx["forecast"][0] if len(race_ctx["forecast"]) > 0 else race_ctx["weather"],
        race_ctx["forecast"][1] if len(race_ctx["forecast"]) > 1 else race_ctx["weather"],
        race_ctx["forecast"][2] if len(race_ctx["forecast"]) > 2 else race_ctx["weather"],
        race_ctx["training_type"], race_ctx["k_wear"],
        race_ctx["speed_bonus"], season_count, race, time_laps
    )

    new_state = _state()
    return {
        "status": "ok",
        "lap": new_state["lap"],
        "total_laps": race_ctx["total_laps"],
        "finished": new_state["lap"] > race_ctx["total_laps"],
    }

# ---------------------------------------------------------------------------
# POST /api/post_race  — po posledním kole
# ---------------------------------------------------------------------------

@app.post("/api/post_race")
async def api_post_race():
    state = _state()
    race_ctx = state.get("race_state", {})

    cars, teams, player, player_2, championship, tracks, \
    DRIVER_1, DRIVER_2, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count = load_game_objects()

    time_laps = state.get("time_laps", [])
    race = state["race"]
    climax = race_ctx.get("climax", "sunny")

    RANK = [a for a in cars if not a.dnf]
    save_state_end_of_race(cars, teams, season_count, race)
    teams, cars, time_laps = post_race_info(time_laps, player, player_2, cars, teams, COUNT_CARS)
    points, cars, teams, players = plot_graph(RANK, DRIVER_1, DRIVER_2, teams, cars, player, player_2, climax)
    lap, time_laps, SAFETY_CAR, LAPS_REMAINING, weather, forecast, cars, WETTINESS = reset_race(climax, cars)

    return {"status": "race_done", "race": race}

# ---------------------------------------------------------------------------
# POST /api/post_championship  — po posledním závodě sezóny
# ---------------------------------------------------------------------------

@app.post("/api/post_championship")
async def api_post_championship():
    state = _state()

    cars, teams, player, player_2, championship, tracks, \
    DRIVER_1, DRIVER_2, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count = load_game_objects()

    save_state_end_of_season(cars, teams, season_count)

    best, worst = simulate_season_mmr2(list_drivers_mmr2)
    season_count += 1

    for mmr2_driver in list_drivers_mmr2:
        mmr2_driver.rating -= 1 / (season_count * 2)

    worst.name = random.choice(names_free_drivers)
    worst.rating = random.uniform(0.95, 1.05)

    cars.sort(key=lambda x: x.points, reverse=True)
    last_car = cars[-1]

    if last_car.is_player:
        if DRIVER_1 == last_car.name:
            DRIVER_1 = best.name
            player.name, player.ratings = best.name, best.rating
        elif DRIVER_2 == last_car.name:
            DRIVER_2 = best.name
            player_2.name, player_2.ratings = best.name, best.rating

    best.name, best.rating = last_car.name, last_car.ratings
    last_car.name, last_car.ratings = best.name, best.rating

    teams, player, player_2, DRIVER_1, DRIVER_2, cars = trading_at_the_of_season(
        teams, player, player_2, DRIVER_1, DRIVER_2, cars
    )
    WETTINESS, cars, teams = reset_championship(cars, teams)

    save_state_end_of_season(cars, teams, season_count)
    return {"status": "championship_done", "season": season_count}