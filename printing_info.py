import random
from strategy import strategy
from weather import generate_weather
def pit_player(player, player_2, LAPS, lap, TIME_S1, TIME_S2, TIME_S3, pneu, speed, PNEU_types):
    pick = 1
    pick_2 = 1
    if player.dnf is False:
        print("Action: [1] continue [2] box for driver 1")
        pick = input("> ").strip()
        if pick == "PNEUSTAV":
            print(player.pneu, round(player.wear, 2), "%")
            player.time += 2
        if pick == "PNEUSAFE":
            print("PNEUSAFE active for 1 lap")
            player.wear -= 1
            player.time += 3
        if pick == "2":
            print("Pick pneu for driver 1: [hard / medium / soft / wet / inter]")
            strategy(LAPS-lap, TIME_S1, TIME_S2, TIME_S3, pneu, speed)                
            new = input("> ").strip().lower()
            while new not in PNEU_types:
                new = input("Invalid choice. Pick pneu for driver 1: [hard / medium / soft / wet / inter]\n")
            player.pit_stop(new)
    if player_2.dnf is False:
        print("Action: [1] continue [2] box for driver 2")
        pick_2 = input("> ").strip()
        if pick == "PNEUSTAV":
            print(player_2.pneu, round(player_2.wear, 2), "%")
            player_2.time += 2
        if pick == "PNEUSAFE":
            print("PNEUSAFE active for 1 lap")
            player.wear -= 1
            player.time += 3
        if pick_2 == "2":
            print("Pick pneu for driver 2: [hard / medium / soft / wet / inter]")
            strategy(LAPS-lap, TIME_S1, TIME_S2, TIME_S3, pneu, speed)  
            new = input("> ").strip().lower()
            while new not in PNEU_types:
                new = input("Invalid choice. Pick pneu for driver 1: [hard / medium / soft / wet / inter]\n")
            player_2.pit_stop(new)
    if player.dnf is True or player_2.dnf is True:
        if pick == "2" and pick_2 == "2":
            print(random.choice(["Box now, double stack. Maintain gap, all planned.",  "Box, box, double stack! Close gap, no mistakes!",  "Box this lap, we’re double stacking. Maintain delta, we’ve got margin.",  "Plan B, box now. You’ll be second in the stack, minimal delay expected.",  "Box this lap for double stack. First car in now, stand by for release.",  "Box this lap, we are double stacking. Pit crew is prepped for both."]))
            print( "Copy. Keeping gap, I’m right za.",  "Understood. Staying tight.",  "Copy. I’m ready.",  "Confirmed. I’ll hit my marks.")
            player.time += 3
            player_2.time += 3
        elif pick_2 == "2" and pick != "2":
            print(random.choice(["Box, box. Box this lap. Tyres ready, confirm entry.",  "Pit window is open. Box this lap for new weathers.",  "Box now. Hitting your marks is critical.",  "Box, box. Tyre temps look good — execute clean entry.",  "Pit this lap. We’re switching compound."]))
            print(random.choice([ "Copy. In this lap.",  "Understood. Coming in.",  "On my way in.", "Copy. Box, box",  "Copy, box this lap.", "Copy, confirmed."]))
        elif pick == "2" and pick_2 != "2":
            print(random.choice(["Box, box. Box this lap. Tyres ready, confirm entry.",  "Pit window is open. Box this lap for new weathers.",  "Box now. Hitting your marks is critical.",  "Box, box. Tyre temps look good — execute clean entry.",  "Pit this lap. We’re switching compound."]))
            print(random.choice([ "Copy. In this lap.",  "Understood. Coming in.",  "On my way in.", "Copy. Box, box",  "Copy, box this lap.", "Copy, confirmed."]))
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
            print(f"{i}. {a.name} – {status} min")
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
