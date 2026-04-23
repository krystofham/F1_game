from init import *
lenght = get_lenght_of_championship()

championshionship_race_count = len(championship) - lenght
if championshionship_race_count > 0:
    for _ in range(championshionship_race_count):
        championship.pop(random.randint(0, len(championship)-1))
season_count = 1
while len(names_free_drivers) >= 0:
    print(f"Season {season_count}")
    b = 1
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
        get_player_pneu(PNEU_types)
        player.pneu = get_player_pneu(PNEU_types, player.pneu)
        player2.pneu = get_player_pneu(PNEU_types, player2.pneu)
        """
        player.pneu = input("Pick pneu for driver 1: [hard / medium / soft / wet / inter]\n[> ")
        while player.pneu not in PNEU_types:
            player.pneu = input("Invalid choice. Pick pneu for driver 1: [hard / medium / soft / wet / inter]\n[> ")
            if player.pneu == "exit":
                continue
        player_2.pneu = input("Pick pneu for driver 2: [hard / medium / soft / wet / inter]\n[> ")
        while player_2.pneu not in PNEU_types:
            player_2.pneu = input("Invalid choice. Pick pneu for driver 2: [hard / medium / soft / wet / inter]\n[> ")
            if player2.pneu == "exit":
                continue
        """
        generate_pneu_for_bots_on_start()

        simulation = []
        #Training
        speed_bonus, training_type = training(speed, climax, cars)
        #training_type = "1"
        #speed_bonus = True
        #Qualification
        simulation = qualification(simulation, cars, TIME_S1, TIME_S2, TIME_S3, training_type)
        ######################################################################################################################################################################
        while lap <= LAPS:
            if lap == LAPS:
                print("Last lap. Push push.")
            #safety car
            for car in cars:
                SAFETY_CAR, LAPS_REMAINING, car.dnf, car.time = safety_car(car, weather, lap, SAFETY_CAR, LAPS_REMAINING)
            if SAFETY_CAR is True:
                LAPS_REMAINING -=1
            if LAPS_REMAINING == 0:
                SAFETY_CAR = False
            cars.sort(key=lambda x: (x.dnf, x.time))
            #print info
            info(WETTINESS, forecast, lap, weather, LAPS, climax)
            #print info
            for car in cars:
                if car.is_player:
                    car.player_info(cars, DRIVER_1, COUNT_CARS, player, DRIVER_2,player_2, SAFETY_CAR)
            cars.sort(key=lambda x: (x.dnf, x.time))
            #drs check
            for i, car in enumerate(cars, 1):
                if i!=1:
                    car.drs = car.drss(cars[i-1])
            #check pitting
            player, player_2 = pit_player(player, player_2, LAPS, lap, TIME_S1, TIME_S2, TIME_S3, pneu, speed, PNEU_types, SAFETY_CAR, climax)
            cars.sort(key=lambda x: (x.dnf, x.time))
            RANK = [a.name for a in cars if not a.dnf] 
            position = RANK.index(DRIVER_1) + 1 if DRIVER_1 in RANK else COUNT_CARS
            position_2 = RANK.index(DRIVER_2) + 1 if DRIVER_2 in RANK else COUNT_CARS
            #Wettiness
            WETTINESS = wet_track(weather_1, WETTINESS)
            print(f"\n📊 Leaderboard {DRIVER_1}: {position}. position from {len(RANK)}")
            print(f"\n📊 Leaderboard {DRIVER_2}: {position_2}. position from {len(RANK)}")
            # Print drivers table
            drivers_table(cars, COUNT_CARS)
            for car in cars:
                SAFETY_CAR, LAPS_REMAINING = car.simuluj_ai(training_type, WETTINESS, lap, LAPS, forecast, weather, laps=lap, max_laps=LAPS, k_wear=k_wear, wettiness=WETTINESS, TIME_S1=TIME_S1, TIME_S2=TIME_S2, TIME_S3=TIME_S3, speed_bonus= speed_bonus, time_laps=time_laps, PNEU_types=PNEU_types, SAFETY_CAR=SAFETY_CAR, LAPS_REMAINING = LAPS_REMAINING)
            boxy_po_teamu = {}
            for a in cars:
                if not a.is_player and a.pit: 
                    team = a.team
                    if team not in boxy_po_teamu:
                        boxy_po_teamu[team] = 0
                    boxy_po_teamu[team] += 1

            for team, count in boxy_po_teamu.items():
                if count >= 2:
                    print(f"{team.name} is going to double stack.")
            boxy_po_teamu.clear()
            cars.sort(key=lambda x: (x.dnf, x.time))
            RANK = [a for a in cars if not a.dnf]  
            for a in cars:
                if a in RANK:  
                    position = RANK.index(a) + 1  
                else:
                    position = COUNT_CARS  
                a.position.append(position)  # Add position

            # move weather
            weather = forecast.pop(0)
            weather_1 = forecast[0]
            weather_2 = forecast[1]
            weather_3 = forecast[2]
            forecast.append(generate_weather(weather_3, climax))
            weather_4 = forecast[3]
            lap += 1
        #post race
        RANK = [a for a in cars if not a.dnf]
        teams, cars, time_laps = post_race_info(time_laps, player, player_2, cars, teams, COUNT_CARS)
        points, cars, teams, players = plot_graph(RANK, DRIVER_1, DRIVER_2, teams, cars, player, player_2, climax)
        lap, time_laps, SAFETY_CAR, LAPS_REMAINING, weather, forecast, cars, WETTINESS = reset_race(climax, cars)
        b+=1
    #post chamiponship
    print("\n🏁 Drivers at the end of championship:")
    best, worst = simulate_season_mmr2(list_drivers_mmr2)
    season_count +=1
    for mmr2_driver in list_drivers_mmr2:
        mmr2_driver.rating -= 1/(season_count*2)
    random_name = random.choice(names_free_drivers)
    names_free_drivers.pop(names_free_drivers.index(random_name))
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
    print("\n🏆 Teams at the end of championship:")
    teams.sort(key=lambda t: t.points, reverse=True)
    for i, t in enumerate(teams, 1):
        if i == 1:  
            t.rating += 1
            img = mpimg.imread(f'img/{t.name}.png')
            plt.imshow(img)
            plt.axis('off')
            plt.show()
        print(f"{i}. {t.name} – {t.points} points")
        if i == len(teams):
            t.rating -=1
    answear = input("Important question")
    while answear == "":
        answear = input("Important question")
    new_pilot = input("Do you want new pilot? YES/NO\n").lower()   
    while new_pilot not in ("yes", "no"):
        new_pilot = input("Do you want new pilot? YES/NO\n").lower()   
    if new_pilot == "yes":
        player, player_2, DRIVER_1, DRIVER_2, cars = transfer(cars, teams, player, player_2, DRIVER_1, DRIVER_2)        
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
        print(f"Breaking!!!\n {driver_to_trade_1.name.name} ({driver_to_trade_1.name.team.name}, {driver_to_trade_1.name.points} points) changes {driver_to_trade_2.name.name} ({driver_to_trade_2.name.team.name}, {driver_to_trade_2.name.points} points)\nBreaking!!!")
        driver_to_trade_1.name, driver_to_trade_2.name = driver_to_trade_2.name, driver_to_trade_1.name
        want_trade.remove(driver_to_trade_1)
        want_trade.remove(driver_to_trade_2)

    WETTINESS = 0
    for c in cars:
        c.points = 0
    for t in teams:
        t.points = 0