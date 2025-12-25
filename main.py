from init import *
random.seed()
x = 0
cars = []

for driver in drivers:
    cars.append(Car(driver,random.uniform(5, 6)))
player = Car(DRIVER_1, random.uniform(5, 6), is_player=True)
cars.append(player)
player_2 = Car(DRIVER_2, random.uniform(5, 6), is_player=True)
cars.append(player_2)

create_team(TEAM_PLAYER, player, player_2, teams,                               random.uniform(5,   6))
create_team("Scuderia Python", cars[0], cars[1], teams,                         random.uniform(4,   6.9))
create_team("Racing 404",cars[2],cars[3], teams,                                random.uniform(4.5, 6))
create_team("Formula 1.0 racing team",cars[4],cars[5], teams,                   random.uniform(4,   6))
create_team("Microsoft PitStop Protocol racing team",cars[6],cars[7], teams,    random.uniform(4,   6))
create_team("Intel QWERTY GP",cars[8],cars[9], teams,                           random.uniform(4.5, 6))
create_team("Underbyte Nvidia GP",cars[10],cars[11], teams,                     random.uniform(4,   6.85))
create_team("JavaScript Racing team",cars[12],cars[13], teams,                  random.uniform(4,   6.85))
create_team("Java motors",cars[14],cars[15], teams,                             random.uniform(4,   6))
create_team("Jawa Surenate Linux racing team",cars[16],cars[17], teams,         random.uniform(4,   6))
create_team("AMD Assemblyte GP",cars[18],cars[19], teams,                       random.uniform(4,   6))
create_team("VS racing 22",cars[20],cars[21], teams,                            random.uniform(4,   6))
create_team("PyCharm motors",cars[22],cars[23], teams,                          random.uniform(4,   6))
create_team("Pixel motors",cars[24],cars[25], teams,                            random.uniform(4,   6))


lenght = int(input("What is the lenght of the championship: "))
hi = len(championship) - lenght
if hi > 0:
    for _ in range(hi):
        championship.pop(random.randint(0, len(championship)-1))
season_count = 1
while len(names_free_drivers) >= 0:
    print(f"Season {season_count}")
    b = 1
    for race in championship:
        climax = random.choice(["transitional","sunny","sunny","sunny"])
        lap = 0
        for tip in tracks:
            if race == tip.name:
                pneu = tip.pneu
                speed = tip.speed
                TIME_S1 = tip.TIME_S1
                TIME_S2 = tip.TIME_S2
                TIME_S3 = tip.TIME_S3
                LAPS = tip.laps
                dnf_probability = tip.dnf_probability
        for x in cars:
            x.safety_car_probability = dnf_probability
        print(f"Actual race {race} {b}/{len(championship)}")
        print(f"Track is known for {pneu} pneu and {speed} speed. Has {LAPS} laps")
        strategy(LAPS, TIME_S1, TIME_S2, TIME_S3, pneu, speed)

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
        for x in forecast:
            print (f"weather: 🌤️ ☁️  {x}")
        for car in cars:
            car.pneu = random.choice(["hard", "medium"])
        player.pneu = input("Pick pneu for driver 1: [hard / medium / soft / wet / inter]\n[> ")
        while player.pneu not in PNEU_types:
            player.pneu = input("Invalid choice. Pick pneu for driver 1: [hard / medium / soft / wet / inter]\n[> ")
            if player.pneu == "exit":
                continue
        player_2.pneu = input("Pick pneu for driver 2: [hard / medium / soft / wet / inter]\n[> ")
        while player_2.pneu not in PNEU_types:
            player_2.pneu = input("Invalid choice. Pick pneu for driver 2: [hard / medium / soft / wet / inter]\n[> ")
            if player.pneu == "exit":
                continue
        for c in cars:
            if c.is_player is False:
                if weather_1 in ('rain', 'heavy rain'):
                    c.pneu = random.choice(["wet", "inter"])
                if weather_1 == "transitional":
                    c.pneu = random.choice(["soft", "inter"])
        simulation = []
        #Training
        speed_bonus = training(speed, climax, cars)
        #Qualification
        for car in cars:
            sim_time = TIME_S1 * random.uniform(0.9, 1.1) + TIME_S2 * random.uniform(0.9, 1.1) + TIME_S3 * random.uniform(0.9, 1.1)
            if car.is_player and training == "2":
                sim_time = sim_time/1.5 
            simulation.append((car, sim_time))
        simulation.sort(key=lambda x: x[1])
        for i, (car, sim_time) in enumerate(simulation):
            penalized_time =  5 * i
            car.time += penalized_time
        ######################################################################################################################################################################
        while lap <= LAPS:
            if lap == LAPS:
                print("Last lap. Push push.")
            info(WETTINESS, forecast, lap, weather, LAPS, climax)
            for car in cars:
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
                        
            if SAFETY_CAR is True:
                LAPS_REMAINING -=1
            if LAPS_REMAINING == 0:
                SAFETY_CAR = False
            cars.sort(key=lambda x: (x.dnf, x.time))
            for car in cars:
            # sem patří tvůj kód
                if car.is_player:
                    car.player_info(cars, DRIVER_1, COUNT_CARS, player, DRIVER_2,player_2)

            cars.sort(key=lambda x: (x.dnf, x.time))
            car.drss(cars)

            for i, car in enumerate(cars):
                if i > 0:
                    car_pred = cars[i - 1]
                    difference = car.time - car_pred.time
                    if difference < 1.5 and difference > 0:
                        defence = random.uniform(0.6, 0.95)
                        chance_predjeti = max(0.1, 1.5 - difference) * 0.4  # 
                        if car.drs is True:
                            chance_predjeti += 0.3
                        if defence  < chance_predjeti:
                            car.wear += 3
                            cars[i], cars[i - 1] = cars[i - 1], cars[i]
            cars.sort(key=lambda x: (x.dnf, x.time))

            pit_player(player, player_2, LAPS, lap, TIME_S1, TIME_S2, TIME_S3, pneu, speed, PNEU_types)
            cars.sort(key=lambda x: (x.dnf, x.time))
            RANK = [a.name for a in cars if not a.dnf]  # Move this line here
            position = RANK.index(DRIVER_1) + 1 if DRIVER_1 in RANK else COUNT_CARS
            position_2 = RANK.index(DRIVER_2) + 1 if DRIVER_2 in RANK else COUNT_CARS


            #RANK = [a.name for a in cars if not a.dnf]
            WETTINESS = wet_track(weather_1, WETTINESS)
            #position = RANK.index(DRIVER_1) + 1 if DRIVER_1 in RANK else "DNF"
            print(f"\n📊 Leaderboard {DRIVER_1}: {position}. position from {len(RANK)}")
            #position_2 = RANK.index(DRIVER_2) + 1 if DRIVER_2 in RANK else "DNF"
            print(f"\n📊 Leaderboard {DRIVER_2}: {position_2}. position from {len(RANK)}")
            drivers_table(cars, COUNT_CARS)
            for car in cars:
                car.simuluj_ai(training, WETTINESS, lap, LAPS, forecast, weather, laps=LAPS, max_laps=lap, k_wear=k_wear, wettiness=WETTINESS, TIME_S1=TIME_S1, TIME_S2=TIME_S2, TIME_S3=TIME_S3, speed_bonus= speed_bonus, time_laps=time_laps, PNEU_types=PNEU_types)
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
        print("\n🏁 END race!!")
        
        time_laps.sort()
        print(f"{time_laps[0][1]} ({time_laps[0][2].name}) has fastest lap: {round(time_laps[0][0], 3)}")
        for a in cars:
            a.skills -= 0.01
        sector_1 = min(time_laps, key=lambda x: x[3])
        sector_2 = min(time_laps, key=lambda x: x[4])
        sector_3 = min(time_laps, key=lambda x: x[5])

        print(f"{sector_1[1]} ({sector_1[2].name}) has fastest sector 1 {round(sector_1[3], 3)}")
        print(f"{sector_2[1]} ({sector_2[2].name}) has fastest sector 2 {round(sector_2[4], 3)}")
        print(f"{sector_3[1]} ({sector_3[2].name}) has fastest sector 3 {round(sector_3[5], 3)}")

        time_laps[0][2].points += 2
        for d in range(len(time_laps)):
            if time_laps[d][1] == player.name:
                print(f"{time_laps[d][1]} ({time_laps[d][2].name}) has fastest lap {round(time_laps[d][0], 3)}, sector 1 {round(time_laps[d][3], 3)}, sector 2 {round(time_laps[d][4], 3)}, sector 3 {round(time_laps[d][5], 3)}")
                break
        for d in range(len(time_laps)):
            if time_laps[d][1] == player_2.name:
                print(f"{time_laps[d][1]} ({time_laps[d][2].name}) has fastest lap {round(time_laps[d][0], 3)}, sector 1 {round(time_laps[d][3], 3)}, sector 2 {round(time_laps[d][4], 3)}, sector 3 {round(time_laps[d][5], 3)}")
                break
        #time.sleep(6)
        #
        ## Import to CSV
        #with open("vysledky_zavodu.csv", "w", newline="", encoding="utf-8") as file:
        #    writer = csv.writer(file)
        #    writer.writerow(["Rank", "Jezdec", "time (min)", "Počet pit stopů", "DNF", "Stinty"])
        #    for i, a in enumerate(cars, 1):
        #        time = round(a.time / 60, 2) if not a.dnf else "DNF"
        #        stint_popis = "; ".join(
        #            [f"{round(start/60, 1)}–{round((start+doba)/60, 1)}min: {typ}" for start, doba, typ in a.stints]
        #        )
        #        writer.writerow([i, a.name, time, a.box, a.dnf, stint_popis])


        # Make sure, list is without dnf
        RANK = [a.name for a in cars if not a.dnf]
        for driver in cars:
            driver.vypocitej_points_jezdec(RANK)
            driver.skills -= 0.01
        for team in teams:
            team.vypocitej_points(RANK,COUNT_CARS)
        points = sorted(teams, key=lambda x: (x.points))
        # Rank count
        position_1 = RANK.index(DRIVER_1) + 1 if DRIVER_1 in RANK else "DNF"
        position_2 = RANK.index(DRIVER_2) + 1 if DRIVER_2 in RANK else "DNF"
        print("\n🏁 Finalní Position:")
        print(f"{DRIVER_1}: {position_1}. position")
        print(f"{DRIVER_2}: {position_2}. position")
        #time.sleep(4)
        # Results
        cars.sort(key=lambda x: (x.dnf, x.time))
        for i, a in enumerate(cars, 1):
            stav = "DNF" if a.dnf else f"{round(a.time, 2)}s"
            print(f"{i}. {a.name} ({a.team.name}) {a.points} body")
        teams.sort(key=lambda team: team.points, reverse=True)
        #time.sleep(8)
        for i, team in enumerate(teams,1):
            print (f"{i}.{team.name} {team.points} body")
        #time.sleep(8)
        jmena = [a.name for a in cars]
        timey = [a.time/60 if not a.dnf else None for a in cars]
        # colours podle pneu
        colours = []
        colours_graphs(cars, colours)
        # Last stint for every car
        for a in cars:
            if not a.dnf:
                a.stints.append((a.last_stint_start, a.time - a.last_stint_start, a.pneu))
        # Print graph
        plt.figure(figsize=(12, 6))
        plt.barh(jmena[::-1], [c if c is not None else 0 for c in timey][::-1], color=colours[::-1])
        plt.xlabel("time (min)")
        plt.ylabel("Drivers")
        plt.title("🏁 Results of race")
        plt.tight_layout()
        plt.show()
        plt.figure(figsize=(10, 6))
        for a in cars:
            plt.plot(range(1, len(a.position) + 1), a.position, label=a.name)

        plt.gca().invert_yaxis()  # cause first place is the best
        plt.xlabel("lap")
        plt.ylabel("Position")
        plt.title("Position during race")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        plt.figure(figsize=(10, 6))
        players = [player, player_2]
        for a in players:
            plt.plot(range(len(a.position)), a.position, label=a.name)

        plt.gca().invert_yaxis()  # cause first place is the best
        plt.xlabel("lap")
        plt.ylabel("Position")
        plt.title("Position during race")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        reset_race(climax, cars)
        b += 1
    print("\n🏁 Drivers at the end of championship:")
    best, worst = simulate_season_mmr2(list_drivers_mmr2)
    season_count +=1
    for d in list_drivers_mmr2:
        d.skill -= 1/(season_count*2)
    random_name = random.choice(names_free_drivers)
    names_free_drivers.pop(names_free_drivers.index(random_name))
    worst.name, worst.skill = random_name, random.uniform(0.95,1.05)
    cars.sort(key=lambda x: x.points, reverse=True)
    for i, a in enumerate(cars, 1):
        print(f"{i}. {a.name} – {a.points} body ({a.team.name})")
        if i == len(cars):
            new = best.name
            skill = best.skill
            print(f"Breaking!!!\n{new} changes {a.name} ({a.team.name})\nBreaking!!!")
            if a.is_player:
                if DRIVER_1 == a.name:
                    DRIVER_1 = new
                    player.name, player.skills = new, skill
                if DRIVER_2 == a.name:
                    DRIVER_2 = new
                    player_2.name, player_2.skills = new, skill
            best.name, best.skill = a.name, a.skills
            a.name, a.skills = new, skill
    print("\n🏆 Teams at the end of championship:")
    teams.sort(key=lambda t: t.points, reverse=True)
    for i, t in enumerate(teams, 1):
        if i == 1:  
            t.skill += 1
            img = mpimg.imread(f'{t.name}.png')
            plt.imshow(img)
            plt.axis('off')  # Optional: hides axis for image display
            plt.show()
        print(f"{i}. {t.name} – {t.points} body")
        if i == len(teams):
            t.skill -=1
    answear = input("Important question")
    while answear == "":
        answear = input("Important question")
    new_pilot = input("Do you want new pilot? YES/NO\n").lower()   
    if new_pilot == "yes":
        new_pilot = input("Do you want z MMR1 nebo MMR2?\n")
        if new_pilot == "MMR1":
            average_skill = 0
            for x in cars:
                average_skill += x.skills
            average_skill = average_skill/(len(cars) +1)
            swap = input(f"Do you want change {DRIVER_1} or {DRIVER_2}\n")
            while swap != DRIVER_1 or swap != DRIVER_2:
                print("Invalid choice")
                swap = input(f"Do you want change {DRIVER_1} or {DRIVER_2}\n")
            tymy_ridic_1_trade = []
            tymy_ridic_2_trade = []
            possible_transfer = []
            for x in teams:
                for y in cars:
                    if x.drivers[0] == y:
                        if (x.skill - y.skills) >=0:
                            tymy_ridic_1_trade.append(x)
                    if x.drivers[1] == y:
                        if (x.skill - y.skills) >=0:
                            tymy_ridic_2_trade.append(x)
            if DRIVER_1 == swap:
                number = 1
                if average_skill > player.skills:
                    print(f"For exchange of {DRIVER_1} has interest just few teams. For example:")
                    nahodny_ridic = teams[-1].drivers[random.choice[0,1]]
                    print(f"Option 1 {teams[-1].name} ({teams[-1].points} points) offers its pilot {nahodny_ridic.name}")
                    possible_transfer.append(teams[-1])
                else:
                    print("There is a big interest for a driver. For example:")
                    
                    for x in teams:
                        if random.uniform(0, 1) > 0.7:
                            nahodny_ridic = x.drivers[random.choice([0,1])]
                            print(f"Option {number} {x.name} ({x.points} points) {nahodny_ridic.name}")
                            possible_transfer.append(nahodny_ridic)
                            number +=1
                for x in tymy_ridic_1_trade:
                    print(f"Option {number} {x.name} ({x.points} points) offers {x.drivers[0].name}")
                    possible_transfer.append(x.drivers[0])
                    number +=1
                for x in tymy_ridic_2_trade:
                    print(f"Option {number} {x.name} ({x.points} points) offers {x.drivers[1].name}")
                    possible_transfer.append(x.drivers[1])
                    number+=1
                new_pilot = input("What pilot do you want? NAME\n")
                found = False
                for x in possible_transfer:
                    if x == new_pilot:
                        found = True
                while not found:
                    new_pilot = input("What pilot do you want? NAME\n")
                    found = False
                    for x in possible_transfer:
                        if x == new_pilot:
                            found = True
                for x in possible_transfer:
                    if x.name == new_pilot:
                        DRIVER_1 = x.name
                        player.name, x.name = x.name, player.name
                        player.skills, x.skills = x.skills, player.skills
                        print("succesfull swap")
            if DRIVER_2 == swap:
                number = 1
                if average_skill > player_2.skills:
                    print(f"For exchange of {DRIVER_2} has interest just few teams. For example:")
                    nahodny_ridic = teams[-1].drivers[random.choice[0,1]]
                    print(f"Option 1 {teams[-1].name} ({teams[-1].points} points) offers its pilot {nahodny_ridic.name}")
                    possible_transfer.append(teams[-1])
                else:
                    print("There is a big interest for a driver. For example:")
                    
                    for x in teams:
                        if random.uniform(0, 1) > 0.7:
                            nahodny_ridic = x.drivers[random.choice([0,1])]
                            print(f"Option {number} {x.name} ({x.points} points) {nahodny_ridic.name}")
                            possible_transfer.append(nahodny_ridic)
                            number +=1
                for x in tymy_ridic_1_trade:
                    print(f"Option {number} {x.name} ({x.points} points) offers {x.drivers[0].name}")
                    possible_transfer.append(x.drivers[0])
                    number +=1
                for x in tymy_ridic_2_trade:
                    print(f"Option {number} {x.name} ({x.points} points) offers {x.drivers[1].name}")
                    possible_transfer.append(x.drivers[1])
                    number+=1
                new_pilot = input("What pilot do you want? NAME\n")
                found = False
                for x in possible_transfer:
                    if x == new_pilot:
                        found = True
                while not found:
                    new_pilot = input("What pilot do you want? NAME\n")
                    found = False
                    for x in possible_transfer:
                        if x == new_pilot:
                            found = True
                for x in possible_transfer:
                    if x.name == new_pilot:
                        DRIVER_2 = x.name
                        player_2.name, x.name = x.name, player_2.name
                        player_2.skills, x.skills = x.skills, player_2.skills
                        print("succesfull swap")
        elif new_pilot == "MMR2":
            best, worst = simulate_season_mmr2(list_drivers_mmr2)
            print(f"MMR2 {best.name} was won by.")
            final = input("Do you want him? YES/NO?\n")
            if final == "YES":
                change = input(f"Do you want him for {DRIVER_1} or {DRIVER_2}?\n")
                while change !=DRIVER_1 or change !=DRIVER_2:
                    change = input(f"Do you want him for {DRIVER_1} or {DRIVER_2}?\n")
                new = best.name
                skill = best.skill
                if change == DRIVER_1:
                    DRIVER_1 = new
                    player.name, new = new, player.name 
                    player.skills, skill = skill, player.skills
                elif change == DRIVER_2:
                    DRIVER_2 = new
                    player_2.name, new = new, player_2.name 
                    player_2.skills, skill = skill, player_2.skills
    class Want:
        def __init__(self, name):
            self.name = name
            self.transfer_did = False
    want_trade = []
    for x in teams:
        for y in x.drivers:
            if x.skill - y.skills > 0.8 and y.is_player == False:
                want_trade.append(Want(y))
    while len(want_trade) > 0:
        driver_to_trade_1 = random.choice(want_trade)
        driver_to_trade_2 = random.choice(want_trade)
        while driver_to_trade_1 == driver_to_trade_2:
            driver_to_trade_1 = random.choice(want_trade)
        print(f"Breaking!!!\n {driver_to_trade_1.name.name} ({driver_to_trade_1.name.team.name}, {driver_to_trade_1.name.points} points) changes {driver_to_trade_2.name.name} ({driver_to_trade_2.name.team.name}, {driver_to_trade_2.name.points} points)\nBreaking!!!")
        driver_to_trade_1.name, driver_to_trade_2.name == driver_to_trade_2.name, driver_to_trade_1.name
        want_trade.remove(driver_to_trade_1)
        want_trade.remove(driver_to_trade_2)

    WETTINESS = 0
    for c in cars:
        c.points = 0
    for t in teams:
        t.points = 0