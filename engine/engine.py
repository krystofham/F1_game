import random
import json
import os
from log import dlog, elog, ilog, wlog
try:
    from weather import generate_weather
    from mmr2 import simulate_season_mmr2, list_drivers_mmr2
    from load_data_json import *
except:
    from engine.weather import generate_weather
    from engine.mmr2 import simulate_season_mmr2, list_drivers_mmr2
    from engine.load_data_json import *
def qualification(simulation, cars, TIME_S1, TIME_S2, TIME_S3, training):
    ilog(fn="qualification", msg="qualification started", training=training, car_count=len(cars))
    for car in cars:
            sim_time = TIME_S1 * random.uniform(0.9, 1.1) + TIME_S2 * random.uniform(0.9, 1.1) + TIME_S3 * random.uniform(0.9, 1.1)
            if car.is_player and training == "2":
                sim_time = sim_time/1.5 
            simulation.append((car, sim_time))
    simulation.sort(key=lambda x: x[1])
    for i, (car, sim_time) in enumerate(simulation):
            penalized_time =  5 * i
            car.time += penalized_time
    grid = [(car.name, round(sim_time, 3)) for car, sim_time in simulation[:6]]
    ilog(fn="qualification", msg="qualification finished", grid=grid)
    return simulation

def reset_race(climax, cars):
    global lap, time_laps, SAFETY_CAR, LAPS_REMAINING, forecast, weather
    lap = 0
    time_laps = []
    WETTINESS = 0
    SAFETY_CAR = False
    LAPS_REMAINING = 0
    weather = "sunny"
    forecast = [generate_weather(weather, climax)]
    for _ in range(3):
        forecast.append(generate_weather(forecast[-1], climax))
    for a in cars:
        a.time = 0
        a.dnf = False
        a.wear = 0
        a.position = []
        a.puncture = False
        a.box = 0
        a.stints = []
        a.last_stint_start = 0
        a.destroy = False
    ilog(fn="reset_race", msg="race state reset", climax=climax, car_count=len(cars), forecast=forecast)
    return lap, time_laps, SAFETY_CAR, LAPS_REMAINING, weather, forecast, cars, WETTINESS

def make_a_deal(player, teams, tymy_ridic_1_trade, tymy_ridic_2_trade, possible_transfer):
    data = load_data("transfer")
    new_pilot = data["chosen_pilot"].strip()

    new_car = None
    for team in teams:
        for driver in team.drivers:
            if driver.name == new_pilot:
                new_car = driver
                break
        if new_car:
            break

    if not new_car:
        elog(fn="make_a_deal", msg="chosen pilot not found in teams", chosen_pilot=new_pilot)
        raise ValueError(f"Pilot '{new_pilot}' not found in any team")

    old_team = player.team
    new_team = new_car.team

    idx_player = old_team.drivers.index(player)
    idx_new = new_team.drivers.index(new_car)

    old_team.drivers[idx_player] = new_car
    new_team.drivers[idx_new] = player

    new_car.team = old_team
    player.team = new_team

    # ← toto je klíčové
    player.is_player = False
    new_car.is_player = True

    # Převezmi race stav
    new_car.time            = player.time
    new_car.wear            = player.wear
    new_car.pneu            = player.pneu
    new_car.dnf             = player.dnf
    new_car.box             = player.box
    new_car.points          = player.points
    new_car.position        = list(player.position)
    new_car.stints          = list(player.stints)
    new_car.last_stint_start = player.last_stint_start
    new_car.destroy         = player.destroy
    new_car.puncture        = player.puncture
    new_car.safety_car_probability = player.safety_car_probability

    ilog(fn="make_a_deal", msg="MMR1 deal completed",
         old_player=player.name, new_player=new_car.name,
         old_team=old_team.name, new_team=new_team.name)
    return new_car

def transef_mmr1(cars, teams, player, player_2):
    data = load_data("transfer")
    average_rating = sum(x.ratings for x in cars) / (len(cars) + 1)

    swap = data["pilot_to_change"]

    if swap != player.name and swap != player_2.name:
        elog(fn="transef_mmr1", msg="invalid swap driver", swap=swap,
             player_1=player.name, player_2=player_2.name)
        raise ValueError("invalid drivers")
    ilog(fn="transef_mmr1", msg="MMR1 transfer started", swap=swap, chosen_pilot=data.get("chosen_pilot"))

    tymy_ridic_1_trade = []
    tymy_ridic_2_trade = []
    possible_transfer = []

    for x in teams:
        if len(x.drivers) >= 1 and (x.rating - x.drivers[0].ratings) >= 0:
            tymy_ridic_1_trade.append(x)
        if len(x.drivers) >= 2 and (x.rating - x.drivers[1].ratings) >= 0:
            tymy_ridic_2_trade.append(x)

    # 🔴 OPRAVA: Přiřaď celý objekt (ne player.name!)
    if player.name == swap:
        new_player = make_a_deal(
            player, teams,
            tymy_ridic_1_trade, tymy_ridic_2_trade, possible_transfer
        )
        # Nahraď starý player v cars
        try:
            idx = cars.index(player)
            cars[idx] = new_player
        except ValueError:
            pass  # Pokud player není v cars, ignoruj
        player = new_player  # ✅ Přiřaď celý objekt

    elif player_2.name == swap:
        new_player_2 = make_a_deal(
            player_2, teams,
            tymy_ridic_1_trade, tymy_ridic_2_trade, possible_transfer
        )
        # Nahraď starý player_2 v cars
        try:
            idx = cars.index(player_2)
            cars[idx] = new_player_2
        except ValueError:
            pass
        player_2 = new_player_2  # ✅ Přiřaď celý objekt

    return cars, teams, player, player_2, player.name, player_2.name
def transfer(cars, teams, player, player_2):
    data = load_data("deal")
    new_pilot = data["where"]

    if new_pilot not in ("MMR1", "MMR2"):
        elog(fn="transfer", msg="invalid league target", league=new_pilot)
        raise ValueError("bad league")
    ilog(fn="transfer", msg="transfer started", league=new_pilot, pilot_to_change=data.get("pilot_to_change"))

    if new_pilot == "MMR1":
        cars, teams, player, player_2, player.name, player_2.name = transef_mmr1(
            cars, teams, player, player_2
        )

    elif new_pilot == "MMR2":
        best, worst = simulate_season_mmr2(list_drivers_mmr2)
        change = data["pilot_to_change"]

        if change not in (player.name, player_2.name):
            elog(fn="transfer", msg="invalid MMR2 driver", change=change,
                 player_1=player.name, player_2=player_2.name)
            raise ValueError("bad driver")

        target_player = player if change == player.name else player_2

        # Převezmi race stav z target_playera — best nastupuje na jeho místo
        best.time           = target_player.time
        best.wear           = target_player.wear
        best.pneu           = target_player.pneu
        best.dnf            = target_player.dnf
        best.box            = target_player.box
        best.position       = list(target_player.position)
        best.stints         = list(target_player.stints)
        best.points         = target_player.points
        best.last_stint_start = target_player.last_stint_start
        best.destroy        = target_player.destroy
        best.puncture       = target_player.puncture
        best.safety_car_probability = target_player.safety_car_probability

        target_player.is_player = False
        best.is_player = True

        old_team = target_player.team
        idx_target = old_team.drivers.index(target_player)
        old_team.drivers[idx_target] = best
        best.team = old_team
        target_player.team = old_team  # target zůstane v týmu jako ghost

        try:
            idx = cars.index(target_player)
            cars[idx] = best
        except ValueError:
            cars.append(best)

        if change == player.name:
            player = best
        else:
            player_2 = best

        ilog(fn="transfer", msg="MMR2 transfer completed",
             replaced=change, promoted=best.name, demoted=worst.name)

    return player, player_2, player.name, player_2.name, cars


def safety_car(car, weather, lap, SAFETY_CAR, LAPS_REMAINING, LAPS):
    json_path = os.path.join(os.path.dirname(__file__), "..", "config", "tracks.json")
    
    with open(json_path, "r", encoding="utf-8") as f:
        tracks_data = json.load(f)
    
    track_details = None
    for t in tracks_data:
        if t["laps"] == LAPS:
            track_details = t
            break
            
    if track_details is None:
        elog(fn="safety_car", msg="track not found in tracks.json", laps=LAPS)
        raise ValueError(f"Track not found in tracks.json")
        
    sc_prob = track_details.get("dnf_probability")

    if weather == "sunny":
        if car.safety_car_probability < 1:
            car.safety_car_probability = sc_prob
        if random.randint(1, int((car.safety_car_probability / 10))) == 1:
            penalty = random.randint(10, 55)
            car.time += penalty
            wlog(fn="safety_car", msg="driver mistake penalty", name=car.name,
                 penalty=penalty, lap=lap, weather=weather)
            print("Mistake from driver")
        if random.randint(1, int(car.safety_car_probability)) == 1:
            if lap >= 3:
                car.dnf = True
                SAFETY_CAR = True
                LAPS_REMAINING = random.randint(3, 6)
                ilog(fn="safety_car", msg="crash DNF safety car deployed",
                     name=car.name, lap=lap, weather=weather, sc_laps=LAPS_REMAINING)
                print(f"{car.name} recieved DNF")
                print(random.choice([
                    "Radio: Crash ahead, safety car is out!",
                    "Radio: We’ve got yellow flags – full course yellow!",
                    "Radio: Big crash, bring the delta in check.",
                    "Radio: Watch the debris – SC deployed!"
                ]))
    else:
        if car.safety_car_probability < 1:
            car.safety_car_probability = int(sc_prob / 2)
        if random.randint(1, int((car.safety_car_probability / 5))) == 1:
            if lap >= 3:
                car.dnf = True
                SAFETY_CAR = True
                LAPS_REMAINING = random.randint(3, 6)
                ilog(fn="safety_car", msg="wet crash DNF safety car deployed",
                     name=car.name, lap=lap, weather=weather, sc_laps=LAPS_REMAINING)
                print(f"{car.name} recieved DNF")
                print(random.choice([
                    "Radio: Crash ahead, safety car is out!",
                    "Radio: We’ve got yellow flags – full course yellow!",
                    "Radio: Big crash, bring the delta in check.",
                    "Radio: Watch the debris – SC deployed!"
                ]))
                
    if car.dnf != True: 
        car.dnf = False
    if SAFETY_CAR != True: 
        SAFETY_CAR = False
        LAPS_REMAINING = 0
    return SAFETY_CAR, LAPS_REMAINING, car

def generate_pneu_for_bots_on_start(cars: list, weather_1: str) -> list:
    bot_pneu = {}
    for car in cars:
        if not car.is_player:
            if weather_1 in ('rain', 'heavy rain'):
                car.pneu = random.choice(["wet", "inter"])
            elif weather_1 == "transitional":
                car.pneu = random.choice(["soft", "inter"])
            else:
                car.pneu = random.choice(["hard", "medium", "soft"])
            bot_pneu[car.name] = car.pneu
    dlog(fn="generate_pneu_for_bots_on_start", msg="bot starting pneu assigned",
         weather=weather_1, bot_count=len(bot_pneu), sample=list(bot_pneu.items())[:5])
    return cars

def trading_at_the_of_season(teams, player, player_2, cars):
    want_trade = []
    for x in teams:
        for y in x.drivers:
            if abs(x.rating - y.ratings) > 0.8 and not y.is_player:
                want_trade.append(y)

    while len(want_trade) >= 2:
        drv_1, drv_2 = random.sample(want_trade, 2)
        team_1 = drv_1.team
        team_2 = drv_2.team

        idx_1 = team_1.drivers.index(drv_1)
        idx_2 = team_2.drivers.index(drv_2)

        team_1.drivers[idx_1] = drv_2
        team_2.drivers[idx_2] = drv_1
        drv_1.team = team_2
        drv_2.team = team_1

        want_trade.remove(drv_1)
        want_trade.remove(drv_2)
        ilog(fn="trading_at_the_of_season", msg="AI drivers swapped",
             driver_1=drv_1.name, team_1=team_1.name,
             driver_2=drv_2.name, team_2=team_2.name)

    return teams, player, player_2, player.name, player_2.name, cars

def reset_championship(cars, teams):
    ilog(fn="reset_championship", msg="championship points reset",
         car_count=len(cars), team_count=len(teams))
    for c in cars:
        c.points = 0
    for t in teams:
        t.points = 0
    return 0, cars, teams

def happend_something(lap, cars, WETTINESS):
    DRY = ["soft", "medium", "hard"]
    WET = ["inter", "wet"]
    for car in cars:
        # Stop if player DNFs
        if car.dnf and car.is_player:
            dlog(fn="happend_something",
                 msg=f"Player DNF detected for {car.name} at lap {lap}. Stopping simulation.",
                 lap=lap, driver=car.name)
            return True

        # Stop if track is wet and car uses dry tyres
        if WETTINESS > 50 and car.pneu in DRY and car.is_player:
            dlog(fn="happend_something",
                 msg=f"Wet track (wettiness={WETTINESS}) but {car.name} uses dry tyres ({car.pneu}) at lap {lap}. Stopping simulation.",
                 lap=lap, driver=car.name, pneu=car.pneu, wettiness=WETTINESS)
            return True

        # Stop if track is dry and car uses wet tyres
        if WETTINESS < 30 and car.pneu in WET and car.is_player:
            dlog(fn="happend_something",
                 msg=f"Dry track (wettiness={WETTINESS}) but {car.name} uses wet tyres ({car.pneu}) at lap {lap}. Stopping simulation.",
                 lap=lap, driver=car.name, pneu=car.pneu, wettiness=WETTINESS)
            return True
    return False