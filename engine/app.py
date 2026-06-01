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
def load_game_objects(apply_state=True):
    from init import cars, teams, championship, tracks, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING
    state = load_state()
    b = state.get("b", 1)
    season_count = state.get("season_count", 1)

    if apply_state:
        state_drivers = state.get("drivers", [])

        # Deduplikace player záznamů
        seen_player_names = set()
        clean_drivers = []
        for d in state_drivers:
            if d.get("is_player"):
                if d["name"] not in seen_player_names:
                    seen_player_names.add(d["name"])
                    clean_drivers.append(d)
            else:
                clean_drivers.append(d)

        state_players = [d for d in clean_drivers if d.get("is_player")]
        state_ai      = [d for d in clean_drivers if not d.get("is_player")]

        # Hráčská auta — matchuj podle pořadí is_player, ne jména
        player_cars = [c for c in cars if c.is_player]
        for car, d in zip(player_cars, state_players):
            car.name      = d["name"]
            car.ratings   = d.get("rating", car.ratings)
            car.time      = d.get("time", 0.0)
            car.wear      = d.get("wear", 0.0)
            car.pneu      = d.get("pneu", car.pneu)
            car.drs       = d.get("drs", False)
            car.pit       = d.get("pit", False)
            car.dnf       = d.get("dnf", False)
            car.box       = d.get("pit_stops", 0)
            car.position  = d.get("position_history", [])
            car.stints    = d.get("stints", [])
            car.points    = d.get("points", car.points)
            car.is_player = True

        # AI auta — matchuj podle jména
        ai_state_by_name = {d["name"]: d for d in state_ai}
        for car in cars:
            if car.is_player:
                continue
            d = ai_state_by_name.get(car.name)
            if not d:
                continue
            car.ratings   = d.get("rating", car.ratings)
            car.time      = d.get("time", 0.0)
            car.wear      = d.get("wear", 0.0)
            car.pneu      = d.get("pneu", car.pneu)
            car.drs       = d.get("drs", False)
            car.pit       = d.get("pit", False)
            car.dnf       = d.get("dnf", False)
            car.box       = d.get("pit_stops", 0)
            car.position  = d.get("position_history", [])
            car.stints    = d.get("stints", [])
            car.is_player = False
            car.points    = d.get("points", car.points)

    race_ctx       = state.get("race_state", {})
    SAFETY_CAR     = race_ctx.get("safety_car", SAFETY_CAR)
    LAPS_REMAINING = race_ctx.get("safety_car_laps_remaining", LAPS_REMAINING)

    p1_name = state.get("player.name")
    p2_name = state.get("player_2.name")
    player_cars = [c for c in cars if c.is_player]

    player   = next((c for c in player_cars if c.name == p1_name), player_cars[0] if player_cars else None)
    player_2 = next((c for c in player_cars if c.name == p2_name), player_cars[1] if len(player_cars) > 1 else None)

    return cars, teams, player, player_2, championship, tracks, \
           player.name, player_2.name, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count


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

def _clear_user_input():
    """Vymaže obsah všech souborů ve složce user_input."""
    folder = os.path.join(_CONFIG, "../engine/user_input")
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump({}, f)


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
async def  get_team(team_name: str):
    state = _state()
    teams = state["teams"]
    for team in teams:
        if team["name"].lower() == team_name.lower():
            return team
    raise HTTPException(status_code=404, detail=f"Team '{team_name}' not found")


@app.post("/api/init_race")
async def api_init_race():
    cars, teams, player, player_2, championship, tracks, \
    player.name, player_2.name, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count = load_game_objects(apply_state=False)

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
    state["player.name"] = player.name
    state["player_2.name"] = player_2.name
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
    player.name, player_2.name, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count = load_game_objects()

    # time_laps se čte ze root úrovně state.json (ne z race_ctx)
    time_laps = state.get("time_laps", [])
    race = state.get("race", "Unknown Race")

    k_speed = race_ctx.get("k_speed", [1, 1.04, 1.08, 0.6, 0.65])

    lap, cars, teams = sim_the_lap(
        cars, teams, player, player_2, lap,
        SAFETY_CAR, LAPS_REMAINING,
        race_ctx["wettiness"], race_ctx["forecast"], race_ctx["weather"],
        race_ctx["total_laps"], race_ctx["climax"],
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
    player.name, player_2.name, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count = load_game_objects()

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
        player.name, player_2.name, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count = load_game_objects()

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
        if player.name == last_car.name:
            player.name    = old_best_name
            player.ratings = old_best_rating
        elif player_2.name == last_car.name:
            player_2.name    = old_best_name
            player_2.ratings = old_best_rating

    teams, player, player_2, player.name, player_2.name, cars = trading_at_the_of_season(
        teams, player, player_2, cars
    )

    save_state_end_of_season(cars, teams, season_count)  # ← před resetem, se správnými body

    WETTINESS, cars, teams = reset_championship(cars, teams)

    updated_state = _state()
    updated_state["b"] = 1
    updated_state["season_count"] = season_count
    updated_state["championship_length"] = len(championship)
    updated_state["player.name"] = player.name      # ← přidáno
    updated_state["player_2.name"] = player_2.name  # ← přidáno
    with open("state.json", "w", encoding="utf-8") as f:
        json.dump(updated_state, f, indent=4, ensure_ascii=False)

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
    state = _state()
    drivers = state.get("drivers", [])
    players = [d for d in drivers if d.get("is_player")]

    # MMR1 nabídky – AI driverů ze state.json
    ai_drivers = [d for d in drivers if not d.get("is_player")]
    offers_pool = [{"name": d["name"], "team": d.get("team","?"), "points": d.get("points",0), "rating": round(d.get("rating",1.0),4)} for d in ai_drivers]
    random.shuffle(offers_pool)

    result = {
        "driver_1": {"name": players[0]["name"] if len(players)>0 else "", "offers": offers_pool[:5]},
        "driver_2": {"name": players[1]["name"] if len(players)>1 else "", "offers": offers_pool[5:10]},
        "mmr2_best": None
    }

    # MMR2
    try:
        from engine.mmr2 import simulate_season_mmr2, list_drivers_mmr2
        best, _ = simulate_season_mmr2(list_drivers_mmr2)
        result["mmr2_best"] = {"name": best.name, "rating": round(best.rating, 4)}
    except:
        pass

    return result

@app.post("/api/do_transfer")
async def api_do_transfer(data: dict):
    pilot_to_change = data.get("pilot_to_change")
    chosen_pilot    = data.get("chosen_pilot")
    new_rating      = data.get("rating", None)

    if not pilot_to_change or not chosen_pilot:
        raise HTTPException(status_code=400, detail="Missing pilot names")

    state = _state()
    drivers = state.get("drivers", [])

    p1_name = state.get("player.name", "")
    p2_name = state.get("player_2.name", "")

    if pilot_to_change not in (p1_name, p2_name):
        raise HTTPException(status_code=400, detail=f"'{pilot_to_change}' is not a player driver")

    # 1. Nejdřív uprav hráčský záznam IN-PLACE (ještě ve starém listu)
    target = next((d for d in drivers if d["name"] == pilot_to_change and d.get("is_player")), None)
    if not target:
        raise HTTPException(status_code=404, detail=f"Player driver '{pilot_to_change}' not found")

    target["name"] = chosen_pilot
    if new_rating is not None:
        target["rating"] = new_rating

    # 2. Teprve pak odstraň AI duplikát (target už má nové jméno, takže ho filtr neodstraní)
    state["drivers"] = [
        d for d in drivers
        if not (d["name"] == chosen_pilot and not d.get("is_player"))
    ]

    # 3. Aktualizuj root player.name / player_2.name
    if pilot_to_change == p1_name:
        state["player.name"] = chosen_pilot
    elif pilot_to_change == p2_name:
        state["player_2.name"] = chosen_pilot

    # 4. Aktualizuj teams
    for team in state.get("teams", []):
        team["drivers"] = [
            chosen_pilot if d == pilot_to_change else d
            for d in team.get("drivers", [])
        ]

    with open("state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4, ensure_ascii=False)
    _clear_user_input()
    return {
        "status": "ok",
        "driver_1": state.get("player.name", ""),
        "driver_2": state.get("player_2.name", ""),
    }

@app.post("/api/sim_race")
async def api_sim_race():
    """
    Odsimuluje celý závod najednou. Volá se místo opakovaného /api/sim_lap.
    """
    state = _state()
    race_ctx = state.get("race_state")
    if not race_ctx:
        raise HTTPException(status_code=400, detail="Race not initialized. Call /api/init_race first.")

    total_laps = race_ctx["total_laps"]

    cars, teams, player, player_2, championship, tracks, \
    player.name, player_2.name, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count = load_game_objects()

    time_laps = state.get("time_laps", [])
    race = state.get("race", "Unknown Race")
    k_speed = race_ctx.get("k_speed", [1, 1.04, 1.08, 0.6, 0.65])

    tyre_compounds = {
        "hard":   {"wear": race_ctx["k_wear"][0], "speed": k_speed[0]},
        "medium": {"wear": race_ctx["k_wear"][1], "speed": k_speed[1]},
        "soft":   {"wear": race_ctx["k_wear"][2], "speed": k_speed[2]},
        "wet":    {"wear": race_ctx["k_wear"][3], "speed": k_speed[3]},
        "inter":  {"wear": race_ctx["k_wear"][4], "speed": k_speed[4]},
    }

    lap = state.get("lap", 0)
    lap_snapshots = []

    # ── Jediná smyčka, žádné I/O uvnitř ──────────────────────────────────
    while lap <= total_laps:
        lap, cars, teams = sim_the_lap(
            cars, teams, player, player_2, lap,
            SAFETY_CAR, LAPS_REMAINING,
            race_ctx["wettiness"], race_ctx["forecast"], race_ctx["weather"],
            total_laps, race_ctx["climax"],
            race_ctx["pneu_type"], race_ctx["speed_type"],
            tyre_compounds,
            race_ctx["forecast"][0] if len(race_ctx["forecast"]) > 0 else race_ctx["weather"],
            race_ctx["forecast"][1] if len(race_ctx["forecast"]) > 1 else race_ctx["weather"],
            race_ctx["forecast"][2] if len(race_ctx["forecast"]) > 2 else race_ctx["weather"],
            race_ctx["forecast"][3] if len(race_ctx["forecast"]) > 3 else race_ctx["weather"],
            race_ctx["training_type"], race_ctx["k_wear"], k_speed,
            race_ctx["speed_bonus"], season_count, race, time_laps
        )

        # Snapshot stavu po každém kole (pro frontend animaci)
        current_state = _state()
        lap_snapshots.append({
            "lap": lap,
            "drivers": current_state.get("drivers", []),
            "time_laps": current_state.get("time_laps", []),
        })

        if lap > total_laps:
            break

    # Jeden finální zápis stavu
    final_state = _state()

    return {
        "status": "ok",
        "finished": True,
        "total_laps": total_laps,
        "snapshots": lap_snapshots,   # React může animovat kolo po kole lokálně
        "final_state": final_state,
    }

@app.post("/api/sim_until")
async def api_sim_until(data: dict):
    target_lap = data.get("lap", 1)
    state = _state()
    race_ctx = state.get("race_state")
    if not race_ctx:
        raise HTTPException(status_code=400, detail="Race not initialized.")

    total_laps = race_ctx["total_laps"]
    cars, teams, player, player_2, championship, tracks, \
    player.name, player_2.name, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count = load_game_objects()

    time_laps = state.get("time_laps", [])
    race = state.get("race", "Unknown Race")
    k_speed = race_ctx.get("k_speed", [1, 1.04, 1.08, 0.6, 0.65])
    tyre_compounds = {
        "hard":   {"wear": race_ctx["k_wear"][0], "speed": k_speed[0]},
        "medium": {"wear": race_ctx["k_wear"][1], "speed": k_speed[1]},
        "soft":   {"wear": race_ctx["k_wear"][2], "speed": k_speed[2]},
        "wet":    {"wear": race_ctx["k_wear"][3], "speed": k_speed[3]},
        "inter":  {"wear": race_ctx["k_wear"][4], "speed": k_speed[4]},
    }

    lap = state.get("lap", 0)
    lap_snapshots = []

    while lap < target_lap and lap <= total_laps:
        current_race_ctx = _state().get("race_state", race_ctx)
        forecast = current_race_ctx.get("forecast", race_ctx["forecast"])
        SAFETY_CAR = current_race_ctx.get("safety_car", False)
        LAPS_REMAINING = current_race_ctx.get("safety_car_laps_remaining", 0)

        lap, cars, teams = sim_the_lap(
            cars, teams, player, player_2, lap,
            SAFETY_CAR, LAPS_REMAINING,
            current_race_ctx["wettiness"], forecast, current_race_ctx["weather"],
            total_laps, current_race_ctx["climax"],
            current_race_ctx["pneu_type"], current_race_ctx["speed_type"],
            tyre_compounds,
            forecast[0] if len(forecast) > 0 else current_race_ctx["weather"],
            forecast[1] if len(forecast) > 1 else current_race_ctx["weather"],
            forecast[2] if len(forecast) > 2 else current_race_ctx["weather"],
            forecast[3] if len(forecast) > 3 else current_race_ctx["weather"],
            current_race_ctx["training_type"], current_race_ctx["k_wear"], k_speed,
            current_race_ctx["speed_bonus"], season_count, race, time_laps
        )
        current_state = _state()
        lap_snapshots.append({"lap": lap, "drivers": current_state.get("drivers", [])})

    final_state = _state()
    return {
        "status": "ok",
        "lap": lap,
        "total_laps": total_laps,
        "finished": lap >= total_laps,
        "snapshots": lap_snapshots,
        "final_state": final_state,
    }