from big_functions import * 

lenght = get_lenght_of_championship()
championshionship_race_count = len(championship) - lenght
if championshionship_race_count > 0:
    for _ in range(championshionship_race_count):
        championship.pop(random.randint(0, len(championship)-1))
season_count = 1
b = 1


print(f"Season {season_count}")

time_laps = [] 
for race in championship:
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
    race_ctx = build_race_ctx(
    weather=weather, climax=climax, wettiness=WETTINESS,
    safety_car=SAFETY_CAR, safety_car_laps_remaining=LAPS_REMAINING,
    forecast=forecast, training_type=training_type, speed_bonus=speed_bonus,
    pneu_type=pneu, speed_type=speed,
    k_wear=k_wear, k_speed=k_speed, total_laps=LAPS
    )
    save_state_end_of_lap(cars, teams, season_count, race, lap, race_ctx)

    while lap <= LAPS:
        lap, cars, teams = sim_the_lap(
            cars, teams, player, player_2, lap, SAFETY_CAR, LAPS_REMAINING,
            WETTINESS, forecast, weather, LAPS, climax, DRIVER_1, DRIVER_2,
            pneu, speed, PNEU_types, weather_1, weather_2, weather_3, weather_4,
            training_type, k_wear, speed_bonus, season_count, race, time_laps
        )
    #post race
    RANK = [a for a in cars if not a.dnf]
    save_state_end_of_race(cars, teams, season_count, race)
    teams, cars, time_laps = post_race_info(time_laps, player, player_2, cars, teams, COUNT_CARS)
    points, cars, teams, players = plot_graph(RANK, DRIVER_1, DRIVER_2, teams, cars, player, player_2, climax)
    lap, time_laps, SAFETY_CAR, LAPS_REMAINING, weather, forecast, cars, WETTINESS = reset_race(climax, cars)
    b+=1
#post chamiponship
save_state_end_of_season(cars, teams, season_count)
print("\n🏁 Drivers at the end of championship:")
best, worst = simulate_season_mmr2(list_drivers_mmr2)
season_count +=1
for mmr2_driver in list_drivers_mmr2:
    mmr2_driver.rating -= 1/(season_count*2)
random_name = random.choice(names_free_drivers)
# names_free_drivers.pop(names_free_drivers.index(random_name))
worst.name, worst.rating = random_name, random.uniform(0.95,1.05)
cars.sort(key=lambda x: x.points, reverse=True)
for i, a in enumerate(cars, 1):
    print(f"{i}. {a.name} – {a.points} points ({a.team.name})")
    if i == len(cars):
        new = best.name
        rating = best.rating
        print(f"Breaking!!!\n{new} changes {a.name} ({a.team.name})\nBreaking!!!")
        if a.is_player:
            if DRIVER_1 == a.name:
                DRIVER_1 = new
                player.name, player.ratings = new, rating
            if DRIVER_2 == a.name:
                DRIVER_2 = new
                player_2.name, player_2.ratings = new, rating
        best.name, best.rating = a.name, a.ratings
        a.name, a.ratings = new, rating
print_teams_end_championship(teams)
teams, player, player_2, DRIVER_1, DRIVER_2, cars = trading_at_the_of_season(teams, player, player_2, DRIVER_1, DRIVER_2, cars)
WETTINESS, cars, teams =  reset_championship(cars, teams)
