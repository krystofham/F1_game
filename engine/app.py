from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os, json, random
from fastapi.staticfiles import StaticFiles  
from big_functions import *
from load_data_json import *

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

_CONFIG = os.path.dirname(os.path.abspath(__file__))

app.mount("/img", StaticFiles(directory="../img"), name="img") 

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_game_objects():
    from init import (
        cars, teams, player, player_2, championship, tracks,
        DRIVER_1, DRIVER_2, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING
    )
    state = load_state()
    b = state.get("b", 1)
    season_count = state.get("season_count", 1)
    
    # Přidej toto:
    DRIVER_1 = state.get("DRIVER_1", DRIVER_1)
    DRIVER_2 = state.get("DRIVER_2", DRIVER_2)
    
    return cars, teams, player, player_2, championship, tracks, \
           DRIVER_1, DRIVER_2, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count
def _load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def _state():
    try:
        with open(f"state.json", "r") as input_file:
            data = json.load(input_file)
        return data
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
    state = _state()
    return state["drivers"]

@app.get("/api/get_teams")
async def get_teams():
    state = _state()
    return state["teams"]

@app.get("/api/get_teams/{team_name}")
async def get_team(team_name: str):
    state = _state()
    teams = state["teams"]
    for team in teams:
        if team["name"].lower() == team_name.lower():
            return team
    raise HTTPException(status_code=404, detail=f"Team '{team_name}' not found")


@app.post("/api/init_race")
async def api_init_race():
    cars, teams, player, player_2, championship, tracks, \
    DRIVER_1, DRIVER_2, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count = load_game_objects()

    speed_bonus, season_count, time_laps, k_speed, k_wear, training_type, \
    WETTINESS, lap, forecast, weather, climax, pneu, speed, PNEU_types, \
    weather_1, weather_2, weather_3, weather_4, weather_actual = init_race(
        tracks, championship[b - 1], cars, teams, championship,
        player, player_2, b, season_count
    )

    race = championship[b - 1]
    track = next((t for t in tracks if t.name == race), None)
    total_laps = track.laps if track else 67

    state = _state()
    state["lap"] = 0
    state["time_laps"] = []
    state["race"] = getattr(race, "name", str(race))
    state["b"] = b                          # ← zachovej b
    state["season_count"] = season_count    # ← zachovej season_count
    state["championship_length"] = len(championship)  # ← zachovej délku
    state["race_state"] = {
        "total_laps": total_laps,
        "climax": climax,
        "weather": weather_actual,
        "forecast": forecast,
        "wettiness": WETTINESS,
        "pneu_type": pneu,
        "speed_type": speed,
        "training_type": training_type,
        "speed_bonus": speed_bonus,
        "k_wear": k_wear,
        "k_speed": k_speed
    }

    with open("state.json", "w", encoding="utf-8") as out_file:
        json.dump(state, out_file, indent=4, ensure_ascii=False)

    return {
        "status": "ok",
        "race": state["race"],
        "lap": state["lap"],
        "total_laps": total_laps
    }

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

    # time_laps se čte ze root úrovně state.json (ne z race_ctx)
    time_laps = state.get("time_laps", [])
    race = state.get("race", "Unknown Race")

    k_speed = race_ctx.get("k_speed", [1, 1.04, 1.08, 0.6, 0.65])

    lap, cars, teams = sim_the_lap(
        cars, teams, player, player_2, lap,
        SAFETY_CAR, LAPS_REMAINING,
        race_ctx["wettiness"], race_ctx["forecast"], race_ctx["weather"],
        race_ctx["total_laps"], race_ctx["climax"],
        DRIVER_1, DRIVER_2,
        race_ctx["pneu_type"], race_ctx["speed_type"],
        {
            "hard":   {"wear": race_ctx["k_wear"][0], "speed": k_speed[0]},
            "medium": {"wear": race_ctx["k_wear"][1], "speed": k_speed[1]},
            "soft":   {"wear": race_ctx["k_wear"][2], "speed": k_speed[2]},
            "wet":    {"wear": race_ctx["k_wear"][3], "speed": k_speed[3]},
            "inter":  {"wear": race_ctx["k_wear"][4], "speed": k_speed[4]},
        },
        race_ctx["forecast"][0] if len(race_ctx["forecast"]) > 0 else race_ctx["weather"],
        race_ctx["forecast"][1] if len(race_ctx["forecast"]) > 1 else race_ctx["weather"],
        race_ctx["forecast"][2] if len(race_ctx["forecast"]) > 2 else race_ctx["weather"],
        race_ctx["forecast"][3] if len(race_ctx["forecast"]) > 3 else race_ctx["weather"],
        race_ctx["training_type"], race_ctx["k_wear"], k_speed,
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
    race = state.get("race", "Unknown Race")
    climax = race_ctx.get("climax", "sunny")

    teams, cars, time_laps = post_race_info(time_laps, player, player_2, cars, teams, COUNT_CARS)
    save_state_end_of_race(cars, teams, season_count, race, time_laps)
    lap, time_laps, SAFETY_CAR, LAPS_REMAINING, weather, forecast, cars, WETTINESS = reset_race(climax, cars)

    new_b = b + 1
    championship_length = len(championship)
    # Zapiš nové b do state
    updated_state = _state()
    updated_state["b"] = new_b
    updated_state["season_count"] = season_count
    updated_state["championship_length"] = championship_length
    with open("state.json", "w", encoding="utf-8") as f:
        json.dump(updated_state, f, indent=4, ensure_ascii=False)

    # Konec šampionátu?
    if new_b > championship_length:
        return {"status": "race_done", "race": race, "championship_finished": True}

    return {"status": "race_done", "race": race, "championship_finished": False}
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

    worst.name   = random.choice(names_free_drivers)
    worst.rating = random.uniform(0.95, 1.05)

    cars.sort(key=lambda x: x.points, reverse=True)
    last_car = cars[-1]

    if last_car.is_player:
        old_best_name   = best.name
        old_best_rating = best.rating
        if DRIVER_1 == last_car.name:
            DRIVER_1       = old_best_name
            player.name    = old_best_name
            player.ratings = old_best_rating
        elif DRIVER_2 == last_car.name:
            DRIVER_2         = old_best_name
            player_2.name    = old_best_name
            player_2.ratings = old_best_rating

    teams, player, player_2, DRIVER_1, DRIVER_2, cars = trading_at_the_of_season(
        teams, player, player_2, DRIVER_1, DRIVER_2, cars
    )

    WETTINESS, cars, teams = reset_championship(cars, teams)

    updated_state = _state()
    updated_state["b"] = 1
    updated_state["season_count"] = season_count
    updated_state["championship_length"] = len(championship)
    with open("state.json", "w", encoding="utf-8") as f:
        json.dump(updated_state, f, indent=4, ensure_ascii=False)

    save_state_end_of_season(cars, teams, season_count)

    return {"status": "championship_done", "season": season_count}

# LAP USER DATA ENDPOINT
@app.post("/api/set_lap_user_data")
async def api_set_lap_user_data(data: dict):
    path = os.path.join(_CONFIG, "../engine/user_input/lap_user_data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return {"status": "ok"}


# Tranfers
@app.get("/api/get_transfer_offers")
async def api_get_transfer_offers():
    cars, teams, player, player_2, championship, tracks, \
    DRIVER_1, DRIVER_2, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count = load_game_objects()

    average_rating = sum(x.ratings for x in cars) / (len(cars) + 1)

    def build_offers(player_obj):
        offers = []
        if average_rating > player_obj.ratings:
            # slabý hráč — jen 1 nabídka
            t = teams[-1]
            d = t.drivers[random.choice([0, 1])]
            offers.append({"name": d.name, "team": t.name, "points": t.points, "rating": round(d.ratings, 4)})
        else:
            for t in teams:
                if random.uniform(0, 1) > 0.7:
                    d = t.drivers[random.choice([0, 1])]
                    if not d.is_player:
                        offers.append({"name": d.name, "team": t.name, "points": t.points, "rating": round(d.ratings, 4)})
            for t in teams:
                if len(t.drivers) >= 1 and not t.drivers[0].is_player and (t.rating - t.drivers[0].ratings) >= 0:
                    d = t.drivers[0]
                    offers.append({"name": d.name, "team": t.name, "points": t.points, "rating": round(d.ratings, 4)})
                if len(t.drivers) >= 2 and not t.drivers[1].is_player and (t.rating - t.drivers[1].ratings) >= 0:
                    d = t.drivers[1]
                    offers.append({"name": d.name, "team": t.name, "points": t.points, "rating": round(d.ratings, 4)})
        # deduplikace
        seen = set()
        unique = []
        for o in offers:
            if o["name"] not in seen:
                seen.add(o["name"])
                unique.append(o)
        return unique

    result = {
        "driver_1": {"name": DRIVER_1, "offers": build_offers(player)},
        "driver_2": {"name": DRIVER_2, "offers": build_offers(player_2)},
        "mmr2_best": None
    }

    # MMR2 nabídka
    try:
        best, _ = simulate_season_mmr2(list_drivers_mmr2)
        result["mmr2_best"] = {"name": best.name, "rating": round(best.rating, 4)}
    except:
        pass

    path = os.path.join(_CONFIG, "../engine/user_input/transfer_offers.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return result


@app.post("/api/do_transfer")
async def api_do_transfer(data: dict):
    # data: {"want": "yes"/"no", "where": "MMR1"/"MMR2", "pilot_to_change": "...", "chosen_pilot": "..."}
    path_deal = os.path.join(_CONFIG, "../engine/user_input/deal.json")
    path_transfer = os.path.join(_CONFIG, "../engine/user_input/transfer.json")

    with open(path_deal, "w", encoding="utf-8") as f:
        json.dump({"want": data.get("want", "yes"), "where": data.get("where"), "pilot_to_change": data.get("pilot_to_change"), "chosen_pilot": data.get("chosen_pilot", "")}, f, indent=2)
    with open(path_transfer, "w", encoding="utf-8") as f:
        json.dump({"pilot_to_change": data.get("pilot_to_change"), "chosen_pilot": data.get("chosen_pilot", "")}, f, indent=2)

    cars, teams, player, player_2, championship, tracks, \
    DRIVER_1, DRIVER_2, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count = load_game_objects()

    try:
        player, player_2, DRIVER_1, DRIVER_2, cars = transfer(
            cars, teams, player, player_2, DRIVER_1, DRIVER_2
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    save_state_end_of_season(cars, teams, season_count)
    updated_state = _state()
    updated_state["DRIVER_1"] = DRIVER_1
    updated_state["DRIVER_2"] = DRIVER_2
    with open("state.json", "w", encoding="utf-8") as f:
        json.dump(updated_state, f, indent=2, ensure_ascii=False)
    return {"status": "ok", "driver_1": DRIVER_1, "driver_2": DRIVER_2}