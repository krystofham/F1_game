import random
from weather import generate_weather
from mmr2 import simulate_season_mmr2, list_drivers_mmr2
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
def transfer(cars, teams, player, player_2, DRIVER_1, DRIVER_2):
    new_pilot = input("Do you want from MMR1 or MMR2?\n").upper()
    while new_pilot not in ("MMR1", "MMR2"):
        new_pilot = input("Do you want from MMR1 or MMR2?\n").upper()
    if new_pilot == "MMR1":
        average_rating = 0
        for x in cars:
            average_rating += x.ratings
        average_rating = average_rating/(len(cars) +1)
        swap = input(f"Do you want change {DRIVER_1} or {DRIVER_2}\n")
        while swap != DRIVER_1 and swap != DRIVER_2:
            print("Invalid choice")
            swap = input(f"Do you want change {DRIVER_1} or {DRIVER_2}\n")
        tymy_ridic_1_trade = []
        tymy_ridic_2_trade = []
        possible_transfer = []
        for x in teams:
            for y in cars:
                if x.drivers[0] == y:
                    if (x.rating - y.ratings) >=0:
                        tymy_ridic_1_trade.append(x)
                if x.drivers[1] == y:
                    if (x.rating - y.ratings) >=0:
                        tymy_ridic_2_trade.append(x)
        if DRIVER_1 == swap:
            number = 1
            if average_rating > player.ratings:
                print(f"For exchange of {DRIVER_1} has interest just few teams. For example:")
                random_number = random.choice([0, 1])
                nahodny_ridic = teams[-1].drivers[random_number]
                print(f"Option 1 {teams[-1].name} ({teams[-1].points} points) offers its pilot {nahodny_ridic.name}")
                possible_transfer.append(teams[-1])
            else:
                print("There is a big interest for a driver. For example:")
                
                for x in teams:
                    if random.uniform(0, 1) > 0.7:
                        a = random.choice([0,1])
                        nahodny_ridic = x.drivers[a]
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
                if x.name == new_pilot:
                    found = True
            while not found:
                new_pilot = input("What pilot do you want? NAME\n")
                found = False
                for x in possible_transfer:
                    if x.name == new_pilot:
                        found = True
            for x in possible_transfer:
                if x.name == new_pilot:
                    DRIVER_1 = x.name
                    player.name, x.name = x.name, player.name
                    player.ratings, x.ratings = x.ratings, player.ratings
                    print("succesfull swap")
        if DRIVER_2 == swap:
            number = 1
            if average_rating > player_2.ratings:
                print(f"For exchange of {DRIVER_2} has interest just few teams. For example:")
                random_number = random.choice([0, 1])
                nahodny_ridic = teams[-1].drivers[random_number]
                print(f"Option 1 {teams[-1].name} ({teams[-1].points} points) offers its pilot {nahodny_ridic.name}")
                possible_transfer.append(teams[-1])
            else:
                print("There is a big interest for a driver. For example:")
                
                for x in teams:
                    if random.uniform(0, 1) > 0.7:
                        random_number = random.choice([0,1])
                        nahodny_ridic = x.drivers[random_number]
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
                if x.name == new_pilot:
                    found = True
            while not found:
                new_pilot = input("What pilot do you want? NAME\n")
                found = False
                for x in possible_transfer:
                    if x.name == new_pilot:
                        found = True
            for x in possible_transfer:
                if x.name == new_pilot:
                    DRIVER_2 = x.name
                    player_2.name, x.name = x.name, player_2.name
                    player_2.ratings, x.ratings = x.ratings, player_2.ratings
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
            rating = best.rating
            if change == DRIVER_1:
                DRIVER_1 = new
                player.name, new = new, player.name 
                player.ratings, rating = rating, player.ratings
            elif change == DRIVER_2:
                DRIVER_2 = new
                player_2.name, new = new, player_2.name 
                player_2.ratings, rating = rating, player_2.ratings
    return player, player_2, DRIVER_1, DRIVER_2, cars
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