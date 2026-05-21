import random
try:
    from weather import generate_weather
    from mmr2 import simulate_season_mmr2, list_drivers_mmr2
    from load_data_json import *
except:
    from engine.weather import generate_weather
    from engine.mmr2 import simulate_season_mmr2, list_drivers_mmr2
    from engine.load_data_json import *
def qualification(simulation, cars, TIME_S1, TIME_S2, TIME_S3, training):
    for car in cars:
            sim_time = TIME_S1 * random.uniform(0.9, 1.1) + TIME_S2 * random.uniform(0.9, 1.1) + TIME_S3 * random.uniform(0.9, 1.1)
            if car.is_player and training == "2":
                sim_time = sim_time/1.5 
            simulation.append((car, sim_time))
    simulation.sort(key=lambda x: x[1])
    for i, (car, sim_time) in enumerate(simulation):
            penalized_time =  5 * i
            car.time += penalized_time
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
    return lap, time_laps, SAFETY_CAR, LAPS_REMAINING, weather, forecast, cars, WETTINESS
def make_a_deal(player, teams, tymy_ridic_1_trade, tymy_ridic_2_trade, possible_transfer):
    data = load_data("transfer")
    new_pilot = data["chosen_pilot"].strip()

    # Hledej pilota v teams
    new_car = None
    for team in teams:
        for driver in team.drivers:
            if driver.name == new_pilot:
                new_car = driver
                break
        if new_car:
            break

    if not new_car:
        raise ValueError(f"Pilot '{new_pilot}' not found in any team")

    old_team = player.team
    new_team = new_car.team

    idx_player = old_team.drivers.index(player)
    idx_new = new_team.drivers.index(new_car)

    # Vyměň jezdce v týmech
    old_team.drivers[idx_player] = new_car
    new_team.drivers[idx_new] = player

    # Aktualizuj týmy jezdců
    new_car.team = old_team
    player.team = new_team

    # Aktualizuj is_player
    new_car.is_player = True
    player.is_player = False

    return new_car  # ✅ Vrací nový objekt vozidla
def transef_mmr1(cars, teams, player, player_2):
    data = load_data("transfer")
    average_rating = sum(x.ratings for x in cars) / (len(cars) + 1)

    swap = data["pilot_to_change"]

    if swap != player.name and swap != player_2.name:
        raise ValueError("invalid drivers")

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

    if player_2.name == swap:
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
        raise ValueError("bad league")
 
    if new_pilot == "MMR1":
        cars, teams, player, player_2, player.name, player_2.name = transef_mmr1(
            cars, teams, player, player_2
        )
 
    elif new_pilot == "MMR2":
        best, worst = simulate_season_mmr2(list_drivers_mmr2)
        change = data["pilot_to_change"]

        if change not in (player.name, player_2.name):
            raise ValueError("bad driver")

        if change == player.name:
            target_player = player
        else:
            target_player = player_2

        # Hráč odchází → už není is_player
        target_player.is_player = False

        # Příchozí jezdec se stává hráčem
        best.is_player = True

        # Fyzická výměna v týmech
        old_team = target_player.team
        new_team = best.team

        idx_target = old_team.drivers.index(target_player)
        idx_best   = new_team.drivers.index(best)

        old_team.drivers[idx_target] = best
        new_team.drivers[idx_best]   = target_player

        best.team          = old_team
        target_player.team = new_team

        if change == player.name:
            player.name = best.name
            player   = best
        else:
            player_2.name = best.name
            player_2 = best

        # team.drivers zůstává beze změny – target_player je stále stejný objekt
        # player / player_2 reference také zůstávají – jsou to stále stejné objekty
 
    return player, player_2, player.name, player_2.name, cars
def safety_car(car, weather, lap, SAFETY_CAR, LAPS_REMAINING):
    if weather == "sunny":
        if car.safety_car_probability < 1:
            car.safety_car_probability = 200
        if random.randint(1,int((car.safety_car_probability/10))) == 1:
            car.time += random.randint(10, 55)
            print("Mistake from driver")
        if random.randint(1, car.safety_car_probability) == 1:
            if lap >= 3:
                car.dnf = True
                SAFETY_CAR = True
                LAPS_REMAINING = random.randint(3,6)
                print(f"{car.name} recieved DNF")
                print(random.choice([
            "Radio: Crash ahead, safety car is out!",
            "Radio: We’ve got yellow flags – full course yellow!",
            "Radio: Big crash, bring the delta in check.",
            "Radio: Watch the debris – SC deployed!"
        ]))
    else:
        if car.safety_car_probability < 1:
            car.safety_car_probability = 200
        if random.randint(1,int((car.safety_car_probability/5))) == 1:
            if lap >= 3:
                car.dnf = True
                SAFETY_CAR = True
                LAPS_REMAINING = random.randint(3,6)
                print(f"{car.name} recieved DNF")
                print(random.choice([
            "Radio: Crash ahead, safety car is out!",
            "Radio: We’ve got yellow flags – full course yellow!",
            "Radio: Big crash, bring the delta in check.",
            "Radio: Watch the debris – SC deployed!"
        ]))
    if car.dnf != True: car.dnf =False
    if SAFETY_CAR !=True: 
        SAFETY_CAR=False
        LAPS_REMAINING = 0
    return SAFETY_CAR, LAPS_REMAINING, car.dnf, car.time
def generate_pneu_for_bots_on_start(cars: list, weather_1: str) -> list:
    for car in cars:
        if weather_1 in ('rain', 'heavy rain'):
            car.pneu = random.choice(["wet", "inter"])
        elif weather_1 == "transitional":
            car.pneu = random.choice(["soft", "inter"])
        else:
            car.pneu = random.choice(["hard", "medium", "soft"])
    return cars

def trading_at_the_of_season(teams, player, player_2, cars):
    new_pilot = load_data("deal")["want"]
 
    if new_pilot not in ("yes", "no"):
        raise ValueError("bad typo")
 
    if new_pilot == "yes":
        player, player_2, player.name, player_2.name, cars = transfer(
            cars, teams, player, player_2
        )
 
    class Want:
        def __init__(self, name):
            self.name = name          
            self.transfer_did = False
 
    want_trade = []
    for x in teams:
        for y in x.drivers:
            if x.rating - y.ratings > 0.8 and y.is_player == False:
                want_trade.append(Want(y))
 
    while len(want_trade) >= 2:
        driver_to_trade_1, driver_to_trade_2 = random.sample(want_trade, 2)
 
        drv_1 = driver_to_trade_1.name  
        drv_2 = driver_to_trade_2.name 
 
        team_1 = drv_1.team
        team_2 = drv_2.team
 
        print(
            f"Breaking!!!\n {drv_1.name} ({team_1.name}, {drv_1.points} points) "
            f"changes {drv_2.name} ({team_2.name}, {drv_2.points} points)\nBreaking!!!"
        )
 
        idx_1 = team_1.drivers.index(drv_1)
        idx_2 = team_2.drivers.index(drv_2)
 
        team_1.drivers[idx_1] = drv_2
        team_2.drivers[idx_2] = drv_1
 
        drv_1.team = team_2
        drv_2.team = team_1
 
        want_trade.remove(driver_to_trade_1)
        want_trade.remove(driver_to_trade_2)
 
    return teams, player, player_2, player.name, player_2.name, cars

def reset_championship(cars, teams):
    for c in cars:
        c.points = 0
    for t in teams:
        t.points = 0
    return 0, cars, teams