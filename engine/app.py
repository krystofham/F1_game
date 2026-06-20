from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os, json, random, traceback
from fastapi.staticfiles import StaticFiles  
from big_functions import *
from load_data_json import *
from log import elog, ilog, wlog, dlog, log, snapshot_state as td_snapshot_state
from log import snapshot_cars as td_snapshot_cars
from saving import save_season_csv, save_race_csv, update_track_record


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

_CONFIG = os.path.dirname(os.path.abspath(__file__))
ilog(fn="app_startup", msg="FastAPI started", config_dir=_CONFIG)

app.mount("/img", StaticFiles(directory="../img"), name="img")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _resolve_driver_car(driver_name, player_by_name, ai_by_name, player_names, is_player_slot):
    """Najde správný Car objekt — hráč vs. AI u stejného jména po transferu."""
    if is_player_slot and driver_name in player_by_name:
        return player_by_name[driver_name]
    if driver_name in ai_by_name and driver_name not in player_names:
        return ai_by_name[driver_name]
    if driver_name in player_by_name:
        return player_by_name[driver_name]
    if driver_name in ai_by_name:
        return ai_by_name[driver_name]
    return None


def _remove_shadow_duplicate_cars(cars, player_names):
    """Init má AI jezdce stejného jména jako hráč po transferu — bez týmu a duplicitní."""
    for car in list(cars):
        if car.team is None and not car.is_player and car.name in player_names:
            cars.remove(car)


def apply_teams_from_state(cars, teams, state_teams, state_drivers=None):
    """Synchronizuje in-memory týmy podle state.json. Při neshodě vrátí False."""
    if not state_teams:
        wlog(fn="apply_teams_from_state", msg="state_teams empty, skipping")
        return False

    player_by_name = {c.name: c for c in cars if c.is_player}
    player_names   = set(player_by_name)
    ai_by_name     = {}
    for c in cars:
        if not c.is_player:
            ai_by_name.setdefault(c.name, c)

    is_player_slot = {}
    for d in state_drivers or []:
        name = d["name"]
        if d.get("is_player"):
            is_player_slot[name] = True
        elif name not in is_player_slot:
            is_player_slot[name] = False

    team_by_name = {t.name: t for t in teams}
    assignments  = []
    used_car_ids = set()

    for st in state_teams:
        team = team_by_name.get(st.get("name"))
        if not team:
            continue
        for driver_name in st.get("drivers", []):
            car = _resolve_driver_car(
                driver_name, player_by_name, ai_by_name, player_names,
                is_player_slot.get(driver_name, False),
            )
            if car is None or id(car) in used_car_ids:
                elog(
                    fn="apply_teams_from_state",
                    msg="driver resolution failed, aborting team apply",
                    driver=driver_name,
                    team=st.get("name"),
                    reason="no_car" if car is None else "duplicate_car",
                    is_player_slot=is_player_slot.get(driver_name, False),
                    player_names=sorted(player_names),
                )
                return False
            assignments.append((team, car))
            used_car_ids.add(id(car))

    if not assignments:
        elog(fn="apply_teams_from_state", msg="no assignments built, aborting")
        return False

    for t in teams:
        t.drivers = []
    for car in cars:
        car.team = None
    for team, car in assignments:
        team.pridej_jezdce(car)

    removed = []
    for car in list(cars):
        if car.team is None and not car.is_player and car.name in player_names:
            removed.append(car.name)
    _remove_shadow_duplicate_cars(cars, player_names)

    if removed:
        wlog(fn="apply_teams_from_state", msg="shadow duplicates removed after apply", names=removed)

    ilog(fn="apply_teams_from_state", msg="teams applied ok", assignment_count=len(assignments))
    return True


def _apply_driver_dict_to_car(car, d):
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


def _apply_ai_driver_dict_to_car(car, d):
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
    car.is_player = False
    car.points    = d.get("points", car.points)


def _sync_ai_cars_with_state(cars, state_ai, player_names):
    """
    Namapuje AI auta na state AI i když došlo k přejmenování
    (např. Johan -> player, Max -> AI).
    """
    ai_cars    = [c for c in cars if not c.is_player]
    ai_by_name = {}
    for c in ai_cars:
        ai_by_name.setdefault(c.name, []).append(c)

    matched_car_ids = set()
    unmatched_state = []

    for d in state_ai:
        pool   = ai_by_name.get(d["name"], [])
        chosen = next((c for c in pool if id(c) not in matched_car_ids), None)
        if chosen is None:
            unmatched_state.append(d)
            continue
        _apply_ai_driver_dict_to_car(chosen, d)
        matched_car_ids.add(id(chosen))

    free_ai_cars = [c for c in ai_cars if id(c) not in matched_car_ids]
    for d in unmatched_state:
        if not free_ai_cars:
            elog(fn="_sync_ai_cars_with_state", msg="no free AI cars left for unmatched state entry", missing_name=d["name"])
            break
        idx    = next((i for i, c in enumerate(free_ai_cars) if c.name in player_names), 0)
        chosen = free_ai_cars.pop(idx)
        old_name = chosen.name
        _apply_ai_driver_dict_to_car(chosen, d)
        ilog(fn="_sync_ai_cars_with_state", msg="AI car renamed during sync (transfer side effect)",
             old_name=old_name, new_name=d["name"])


def load_game_objects(apply_state=True):
    from init import cars, teams, championship, tracks, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING
    from init import player as init_player, player_2 as init_player_2

    state        = load_state()
    b            = state.get("b", 1)
    season_count = state.get("season_count", 1)

    if apply_state:
        state_drivers = state.get("drivers", [])

        # Deduplikace player záznamů
        seen_player_names = set()
        clean_drivers     = []
        for d in state_drivers:
            if d.get("is_player"):
                if d["name"] not in seen_player_names:
                    seen_player_names.add(d["name"])
                    clean_drivers.append(d)
            else:
                clean_drivers.append(d)

        state_players_by_name = {d["name"]: d for d in clean_drivers if d.get("is_player")}
        state_ai              = [d for d in clean_drivers if not d.get("is_player")]

        p1_name = state.get("player.name", "")
        p2_name = state.get("player_2.name", "")

        slot_map = ((init_player, p1_name), (init_player_2, p2_name))
        for car, expected_name in slot_map:
            if not expected_name:
                wlog(fn="load_game_objects", msg="player.name key empty, skipping slot", slot=car.name)
                continue
            d = state_players_by_name.get(expected_name)
            if d:
                before = car.name
                _apply_driver_dict_to_car(car, d)
                if before != car.name:
                    ilog(fn="load_game_objects", msg="player slot renamed (transfer applied)",
                         slot_init=before, expected=expected_name, applied=car.name)
            else:
                elog(fn="load_game_objects", msg="player not found in state drivers — transfer mismatch?",
                     slot_init=car.name, expected=expected_name,
                     available_players=list(state_players_by_name.keys()))

        _sync_ai_cars_with_state(cars, state_ai, {p1_name, p2_name})

        teams_ok = apply_teams_from_state(cars, teams, state.get("teams", []), clean_drivers)
        if not teams_ok:
            wlog(fn="load_game_objects", msg="apply_teams_from_state failed, keeping init.py teams",
                 snapshot=td_snapshot_state(state, "after_failed_apply"))

        ilog(fn="load_game_objects", msg="state applied",
             teams_from_state=teams_ok,
             state_snapshot=td_snapshot_state(state, "load"),
             cars_snapshot=td_snapshot_cars(cars, init_player, init_player_2))

    race_ctx       = state.get("race_state", {})
    SAFETY_CAR     = race_ctx.get("safety_car", SAFETY_CAR)
    LAPS_REMAINING = race_ctx.get("safety_car_laps_remaining", LAPS_REMAINING)

    p1_name     = state.get("player.name")
    p2_name     = state.get("player_2.name")
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
        with open("state.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        wlog(fn="_state", msg="state.json not found, returning empty dict")
        return {}
    except json.JSONDecodeError as e:
        elog(fn="_state", msg="state.json is malformed JSON", error=str(e))
        return {}


def _write_state(state: dict, caller: str) -> None:
    """Centralizovaný zápis state.json — jedno místo, jeden log."""
    try:
        with open("state.json", "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4, ensure_ascii=False)
        ilog(fn=caller, msg="state.json written ok")
    except OSError as e:
        elog(fn=caller, msg="state.json write failed", error=str(e))
        raise HTTPException(status_code=500, detail="Nelze uložit stav hry.")


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
    return _state()["drivers"]


@app.get("/api/get_teams")
async def get_teams():
    return _state()["teams"]


@app.get("/api/get_teams/{team_name}")
async def get_team(team_name: str):
    state = _state()
    for team in state["teams"]:
        if team["name"].lower() == team_name.lower():
            return team
    raise HTTPException(status_code=404, detail=f"Team '{team_name}' not found")


# ---------------------------------------------------------------------------
# POST /api/init_race
# ---------------------------------------------------------------------------

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

    race       = championship[b - 1]
    track      = next((t for t in tracks if t.name == race), None)
    total_laps = track.laps if track else 67

    if not track:
        elog(fn="api_init_race", msg="track not found in database, fallback laps=67 used — THIS IS A BUG",
             race=race, fallback_laps=67)
    
    # time_laps se resetuje na [] při init — logujeme explicitně
    # protože time_laps persistence je historicky problematická
    ilog(fn="api_init_race", msg="time_laps reset to [] for new race",
         race=getattr(race, "name", str(race)), b=b)

    state = _state()
    state["smt_happened"]       = False
    state["lap"]                = 0
    state["time_laps"]          = []   # ← reset při každém novém závodě
    state["race"]               = getattr(race, "name", str(race))
    state["b"]                  = b
    state["season_count"]       = season_count
    state["player.name"]        = player.name
    state["player_2.name"]      = player_2.name
    state["championship_length"] = len(championship)
    state["race_state"] = {
        "total_laps":    total_laps,
        "climax":        climax,
        "weather":       weather_actual,
        "forecast":      forecast,
        "wettiness":     WETTINESS,
        "pneu_type":     pneu,
        "speed_type":    speed,
        "training_type": training_type,
        "speed_bonus":   speed_bonus,
        "k_wear":        k_wear,
        "k_speed":       k_speed,
    }

    ilog(fn="api_init_race", msg="race initialized",
         race=state["race"], total_laps=total_laps,
         weather=weather_actual, forecast=forecast,
         pneu_p1=pneu, training=training_type, b=b, season=season_count)

    _write_state(state, "api_init_race")

    return {"status": "ok", "race": state["race"], "lap": state["lap"], "total_laps": total_laps}


# ---------------------------------------------------------------------------
# POST /api/sim_lap
# ---------------------------------------------------------------------------

@app.post("/api/sim_lap")
async def api_sim_lap():
    state    = _state()
    race_ctx = state.get("race_state")

    if not race_ctx:
        elog(fn="api_sim_lap", msg="race_state missing, init_race not called")
        raise HTTPException(status_code=400, detail="Race not initialized. Call /api/init_race first.")

    lap = state["lap"]
    if lap > race_ctx["total_laps"]:
        wlog(fn="api_sim_lap", msg="sim_lap called after race finished", lap=lap, total=race_ctx["total_laps"])
        raise HTTPException(status_code=400, detail="Race already finished. Call /api/post_race.")

    # --- time_laps guard ---
    time_laps = state.get("time_laps")
    if time_laps is None:
        elog(fn="api_sim_lap", msg="time_laps key missing from state.json entirely — init_race may not have run",
             lap=lap)
        time_laps = []
    elif time_laps == [] and lap > 0:
        # Kolo > 0 ale time_laps prázdné = data se ztratila (save bug nebo předčasný reset)
        elog(fn="api_sim_lap", msg="time_laps is empty but lap > 0 — data loss suspected",
             lap=lap, total_laps=race_ctx["total_laps"])
    else:
        dlog(fn="api_sim_lap", msg="time_laps loaded", lap=lap, time_laps_count=len(time_laps))

    race    = state.get("race")
    k_speed = race_ctx.get("k_speed")

    if not race:
        wlog(fn="api_sim_lap", msg="race key missing from state, using fallback", fallback="Unknown Race")
        race = "Unknown Race"
    if not k_speed:
        wlog(fn="api_sim_lap", msg="k_speed missing from race_state, using hardcoded fallback")
        k_speed = [1, 1.04, 1.08, 0.6, 0.65]

    cars, teams, player, player_2, championship, tracks, \
    player.name, player_2.name, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count = load_game_objects()

    try:
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
    except Exception as e:
        elog(fn="api_sim_lap", msg="sim_the_lap raised exception", error=str(e), lap=lap, race=race)
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    new_state  = _state()
    new_time_laps = new_state.get("time_laps", [])

    # Ověř že sim_the_lap skutečně zapsal time_laps zpět do state.json
    if len(new_time_laps) == 0 and lap > 0:
        elog(fn="api_sim_lap", msg="time_laps still empty after sim_the_lap — sim did not write state",
             lap=lap, race=race)
    else:
        dlog(fn="api_sim_lap", msg="lap simmed ok",
             lap=lap, time_laps_count=len(new_time_laps))

    return {
        "status":     "ok",
        "lap":        new_state["lap"],
        "total_laps": race_ctx["total_laps"],
        "finished":   new_state["lap"] > race_ctx["total_laps"],
    }


# ---------------------------------------------------------------------------
# POST /api/post_race
# ---------------------------------------------------------------------------

@app.post("/api/post_race")
async def api_post_race():
    state    = _state()
    race_ctx = state.get("race_state", {})

    if not race_ctx:
        elog(fn="api_post_race", msg="race_state missing from state.json")

    cars, teams, player, player_2, championship, tracks, \
    player.name, player_2.name, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count = load_game_objects()

    race = state.get("race")
    if not race:
        wlog(fn="api_post_race", msg="race key missing from state, using fallback")
        race = "Unknown Race"

    # --- time_laps guard ---
    time_laps = state.get("time_laps")
    if time_laps is None:
        elog(fn="api_post_race", msg="time_laps key missing entirely from state.json",
             race=race, season=season_count)
        time_laps = []
    elif time_laps == []:
        elog(fn="api_post_race", msg="time_laps is empty at post_race — race results will be incomplete",
             race=race, season=season_count,
             total_laps=race_ctx.get("total_laps"), current_lap=state.get("lap"))
    else:
        ilog(fn="api_post_race", msg="time_laps loaded for post_race",
             race=race, time_laps_count=len(time_laps))

    climax = race_ctx.get("climax", "sunny")
    if "climax" not in race_ctx:
        wlog(fn="api_post_race", msg="climax missing from race_state, using fallback 'sunny'")

    teams, cars, time_laps = post_race_info(time_laps, player, player_2, cars, teams, COUNT_CARS)
    save_state_end_of_race(cars, teams, season_count, race, time_laps)
    
    state_for_csv = _state()
    save_race_csv(
        drivers=state_for_csv.get("drivers", []),
        race=race,
        season=season_count,
        race_ctx=race_ctx,
    )

    record_broken = update_track_record(
        time_laps=state.get("time_laps", []),
        track=race,
        season=season_count,
    )
    if record_broken:
        ilog(fn="api_post_race", msg="new track record set", race=race)
    
    
    
    lap, time_laps, SAFETY_CAR, LAPS_REMAINING, weather, forecast, cars, WETTINESS = reset_race(climax, cars)

    # Ověř že time_laps byl správně uložen save_state_end_of_race
    check_state = _state()
    saved_time_laps = check_state.get("time_laps", [])
    if saved_time_laps == [] and len(time_laps) > 0:
        elog(fn="api_post_race", msg="time_laps not persisted by save_state_end_of_race — saving bug",
             race=race, time_laps_count=len(time_laps))
    else:
        ilog(fn="api_post_race", msg="post_race processing done",
             race=race, b=b, new_b=b+1, season=season_count,
             saved_time_laps_count=len(saved_time_laps))

    new_b                = b + 1
    championship_length  = len(championship)

    updated_state = _state()
    updated_state["b"]                  = new_b
    updated_state["season_count"]       = season_count
    updated_state["championship_length"] = championship_length

    _write_state(updated_state, "api_post_race")
    # Generate climax
    climax = random.choice(["transitional","sunny","sunny","sunny"])
    weather = random.choice(WEATHER_TYPES)
    with open(os.path.join(_CONFIG, "../engine/user_input/climax.json"), "w", encoding="utf-8") as f:
        json.dump({"climax": climax, "weather": weather}, f, indent=2, ensure_ascii=False)
    if new_b > championship_length:
        ilog(fn="api_post_race", msg="championship finished", season=season_count)
        return {"status": "race_done", "race": race, "championship_finished": True}
    return {"status": "race_done", "race": race, "championship_finished": False}

# Get climax
@app.get("/api/get_climax")
async def api_get_climax():
    path = os.path.join(_CONFIG, "../engine/user_input/climax.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        elog(fn="api_get_climax", msg="failed to read climax.json", error=str(e), path=path)
        return {"climax": "unknown", "weather": "unknown"}
    return {"climax": data.get("climax", "unknown"), "weather": data.get("weather", "unknown")}

# ---------------------------------------------------------------------------
# POST /api/post_championship
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
    ilog(fn="api_post_championship", msg="MMR2 season simmed",
         mmr2_best=best.name, mmr2_best_rating=round(best.rating, 4),
         mmr2_worst_replaced_with=worst.name)

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
        ilog(fn="api_post_championship", msg="last-placed player auto-promoted from MMR2",
             demoted_player=last_car.name, promoted_mmr2=old_best_name,
             new_rating=round(old_best_rating, 4))

    teams, player, player_2, player.name, player_2.name, cars = trading_at_the_of_season(
        teams, player, player_2, cars
    )

    save_state_end_of_season(cars, teams, season_count)
    save_season_csv(cars, teams, season_count)
    WETTINESS, cars, teams = reset_championship(cars, teams)

    updated_state = _state()
    updated_state["b"]                  = 1
    updated_state["season_count"]       = season_count
    updated_state["championship_length"] = len(championship)
    updated_state["player.name"]        = player.name
    updated_state["player_2.name"]      = player_2.name

    ilog(fn="api_post_championship", msg="season reset done",
         new_season=season_count, p1=player.name, p2=player_2.name)

    _write_state(updated_state, "api_post_championship")

    return {"status": "championship_done", "season": season_count}


# ---------------------------------------------------------------------------
# Lap user data / init config
# ---------------------------------------------------------------------------

@app.post("/api/set_lap_user_data")
async def api_set_lap_user_data(data: dict):
    path = os.path.join(_CONFIG, "../engine/user_input/lap_user_data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    dlog(fn="api_set_lap_user_data", msg="lap user data written", data=data)
    return {"status": "ok"}


@app.post("/api/set_init_config")
async def api_set_init_config(data: dict):
    path = os.path.join(_CONFIG, "../engine/user_input/init.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Ověř zápis — init.json je kritický pro init_race, každý problém tady = bug v závodě
    try:
        with open(path, "r") as f:
            written = json.load(f)
        if written != data:
            elog(fn="api_set_init_config", msg="init.json write verify failed — written content differs",
                 expected=data, got=written)
        else:
            dlog(fn="api_set_init_config", msg="init.json written and verified", payload=data)
    except Exception as e:
        elog(fn="api_set_init_config", msg="init.json verify read failed", error=str(e), path=path)

    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Transfers
# ---------------------------------------------------------------------------

@app.get("/api/get_transfer_offers")
async def api_get_transfer_offers():
    state   = _state()
    drivers = state.get("drivers", [])

    if not drivers:
        elog(fn="api_get_transfer_offers", msg="drivers list empty in state.json")

    players    = [d for d in drivers if d.get("is_player")]
    ai_drivers = [d for d in drivers if not d.get("is_player")]

    offers_pool = [
        {"name": d["name"], "team": d.get("team", "?"),
         "points": d.get("points", 0), "rating": round(d.get("rating", 1.0), 4)}
        for d in ai_drivers
    ]
    random.shuffle(offers_pool)

    result = {
        "driver_1": {"name": players[0]["name"] if len(players) > 0 else "", "offers": offers_pool[:5]},
        "driver_2": {"name": players[1]["name"] if len(players) > 1 else "", "offers": offers_pool[5:10]},
        "mmr2_best": None,
    }

    try:
        from engine.mmr2 import simulate_season_mmr2, list_drivers_mmr2
        best, _ = simulate_season_mmr2(list_drivers_mmr2)
        result["mmr2_best"] = {"name": best.name, "rating": round(best.rating, 4)}
    except Exception as e:
        elog(fn="api_get_transfer_offers", msg="MMR2 sim failed, mmr2_best will be null", error=str(e))

    ilog(fn="api_get_transfer_offers", msg="transfer offers generated",
         p1=result["driver_1"]["name"], p2=result["driver_2"]["name"],
         mmr2_best=result["mmr2_best"])
    return result


@app.post("/api/do_transfer")
async def api_do_transfer(data: dict):
    pilot_to_change = data.get("pilot_to_change")
    chosen_pilot    = data.get("chosen_pilot")
    new_rating      = data.get("rating", None)

    if not pilot_to_change or not chosen_pilot:
        elog(fn="api_do_transfer", msg="missing pilot name(s) in request",
             pilot_to_change=pilot_to_change, chosen_pilot=chosen_pilot)
        raise HTTPException(status_code=400, detail="Missing pilot names")

    if pilot_to_change == chosen_pilot:
        elog(fn="api_do_transfer", msg="pilot_to_change == chosen_pilot, same driver",
             pilot=pilot_to_change)
        raise HTTPException(status_code=400, detail="Cannot transfer to the same pilot")

    state   = _state()
    drivers = state.get("drivers", [])
    p1_name = state.get("player.name", "")
    p2_name = state.get("player_2.name", "")

    if pilot_to_change not in (p1_name, p2_name):
        raise HTTPException(status_code=400, detail=f"'{pilot_to_change}' is not a player driver")

    ilog(fn="api_do_transfer", msg="transfer started",
         pilot_to_change=pilot_to_change, chosen_pilot=chosen_pilot,
         before=td_snapshot_state(state, "before_transfer"))

    target = next((d for d in drivers if d["name"] == pilot_to_change and d.get("is_player")), None)
    if not target:
        elog(fn="api_do_transfer", msg="target player driver not found in drivers list",
             pilot_to_change=pilot_to_change,
             player_names_in_drivers=[d["name"] for d in drivers if d.get("is_player")])
        raise HTTPException(status_code=404, detail=f"Player driver '{pilot_to_change}' not found")

    outgoing_ai = next(
        (d for d in drivers if d["name"] == chosen_pilot and not d.get("is_player")), None
    )
    if not outgoing_ai:
        elog(fn="api_do_transfer", msg="chosen AI pilot not found in drivers list",
             chosen_pilot=chosen_pilot,
             ai_names=[d["name"] for d in drivers if not d.get("is_player")])
        raise HTTPException(status_code=404, detail=f"Pilot '{chosen_pilot}' not found")

    old_team_name = target.get("team", "")
    new_team_name = outgoing_ai.get("team", "")

    if not old_team_name or not new_team_name:
        wlog(fn="api_do_transfer", msg="one or both teams are empty string",
             pilot_to_change=pilot_to_change, old_team=old_team_name,
             chosen_pilot=chosen_pilot, new_team=new_team_name)

    target["name"] = chosen_pilot
    target["team"] = new_team_name
    if new_rating is not None:
        target["rating"] = new_rating

    state["drivers"] = [
        d for d in drivers
        if not (d["name"] == chosen_pilot and not d.get("is_player"))
    ]

    replacement = dict(outgoing_ai)
    replacement["name"]      = pilot_to_change
    replacement["team"]      = old_team_name
    replacement["is_player"] = False
    state["drivers"].append(replacement)

    if pilot_to_change == p1_name:
        state["player.name"] = chosen_pilot
    elif pilot_to_change == p2_name:
        state["player_2.name"] = chosen_pilot

    for team in state.get("teams", []):
        if team.get("name") == old_team_name:
            team["drivers"] = [
                replacement["name"] if d == pilot_to_change else d
                for d in team.get("drivers", [])
            ]
        elif team.get("name") == new_team_name:
            team["drivers"] = [
                chosen_pilot if d == chosen_pilot else d
                for d in team.get("drivers", [])
            ]

    ilog(fn="api_do_transfer", msg="transfer done",
         pilot_to_change=pilot_to_change, chosen_pilot=chosen_pilot,
         old_team=old_team_name, new_team=new_team_name,
         replacement_name=replacement["name"], replacement_team=replacement["team"],
         after=td_snapshot_state(state, "after_transfer"))

    _write_state(state, "api_do_transfer")
    _clear_user_input()

    return {
        "status":   "ok",
        "driver_1": state.get("player.name", ""),
        "driver_2": state.get("player_2.name", ""),
    }


# ---------------------------------------------------------------------------
# POST /api/sim_race — celý závod najednou
# ---------------------------------------------------------------------------

@app.post("/api/sim_race")
async def api_sim_race():
    state    = _state()
    race_ctx = state.get("race_state")
    smt_happened = state.get("smt_happened", False)
    if not race_ctx:
        elog(fn="api_sim_race", msg="race_state missing, init_race not called")
        raise HTTPException(status_code=400, detail="Race not initialized. Call /api/init_race first.")

    total_laps = race_ctx["total_laps"]
    race       = state.get("race", "Unknown Race")

    # --- time_laps guard ---
    time_laps = state.get("time_laps")
    if time_laps is None:
        elog(fn="api_sim_race", msg="time_laps key missing from state.json at race start",
             race=race, lap=state.get("lap"))
        time_laps = []
    elif time_laps != []:
        # Nenulové time_laps na startu = pravděpodobně nedokončený předchozí závod
        wlog(fn="api_sim_race", msg="time_laps not empty at sim_race start — leftover from previous race?",
             race=race, time_laps_count=len(time_laps))

    cars, teams, player, player_2, championship, tracks, \
    player.name, player_2.name, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count = load_game_objects()

    k_speed = race_ctx.get("k_speed", [1, 1.04, 1.08, 0.6, 0.65])
    if not race_ctx.get("k_speed"):
        wlog(fn="api_sim_race", msg="k_speed missing from race_state, using hardcoded fallback")

    tyre_compounds = {
        "hard":   {"wear": race_ctx["k_wear"][0], "speed": k_speed[0]},
        "medium": {"wear": race_ctx["k_wear"][1], "speed": k_speed[1]},
        "soft":   {"wear": race_ctx["k_wear"][2], "speed": k_speed[2]},
        "wet":    {"wear": race_ctx["k_wear"][3], "speed": k_speed[3]},
        "inter":  {"wear": race_ctx["k_wear"][4], "speed": k_speed[4]},
    }

    lap           = state.get("lap", 0)
    lap_snapshots = []

    ilog(fn="api_sim_race", msg="full race sim started",
         race=race, total_laps=total_laps, start_lap=lap, season=season_count)
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

        current_state = _state()
        current_time_laps = current_state.get("time_laps", [])

        # time_laps musí růst každé kolo — pokud neroste, sim_the_lap nezapisuje
        if lap > 0 and len(current_time_laps) == 0:
            elog(fn="api_sim_race", msg="time_laps empty after sim_the_lap — sim not writing state",
                 lap=lap, race=race)

        lap_snapshots.append({
            "lap":       lap,
            "drivers":   current_state.get("drivers", []),
            "time_laps": current_time_laps,
        })

        if lap > total_laps:
            break
        ilog(fn="api_sim_race", msg="something happened function run", lap=lap)
        smt_occurs = happend_something(lap, cars, race_ctx["wettiness"]) 
        dlog(fn="api_sim_race", msg="lap simmed", smt_occurs=smt_occurs, smt_happened=smt_happened)
        settings_path = os.path.join(_CONFIG, "user_input/settings.json")
        try:
            with open(settings_path) as f:
                settings = json.load(f)
            stop_on_event = settings.get("stop_on_event", True)
        except Exception:
            stop_on_event = True
        if smt_occurs and not smt_happened and stop_on_event:
            smt_happened = True
            updated = _state()
            updated["smt_happened"] = True
            _write_state(updated, "api_sim_race")
            dlog(fn="api_sim_race", msg="breaking loop", smt_occurs=smt_occurs)
            break
        
    final_state       = _state()
    final_time_laps   = final_state.get("time_laps", [])

    ilog(fn="api_sim_race", msg="full race sim finished",
         race=race, total_laps=total_laps, final_time_laps_count=len(final_time_laps))

    if len(final_time_laps) == 0:
        elog(fn="api_sim_race", msg="time_laps empty after full race — results will be broken at post_race",
             race=race, total_laps=total_laps)

    return {
        "status":      "ok",
        "finished":    True,
        "total_laps":  total_laps,
        "snapshots":   lap_snapshots,
        "final_state": final_state,
    }


# ---------------------------------------------------------------------------
# POST /api/sim_until
# ---------------------------------------------------------------------------

@app.post("/api/sim_until")
async def api_sim_until(data: dict):
    target_lap = data.get("lap", 1)
    state      = _state()
    race_ctx   = state.get("race_state")

    if not race_ctx:
        elog(fn="api_sim_until", msg="race_state missing")
        raise HTTPException(status_code=400, detail="Race not initialized.")

    total_laps = race_ctx["total_laps"]
    race       = state.get("race", "Unknown Race")

    # --- time_laps guard ---
    time_laps = state.get("time_laps")
    if time_laps is None:
        elog(fn="api_sim_until", msg="time_laps key missing from state.json",
             race=race, target_lap=target_lap)
        time_laps = []
    elif time_laps == [] and state.get("lap", 0) > 0:
        elog(fn="api_sim_until", msg="time_laps empty but lap > 0 — data loss suspected",
             race=race, lap=state.get("lap"), target_lap=target_lap)
    else:
        dlog(fn="api_sim_until", msg="time_laps loaded",
             current_lap=state.get("lap"), target_lap=target_lap,
             time_laps_count=len(time_laps))

    k_speed = race_ctx.get("k_speed", [1, 1.04, 1.08, 0.6, 0.65])
    if not race_ctx.get("k_speed"):
        wlog(fn="api_sim_until", msg="k_speed missing from race_state, using hardcoded fallback")

    cars, teams, player, player_2, championship, tracks, \
    player.name, player_2.name, COUNT_CARS, SAFETY_CAR, LAPS_REMAINING, b, season_count = load_game_objects()

    tyre_compounds = {
        "hard":   {"wear": race_ctx["k_wear"][0], "speed": k_speed[0]},
        "medium": {"wear": race_ctx["k_wear"][1], "speed": k_speed[1]},
        "soft":   {"wear": race_ctx["k_wear"][2], "speed": k_speed[2]},
        "wet":    {"wear": race_ctx["k_wear"][3], "speed": k_speed[3]},
        "inter":  {"wear": race_ctx["k_wear"][4], "speed": k_speed[4]},
    }

    lap           = state.get("lap", 0)
    lap_snapshots = []
    smt_happened  = False
    while lap < target_lap and lap <= total_laps:
        current_race_ctx = _state().get("race_state", race_ctx)
        forecast         = current_race_ctx.get("forecast", race_ctx["forecast"])
        SAFETY_CAR       = current_race_ctx.get("safety_car", False)
        LAPS_REMAINING   = current_race_ctx.get("safety_car_laps_remaining", 0)

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
        current_time_laps = current_state.get("time_laps", [])

        if lap > 0 and len(current_time_laps) == 0:
            elog(fn="api_sim_until", msg="time_laps empty after sim_the_lap",
                 lap=lap, target_lap=target_lap, race=race)
        smt_occurs = happend_something(lap, cars, current_race_ctx["wettiness"]) 
        settings_path = os.path.join(_CONFIG, "user_input/settings.json")
        try:
            with open(settings_path) as f:
                settings = json.load(f)
            stop_on_event = settings.get("stop_on_event", True)
        except Exception:
            stop_on_event = True
        if smt_occurs and not smt_happened and stop_on_event:
            smt_happened = True
            break
        lap_snapshots.append({"lap": lap, "drivers": current_state.get("drivers", [])})

    final_state = _state()
    ilog(fn="api_sim_until", msg="sim_until done",
         race=race, reached_lap=lap, target_lap=target_lap,
         time_laps_count=len(final_state.get("time_laps", [])))

    return {
        "status":      "ok",
        "lap":         lap,
        "total_laps":  total_laps,
        "finished":    lap >= total_laps,
        "snapshots":   lap_snapshots,
        "final_state": final_state,
    }


# ---------------------------------------------------------------------------
# GET /api/tracks
# ---------------------------------------------------------------------------

@app.get("/api/tracks")
def get_tracks_api():
    try:
        loaded_tracks = Track.load_all_from_json()
        random.shuffle(loaded_tracks)
        dlog(fn="load_all_from_json", msg="tracks shuffled second time", order=[t.name for t in loaded_tracks])
        if not loaded_tracks:
            elog(fn="get_tracks_api", msg="Track.load_all_from_json returned empty list")
            raise HTTPException(status_code=404, detail="Tracks not loaded")

        tracks_data = [
            {
                "name":       track.name,
                "pneu_wear":  track.pneu,
                "speed_type": track.speed,
                "temp_1":     track.TIME_S1,
                "temp_2":     track.TIME_S2,
                "temp_3":     track.TIME_S3,
                "laps":       track.laps,
                "sc_prob":    track.dnf_probability,
            }
            for track in loaded_tracks
        ]
        return tracks_data

    except HTTPException:
        raise
    except Exception as e:
        elog(fn="get_tracks_api", msg="unexpected error loading tracks", error=str(e))
        raise HTTPException(status_code=500, detail=f"Interní chyba serveru: {str(e)}")


@app.get("/api/settings")
async def get_settings():
    path = os.path.join(_CONFIG, "user_input/settings.json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"stop_on_event": True, "show_logs": False}

@app.post("/api/settings")
async def post_settings(data: dict):
    path = os.path.join(_CONFIG, "user_input/settings.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return {"status": "ok"}