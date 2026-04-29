from init import *

def sim_the_lap(cars, teams, player, player_2, lap, SAFETY_CAR, LAPS_REMAINING, WETTINESS, forecast, weather, LAPS, climax, DRIVER_1, DRIVER_2, pneu, speed, PNEU_types, weather_1, weather_2, weather_3, weather_4, training_type, k_wear, speed_bonus, season_count, race, time_laps):

    # Načti aktuální stav
    state = load_state()
    race_ctx = state.get("race_state", {})

    # Přepiš proměnné ze state pokud existují
    if race_ctx:
        SAFETY_CAR      = race_ctx.get("safety_car", SAFETY_CAR)
        LAPS_REMAINING  = race_ctx.get("safety_car_laps_remaining", LAPS_REMAINING)
        WETTINESS       = race_ctx.get("wettiness", WETTINESS)
        forecast        = race_ctx.get("forecast", forecast)
        weather         = race_ctx.get("weather", weather)

    # Safety car
    for car in cars:
        SAFETY_CAR, LAPS_REMAINING, car.dnf, car.time = safety_car(car, weather, lap, SAFETY_CAR, LAPS_REMAINING)
    if SAFETY_CAR:
        LAPS_REMAINING -= 1
    if LAPS_REMAINING == 0:
        SAFETY_CAR = False

    cars.sort(key=lambda x: (x.dnf, x.time))
    info(WETTINESS, forecast, lap, weather, LAPS, climax)

    for car in cars:
        if car.is_player:
            car.player_info(cars, DRIVER_1, COUNT_CARS, player, DRIVER_2, player_2, SAFETY_CAR)

    cars.sort(key=lambda x: (x.dnf, x.time))

    for i, car in enumerate(cars, 1):
        if i != 1:
            car.drs = car.drss(cars[i - 1])

    player, player_2 = pit_player(player, player_2, LAPS, lap, TIME_S1, TIME_S2, TIME_S3, pneu, speed, PNEU_types, SAFETY_CAR, climax)
    cars.sort(key=lambda x: (x.dnf, x.time))

    RANK = [a.name for a in cars if not a.dnf]
    position   = RANK.index(DRIVER_1) + 1 if DRIVER_1 in RANK else COUNT_CARS
    position_2 = RANK.index(DRIVER_2) + 1 if DRIVER_2 in RANK else COUNT_CARS

    WETTINESS = wet_track(weather_1, WETTINESS)
    print(f"\n📊 Leaderboard {DRIVER_1}: {position}. position from {len(RANK)}")
    print(f"\n📊 Leaderboard {DRIVER_2}: {position_2}. position from {len(RANK)}")
    drivers_table(cars, COUNT_CARS)

    for car in cars:
        SAFETY_CAR, LAPS_REMAINING = car.simuluj_ai(
            training_type, WETTINESS, lap, LAPS, forecast, weather,
            laps=lap, max_laps=LAPS, k_wear=k_wear, wettiness=WETTINESS,
            TIME_S1=TIME_S1, TIME_S2=TIME_S2, TIME_S3=TIME_S3,
            speed_bonus=speed_bonus, time_laps=time_laps,
            PNEU_types=PNEU_types, SAFETY_CAR=SAFETY_CAR, LAPS_REMAINING=LAPS_REMAINING
        )

    boxy_po_teamu = {}
    for a in cars:
        if not a.is_player and a.pit:
            boxy_po_teamu[a.team] = boxy_po_teamu.get(a.team, 0) + 1
    for team, count in boxy_po_teamu.items():
        if count >= 2:
            print(f"{team.name} is going to double stack.")

    cars.sort(key=lambda x: (x.dnf, x.time))
    RANK_OBJ = [a for a in cars if not a.dnf]
    for a in cars:
        position = RANK_OBJ.index(a) + 1 if a in RANK_OBJ else COUNT_CARS
        a.position.append(position)

    # Posuň počasí
    weather = forecast.pop(0)
    weather_1 = forecast[0]
    weather_2 = forecast[1]
    weather_3 = forecast[2]
    forecast.append(generate_weather(weather_3, climax))

    lap += 1

    # Ulož stav s aktuálním race_ctx
    race_ctx = build_race_ctx(
        weather=weather, climax=climax, wettiness=WETTINESS,
        safety_car=SAFETY_CAR, safety_car_laps_remaining=LAPS_REMAINING,
        forecast=forecast, training_type=training_type, speed_bonus=speed_bonus,
        pneu_type=pneu, speed_type=speed,
        k_wear=k_wear, k_speed=[],  # k_speed předej pokud ho máš v scope
        total_laps=LAPS
    )
    save_state_end_of_lap(cars, teams, season_count, race, lap, race_ctx)

    return lap, cars, teams

def sim_the_race(cars, teams, player, player_2, pneu):
    climax = random.choice(["transitional","sunny","sunny","sunny"])
    lap = 0
    for track in tracks:
        if race == track.name:
            pneu = track.pneu
            speed = track.speed
            TIME_S1 = track.TIME_S1
            TIME_S2 = track.TIME_S2
            TIME_S3 = track.TIME_S3
            LAPS = track.laps
            dnf_probability = track.dnf_probability
    for x in cars:
        x.safety_car_probability = dnf_probability
    print(f"Actual race {race} {b}/{len(championship)}")
    print(f"Track is known for {pneu} pneu and {speed} speed. Has {LAPS} laps")
    strategy(LAPS, TIME_S1, TIME_S2, TIME_S3, pneu, speed, climax)

    if pneu == "medium":
        k_wear = [1.5,5,9,4.4,8.4]
    elif pneu == "soft":
        k_wear = [2,7,12,5,9]       
    else:
        k_wear = [1,4,7,4,8]
    if speed == "medium":
        k_speed = [1,1.04,1.08,0.6,0.65]
    elif speed == "quick":
        k_speed = [1.05,1.09,1.13,0.65,0.7]
    else:
        k_speed = [0.95,0.99,1.03,0.55,0.6]

    PNEU_types = {
    "hard": {"wear": k_wear[0], "speed": k_speed[0]},
    "medium": {"wear": k_wear[1], "speed": k_speed[1]},
    "soft": {"wear": k_wear[2], "speed": k_speed[2]},
    "wet": {"wear": k_wear[3], "speed": k_speed[3]},
    "inter": {"wear": k_wear[4], "speed": k_speed[4]},
    }
    if climax == "sunny":
        weather = "sunny"
    else:
        weather = random.choice(WEATHER_TYPES)
    if weather in ('rain', 'heavy rain'):
        WETTINESS = 100
    weather_1 = generate_weather(weather, climax)
    weather_2 = generate_weather(weather_1, climax)
    weather_3 = generate_weather(weather_2, climax)
    weather_4 = generate_weather(weather_3, climax)
    forecast = [weather_1, weather_2, weather_3, weather_4]
    print(f"Will be {climax}")
    for weather in forecast:
        print (f"weather: 🌤️ ☁️  {weather}")
    for car in cars:
        car.pneu = random.choice(["hard", "medium"])
    player.pneu = get_player_pneu(PNEU_types, player.pneu, "driver_1")
    player_2.pneu = get_player_pneu(PNEU_types, player_2.pneu, "driver_2")
    cars = generate_pneu_for_bots_on_start(cars, weather_1)
    simulation = []
    #Training
    # speed_bonus, training_type = training(speed, climax, cars)
    training_type = "1"
    speed_bonus = True
    #Qualification
    simulation = qualification(simulation, cars, TIME_S1, TIME_S2, TIME_S3, training_type)
    ######################################################################################################################################################################
    while lap <= LAPS:  
        lap, cars, teams = sim_the_lap(cars, teams, player, player_2)
        #safety car
        
    #post race
    RANK = [a for a in cars if not a.dnf]
    save_state_end_of_race(cars, teams, season_count, race)
    teams, cars, time_laps = post_race_info(time_laps, player, player_2, cars, teams, COUNT_CARS)
    points, cars, teams, players = plot_graph(RANK, DRIVER_1, DRIVER_2, teams, cars, player, player_2, climax)
    lap, time_laps, SAFETY_CAR, LAPS_REMAINING, weather, forecast, cars, WETTINESS = reset_race(climax, cars)
    b+=1
    return cars, teams