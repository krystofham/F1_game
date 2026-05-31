import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os, json
try:
    from load_data_json import *
    from strategy import strategy
    from weather import generate_weather
except:
    from engine.load_data_json import *
    from engine.strategy import strategy
    from engine.weather import generate_weather
def pit_player(player, player_2, LAPS, lap, TIME_S1, TIME_S2, TIME_S3, pneu, speed, PNEU_types, SAFETY_CAR, climax):
    data = load_data("lap_user_data")

    d1_data = data.get(player.name,   data.get("driver_1", {"action": "1", "new_pneu": "medium"}))
    d2_data = data.get(player_2.name, data.get("driver_2", {"action": "1", "new_pneu": "medium"}))

    pick   = d1_data["action"].strip().lower()
    pick_2 = d2_data["action"].strip().lower()

    if not player.dnf:
        if pick == "pneustav":
            print(player.pneu, round(player.wear, 2), "%")
            player.time += 2
        elif pick == "pneusafe":
            print("PNEUSAFE active for 1 lap")
            player.wear -= 1
            player.time += 3
        elif pick == "2":
            new = d1_data["new_pneu"].strip().lower()
            if new not in PNEU_types:
                raise ValueError(f"Driver 1: invalid tyre '{new}'")
            strategy(LAPS - lap, TIME_S1, TIME_S2, TIME_S3, pneu, speed, climax)
            player.pit_stop(new, SAFETY_CAR)

    if not player_2.dnf:
        if pick_2 == "pneustav":
            print(player_2.pneu, round(player_2.wear, 2), "%")
            player_2.time += 2
        elif pick_2 == "pneusafe":
            print("PNEUSAFE active for 1 lap")
            player_2.wear -= 1
            player_2.time += 3
        elif pick_2 == "2":
            new = d2_data["new_pneu"].strip().lower()
            if new not in PNEU_types:
                raise ValueError(f"Driver 2: invalid tyre '{new}'")
            strategy(LAPS - lap, TIME_S1, TIME_S2, TIME_S3, pneu, speed, climax)
            player_2.pit_stop(new, SAFETY_CAR)

    if not (player.dnf or player_2.dnf):
        if pick == "2" and pick_2 == "2":
            print(random.choice([
                "Box now, double stack. Maintain gap, all planned.",
                "Box, box, double stack! Close gap, no mistakes!",
                "Box this lap, we're double stacking. Maintain delta, we've got margin.",
                "Plan B, box now. You'll be second in the stack, minimal delay expected.",
                "Box this lap for double stack. First car in now, stand by for release.",
                "Box this lap, we are double stacking. Pit crew is prepped for both."
            ]))
            print(random.choice([
                "Copy. Keeping gap, I'm right za.",
                "Understood. Staying tight.",
                "Copy. I'm ready.",
                "Confirmed. I'll hit my marks."
            ]))
            player.time   += 3
            player_2.time += 3
        elif pick_2 == "2" and pick != "2":
            print(random.choice([
                "Box, box. Box this lap. Tyres ready, confirm entry.",
                "Pit window is open. Box this lap for new weathers.",
                "Box now. Hitting your marks is critical.",
                "Box, box. Tyre temps look good — execute clean entry.",
                "Pit this lap. We're switching compound."
            ]))
            print(random.choice([
                "Copy. In this lap.", "Understood. Coming in.",
                "On my way in.", "Copy. Box, box",
                "Copy, box this lap.", "Copy, confirmed."
            ]))
        elif pick == "2" and pick_2 != "2":
            print(random.choice([
                "Box, box. Box this lap. Tyres ready, confirm entry.",
                "Pit window is open. Box this lap for new weathers.",
                "Box now. Hitting your marks is critical.",
                "Box, box. Tyre temps look good — execute clean entry.",
                "Pit this lap. We're switching compound."
            ]))
            print(random.choice([
                "Copy. In this lap.", "Understood. Coming in.",
                "On my way in.", "Copy. Box, box",
                "Copy, box this lap.", "Copy, confirmed."
            ]))

    # Reset po přečtení — aby se pitstop neopakoval
    try:
        reset_path = os.path.join(os.path.dirname(__file__), "user_input/lap_user_data.json")
        with open(reset_path, "w", encoding="utf-8") as f:
            json.dump({
                player.name:   {"action": "1", "new_pneu": "medium"},
                player_2.name: {"action": "1", "new_pneu": "medium"},
                "commands": []
            }, f, indent=2)
    except Exception as e:
        print(f"Warning: could not reset lap_user_data: {e}")

    return player, player_2
def info(WETTINESS, forecast, lap, weather, LAPS, climax):
    weather_1 = forecast[0]
    weather_2 = forecast[1]
    weather_3 = forecast[2]
    weather_4 = forecast[3]
    if lap == 0:
        print(f"Qualification | Actual weather: {weather}")
    else:
        print(f"\n🌤️  lap {lap}/{LAPS} | Actual weather: {weather}")
    if WETTINESS > 0:
        print(f"Wet track {WETTINESS}%")
    if random.randint(1, 10) < 8:
        print(f"🔮 Forecast: {', '.join(forecast)}")
        if weather_1 == "sunny" and weather_4 in ["rain", "heavy rain"]:
            print(random.choice(["We’re monitoring the weather, expect rain in 3 laps.", "Rain is coming in now, you should start thinking about wet tires soon.", "Rain intensity increasing, we expect full wet conditions in the next 3 laps."]))
            print(random.choice(["Copy that, adjusting my pace.", "Understood, I’m keeping an eye on it.","OK"]))
    else:
        fake = [generate_weather(weather, climax) for _ in range(4)]
        print(f"🔮 Forecast: {', '.join(fake)}")
        if fake[0] == "sunny" and fake[3] in ["rain", "heavy rain"]:
            print(random.choice(["We’re monitoring the weather, expect rain in 3 laps.", "Rain is coming in now, you should start thinking about wet tires soon.", "Rain intensity increasing, we expect full wet conditions in the next 3 laps."]))
            print(random.choice(["Copy that, adjusting my pace.", "Understood, I’m keeping an eye on it.","OK"]))
    return forecast
def drivers_table(cars, COUNT_CARS):
    for i, a in enumerate(cars[:6], 1):
        if a.dnf:
            status = COUNT_CARS        
        status = round(a.time, 3)
        if i == 1:
            status_1 = round(status/60, 3)
            print(f"{i}. {a.name} – {status} sek")
            heloo = round(a.wear) * random.uniform(0.9, 1.1)
            heloo = round(heloo, 1)
            print(f"Number of pit stops: {a.box}| Wear: {heloo}%")
            status_1 = round(status, 3)
        else:
            distance = round(status - status_1, 3)
            print(f"{i}. {a.name} + {distance} s")
            heloo = round(a.wear) * random.uniform(0.9, 1.1)
            heloo = round(heloo, 1)
            print(f"Number of pit stops: {a.box}| Wear: {heloo}%")
            status_1 = status
def post_race_info(time_laps, player, player_2, cars, teams, COUNT_CARS):
    print("\n🏁 END race!!")
    
    # === BEZPEČNOSTNÍ KONTROLA PRO PRÁZDNÉ TIME_LAPS ===
    if not time_laps:
        print("⚠️ Warning: No lap times were recorded during this race!")
        print("Fastest lap and fastest sectors cannot be determined.")
    else:
        # Tento blok se spustí POUZE, pokud máme v pole nějaké časy
        time_laps.sort()
        print(f"{time_laps[0][1]} ({time_laps[0][2]}) has fastest lap: {round(time_laps[0][0], 3)}")
        
        sector_1 = min(time_laps, key=lambda x: x[3])
        sector_2 = min(time_laps, key=lambda x: x[4])
        sector_3 = min(time_laps, key=lambda x: x[5])

        print(f"{sector_1[1]} ({sector_1[2]}) has fastest sector 1 {round(sector_1[3], 3)}")
        print(f"{sector_2[1]} ({sector_2[2]}) has fastest sector 2 {round(sector_2[4], 3)}")
        print(f"{sector_3[1]} ({sector_3[2]}) has fastest sector 3 {round(sector_3[5], 3)}")

        for x in teams:
            if x.name == sector_1[2]:
                x.points += 2

    # Výpis pro hráče (spustí se také jen, pokud data existují)
    if time_laps:
        for d in range(len(time_laps)):
            if time_laps[d][1] == player.name:
                print(f"{time_laps[d][1]} ({time_laps[d][2]}) has fastest lap {round(time_laps[d][0], 3)}, sector 1 {round(time_laps[d][3], 3)}, sector 2 {round(time_laps[d][4], 3)}, sector 3 {round(time_laps[d][5], 3)}")
                break
        for d in range(len(time_laps)):
            if time_laps[d][1] == player_2.name:
                print(f"{time_laps[d][1]} ({time_laps[d][2]}) has fastest lap {round(time_laps[d][0], 3)}, sector 1 {round(time_laps[d][3], 3)}, sector 2 {round(time_laps[d][4], 3)}, sector 3 {round(time_laps[d][5], 3)}")
                break

    # Zbytek bodování a ratingů (zůstává beze změny)
    RANK = [a.name for a in cars if not a.dnf]
    for driver in cars:
        driver.vypocitej_points_jezdec(RANK)
        driver.ratings -= 0.01
    for team in teams:
        team.vypocitej_points(RANK, COUNT_CARS)
        
    return teams, cars, time_laps
def print_teams_end_championship(teams:list) -> list:
    print("\n🏆 Teams at the end of championship:")
    teams.sort(key=lambda t: t.points, reverse=True)
    for i, t in enumerate(teams, 1):
        if i == 1:  
            t.rating += 1
            img = mpimg.imread(f'../img/{t.name}.png')
            plt.imshow(img)
            plt.axis('off')
            plt.show()
        print(f"{i}. {t.name} – {t.points} points")
        if i == len(teams):
            t.rating -=1
    return teams