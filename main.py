import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
random.seed()
#import csv
RANK = 0
WETTINESS = 0
names_free_drivers = [    "Maximilian Becker", "Santiago Cruz",   "Oliver Wright", "Hiroshi Takeda",     "Sebastian Fontaine", "Mateo Silva",     "Jonas Lindberg", "Ivan Kuznetsov",     "Lorenzo Bianchi", "Connor Mitchell",    "Rafael Ortega", "Tobias Schmidt",     "Yuto Nakamura", "Charles Lambert",     "Gabriel Costa", "Andrei Petrescu",    "Lutime Meyer", "Zhang Wei",     "Finn Gallagher", "Ricardo Santos", "Micheal Unide", "Tsu tsei chui", "Simon Lambert", "Sven Olisson", "Albert McHugh"]
TIME_S1 = 15
TIME_S2 = 23
TIME_S3 = 22
time_laps = []
LAPS = 0
LAPS_REMAINING = 0
DRIVER_1 = "Max Vershaeren"
DRIVER_2 = "Kim Nguyen"
TEAM_PLAYER = "MySql AWS Maxim racing team"
COUNT_CARS = 28

WEATHER_TYPES = ["sunny", "transitional", "rain", "heavy rain"]
pneu_colours = {
    "hard": "gray",
    "medium": "yellow",
    "soft": "red",
    "inter": "green",
    "wet": "deepskyblue"
}
def wet_track(weather, wettiness):
    if weather == "heavy rain":
        wettiness += 30
    if weather == "rain":
        wettiness += 20
    if weather == "transitional":
        if wettiness < 60:
            wettiness += 10
        elif wettiness >40:  
            wettiness -= 10
    if weather == "sunny":
        wettiness -= 20
    if wettiness > 100:
        wettiness = 100
    if wettiness < 0:
        wettiness = 0
    return wettiness

def technical_sector_sim(settings):
    speed_in_training = settings[0]/10
    understeer_in_traning = settings[1]/5
    oversteer_in_training = settings[2]/5
    acceleration = settings[3]/10
    grip = settings[4]/5
    curb_handling = settings[5]/5
    my_time = 30
    my_time -= grip + acceleration + oversteer_in_training + understeer_in_traning + speed_in_training + curb_handling
            
    corner_slow = [1, 3, 5, 9, 11, 15]
    corner_medium =  [2, 6, 7, 12, 13]
    corner_fast = [4, 8, 10, 14]
    speeds_on_exit_player = []
    oversteers_player = []
    understeers_player = []
    time_sim_player = []
    for x in range(1, 16):
        chance_mistake = (settings[1] + settings[2]) * -1
        if chance_mistake < 1:
            chance_mistake = 1
        if random.randint(0, 100) < chance_mistake:
            mistake = True
        else:
            mistake = False
        for y in corner_fast:
            if x == y:
                corner = "fast"
        for y in corner_medium:
            if x ==y:
                corner = "medium"
        for y in corner_slow:
            if x==y:
                corner = "slow"
        under = settings[1]*random.uniform(0.98,1.02)
        over = settings[2]*random.uniform(0.98,1.02)
        bonus_time = 0
        if corner == "slow":
            corner_speed = 100+ random.uniform(-5, 5)
            if under > 2:
                corner_speed -= 10*under
                bonus_time += 2
            if over > 2:
                corner_speed -= 10*over
                bonus_time += 2
            if grip < -1:
                under += settings[1]*grip*2
                if under <0:
                    under *= -1
                over += settings[2]*grip
                if over <0:
                    over *= -1
            if curb_handling <-5:
                under += settings[1]*grip
                if under <0:
                    under *= -1
                over += settings[2]*grip*2
                if over <0:
                    over *= -1
            time_sim_player.append(15 + under + over+ bonus_time)
        elif corner == "medium":
            corner_speed = 150+ random.uniform(-5, 5)
            if under > 2:
                corner_speed -= 30*under
                bonus_time += 2
            if over > 2:
                corner_speed -= 30*over
                bonus_time += 2
            if grip < -4:
                under += settings[1]*grip*2
                if under <0:
                    under *= -1
                over += settings[2]*grip
                if over <0:
                    over *= -1
            if curb_handling <-4:
                under += settings[1]*grip
                if under <0:
                    under *= -1
                over += settings[2]*grip*2
                if over <0:
                    over *= -1
            time_sim_player.append(10 + under + over+ bonus_time)
        elif corner == "fast":
            corner_speed = 200+ random.uniform(-5, 5)
            if under > 2:
                corner_speed -= 30*under
                bonus_time += 2
            if over > 2:
                corner_speed -= 30*over
                bonus_time += 2
            if grip < -5:
                under += settings[1]*grip*2
                if under <0:
                    under *= -1
                over += settings[2]*grip
                if over <0:
                    over *= -1
            if curb_handling <-2:
                under += settings[1]*grip
                if under <0:
                    under *= -1
                over += settings[2]*grip*2
                if over <0:
                    over *= -1
            time_sim_player.append(7 + under + over + bonus_time)
        if corner_speed < 0:
            corner_speed = 0
        speed_on_exit = corner_speed +speed_in_training*10+10* acceleration

        if mistake:
            speed_on_exit = 30
            under = 10
            over = 10
        if speed_on_exit <0:
            speed_on_exit *=-1
        speeds_on_exit_player.append(speed_on_exit)
        understeers_player.append(under)
        oversteers_player.append(over)



    speeds_on_exit_bot = []
    time_sim = []
    for x in range(1, 16):
        for y in corner_fast:
            if x == y:
                corner = "fast"
        for y in corner_medium:
            if x ==y:
                corner = "medium"
        for y in corner_slow:
            if x==y:
                corner = "slow"
        under = 0
        over = 0
        if corner == "slow":
            corner_speed = 100+ random.uniform(-25, 25)
            time_sim.append(15 + random.uniform(-1.5, 1.5))
        elif corner == "medium":
            corner_speed = 150+ random.uniform(-25, 25)
            time_sim.append(10 + random.uniform(-1.5, 1.5))
        elif corner == "fast":
            corner_speed = 200+ random.uniform(-25, 25)
            time_sim.append(7+ random.uniform(-1.5, 1.5))
        speeds_on_exit_bot.append(corner_speed)



    turns = list(range(1, 16))
    fig, axs = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
# Time comparison
    axs[0].plot(turns, time_sim_player, label="player – time", marker='o', color='orange')
    axs[0].plot(turns, time_sim, label="Bot – time", marker='o', color='blue')
    axs[0].set_ylabel("time [s]")
    axs[0].legend()
    axs[0].grid(True)
# Speed comparison
    axs[1].plot(turns, speeds_on_exit_player, label="exit player [km/h]", marker='o', color='green')
    axs[1].plot(turns, speeds_on_exit_bot, label="exit bot [km/h]", marker='o', color='gray')
    axs[1].set_ylabel("Rychlost [km/h]")
    axs[1].legend()
    axs[1].grid(True)

# Understeer / Oversteer
    axs[2].bar(turns, understeers_player, label="understeer", color='blue', alpha=0.6)
    axs[2].bar(turns, oversteers_player, label="oversteer", color='green', alpha=0.6)
    axs[2].set_ylabel("mistakes")
    axs[2].set_xlabel("corner")
    axs[2].legend()
    axs[2].grid(True)

    plt.tight_layout()
    plt.show()

def colours_graphs():
    for c in cars:
        if c.dnf:
            colours.append("red")
        elif c.pneu.lower() == "hard":
            colours.append("gray")
        elif c.pneu.lower() == "medium":
            colours.append("yellow")
        elif c.pneu.lower() == "soft":
            colours.append("red")
        elif c.pneu.lower() == "wet":
            colours.append("blue")
        elif c.pneu.lower() == "inter":
            colours.append("green")
        else:
            colours.append("green")  
    return colours
def info(WETTINESS):
    forecast = [weather_1, weather_2, weather_3, weather_4]
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
        fake = [generate_weather(weather) for _ in range(4)]
        print(f"🔮 Forecast: {', '.join(fake)}")
        if fake[0] == "sunny" and fake[3] in ["rain", "heavy rain"]:
            print(random.choice(["We’re monitoring the weather, expect rain in 3 laps.", "Rain is coming in now, you should start thinking about wet tires soon.", "Rain intensity increasing, we expect full wet conditions in the next 3 laps."]))
            print(random.choice(["Copy that, adjusting my pace.", "Understood, I’m keeping an eye on it.","OK"]))
    return forecast
def generate_weather(weather):
    if climax == "transitional":
        if weather == "sunny":
            weather = random.choice(["sunny", "sunny","sunny","sunny", "sunny", "sunny","sunny","sunny","sunny", "sunny","sunny","sunny", "sunny", "sunny","sunny","sunny","sunny", "sunny","sunny","sunny", "sunny", "sunny","sunny","sunny", "sunny", "sunny","sunny","sunny", "transitional"])
        elif weather == "transitional":
            weather = random.choice(["sunny", "transitional", "transitional","transitional","rain"])
        elif weather == "rain":
            weather = random.choice(["transitional", "rain", "rain", "rain", "rain", "rain", "rain", "rain", "rain", "rain", "heavy rain"])
        elif weather == "heavy rain":
            weather = random.choice(["rain", "rain", "heavy rain", "heavy rain", "heavy rain", "heavy rain", "heavy rain", "heavy rain", "heavy rain", "heavy rain"])
    if climax == "sunny":
        weather = "sunny"
    return weather
SAFETY_CAR = False
def drivers_table():
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
def reset_race():
    global lap, time_laps, SAFETY_CAR, LAPS_REMAINING, forecast, weather
    lap = 0
    time_laps = []
    SAFETY_CAR = False
    LAPS_REMAINING = 0
    weather = "sunny"
    forecast = [generate_weather(weather)]
    for _ in range(3):
        forecast.append(generate_weather(forecast[-1]))
    for a in cars:
        a.time = 0
        a.dnf = False
        a.wear = 0
        a.position = []
        a.puncture = False
        a.box = 0
        a.stints = []
        a.last_stint_start = 0
    return lap, time_laps, SAFETY_CAR, LAPS_REMAINING, weather, forecast, cars
def pit_player():
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
def strategy(LAPS, TIME_S1, TIME_S2, TIME_S3, pneu, speed):
    count_laps = LAPS
    if count_laps < 2:
        count_laps == 3
    lap_time = (TIME_S1 + TIME_S2 + TIME_S3)/60
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
    endurance_s = 60/k_wear[2]*k_speed[2]
    endurance_m = 60/k_wear[1]*k_speed[1]
    endurance_h =60/k_wear[0]*k_speed[0]
    wear = [endurance_h, endurance_m, endurance_s]
    name = ["hard", "Medium", "soft"]
    print(f"soft can do {round(endurance_s, 1)} laps, medium {round(endurance_m, 1)} laps, hard {round(endurance_h, 1)} laps")
    box_time = (100/60)
    if count_laps == 0:
        count_laps = 1
    for i, stint in enumerate(wear, 0):
        if count_laps + 4 < wear[i] < count_laps +20:
            remain = wear[i] - count_laps
            average_speed = (wear[i] - remain)*k_speed[i]/count_laps
            time = round((lap_time*LAPS)/average_speed, 2)

            print(f"Possible strategy - {round(stint, 0)} laps - {time} minutes - {name[i]}")



    for i in range(len(wear)):
        if count_laps + 4 < wear[i] + wear[0] < count_laps +20:
            remain = wear[i] + wear[0]- count_laps
            countlapsendurance2 = wear[0] - remain
            average_speed = (k_speed[i]*wear[i] + countlapsendurance2*k_speed[0])/count_laps
            time = round(((lap_time*LAPS)/average_speed) + box_time, 2)
            if countlapsendurance2 > 0:
                print(f"Possible strategy - {round(wear[i] + wear[0],0)} laps - {time} minutes - {name[i]}, {name[0]}")
        if count_laps + 4 < wear[i] + wear[1]  < count_laps +20:
            remain = wear[i] + wear[1]- count_laps
            countlapsendurance2 = wear[1] - remain
            average_speed = (k_speed[i]*wear[i] + countlapsendurance2*k_speed[1])/count_laps
            time = round(((lap_time*LAPS)/average_speed) + box_time, 2)
            if countlapsendurance2 > 0:
                print(f"Possible strategy - {round(wear[i] + wear[1],0)} laps - {time} minutes - {name[i]}, {name[1]}")
        if count_laps + 4 < wear[i] + wear[2]  < count_laps +20:
            remain = wear[i]+ wear[2] - count_laps
            countlapsendurance2 = wear[2] - remain
            average_speed = (k_speed[i]*wear[i] + countlapsendurance2*k_speed[2])/count_laps
            time = round(((lap_time*LAPS)/average_speed) + box_time, 2)
            if countlapsendurance2 > 0:
                print(f"Possible strategy - {round(wear[i] + wear[2], 0)} laps - {time} minutes - {name[i]}, {name[2]}")
    for i in range(len(wear)):
        for j in range(len(wear)):
            if count_laps + 4 <wear[i] + wear[j] + wear[0]  < count_laps +20:
                remain = wear[i] + wear[j]  + wear[0] - count_laps
                countlapsendurance2 = wear[0] - remain
                average_speed = (k_speed[i]*wear[i] + k_speed[j]*wear[j]+ countlapsendurance2*k_speed[0])/count_laps
                time = round((lap_time*LAPS/average_speed) + box_time*2, 2)
                if countlapsendurance2 > 0:
                    print(f"Possible strategy - {round(wear[i] + wear[j] + wear[0], 0)} laps - {round(lap_time*(wear[i] + wear[j]+wear[0]) + box_time*2, 0)} minutes - {name[i]}, {name[j]}, {name[0]}")
            if count_laps + 4 <wear[i] + wear[j] + wear[1]  < count_laps +20:
                remain = wear[i] + wear[j]  + wear[1]- count_laps
                countlapsendurance2 = wear[1] - remain
                average_speed = (k_speed[i]*wear[i] + k_speed[j]*wear[j]+ countlapsendurance2*k_speed[1])/count_laps
                time = round(((lap_time*LAPS)/average_speed) + box_time*2, 2)
                if countlapsendurance2 > 0:
                    print(f"Possible strategy - {round(wear[i] + wear[j] + wear[1], 0)} laps - {round(lap_time*(wear[i] + wear[j]+wear[1]) + box_time*2, 0)} minutes - {name[i]}, {name[j]}, {name[1]}")
            if count_laps + 4 <wear[i] + wear[j] + wear[2]  < count_laps +20:
                remain = wear[i] + wear[j] + wear[2]- count_laps
                countlapsendurance2 = wear[2] - remain
                average_speed = (k_speed[i]*wear[i] + k_speed[j]*wear[j]+ countlapsendurance2*k_speed[2])/count_laps
                time =  round(((lap_time*LAPS)/average_speed) + box_time*2, 2)
                if countlapsendurance2 > 0:
                    print(f"Possible strategy - {round(wear[i] + wear[j] + wear[2], 0)} laps - {time} minutes - {name[i]}, {name[j]}, {name[2]}")
drivers_mmr2 = [
    "Noah Blake", "Felipe Sandoval", "Luca Moretti", "Brian Chen", "Adam Kerdöl", "Pierre Gauthier",
    "Viktor Orlov", "Daisuke Tanaka", "Elias Müller", "Jordan Evans", "Diego Ramirez", "Anton Petrov",
    "Kenji Nakamura", "Nicolas Dubois", "Thomas Fischer", "Miguel Lopéz", "Alexei Solapov", "Ethan Zhang",
    "Leo Harrington", "Marco Silva"
]

# Class to represent each driver
class Drivermmr2:
    def __init__(self, name, skill):
        self.name = name
        self.skill = skill
        self.time = 0.0

# Function to simulate the season
def simulate_season_mmr2(drivers):
    for driver in drivers:
        for lap in range(50*12):  # For 50 laps per race For 12 races
            driver.time += driver.skill * random.uniform(0.98, 1.02)  # Add time based on experience
    
    # Sort drivers by their time (lower is better)
    mmr2_sorted = sorted(drivers, key=lambda x: x.time)
    
    # Best driver is the one with the lowest time
    best = mmr2_sorted[0]
    # Worst driver is the one with the highest time
    worst = mmr2_sorted[-1]  
    
    return best, worst

# Create a list of drivers with random experience
list_drivers_mmr2 = [Drivermmr2(name, random.uniform(5.95, 8.05)) for name in drivers_mmr2]

# Run the simulation
best, worst = simulate_season_mmr2(list_drivers_mmr2)

class Car:
    def __init__(self, name, skill, is_player=False):
        self.name = name
        self.box = 0
        self.stints = []  
        self.position = []
        self.last_stint_start = 0 
        self.is_player = is_player
        self.pneu = random.choice(["medium", "hard"])
        self.wear = 0.0
        self.safety_car_probability = 0
        self.skills = skill
        self.time = 0.0
        self.points = 0
        self.drs = False
        self.team = None
        self.dnf = False
        self.puncture = False

    def efectivity_pneu(self, weather):
        if isinstance(self.pneu, list):
            self.pneu = self.pneu[0]

        base = PNEU_types[self.pneu]["speed"]

        if weather in ["rain", "heavy rain"] and self.pneu not in ["wet", "inter"]:
            base *= 0.3
        if weather == "heavy rain" and self.pneu not in ["wet", "inter"]:
            base *= 0.2
        if weather == "sunny" and self.pneu in ["wet", "inter"]:
            base *= 0.5

        return base


    def simuluj_lap(self, weather, training, wettiness):
        global SAFETY_CAR
        global LAPS_REMAINING
        if self.dnf:
            return
        
        if self.wear >= 100:
            print(f"{self.name} – extreme Wear! ❌")
            self.dnf = True
            return

        if self.puncture:   
            print(f"{self.name} – puncture! ❌")
            SAFETY_CAR = True
            return SAFETY_CAR
            LAPS_REMAINING = random.randint(3,6)
        if self.wear > 80 and random.random() < 0.55:
            print(f"{self.name} – puncture! ❌")
            self.puncture = True
            self.dnf = True
            SAFETY_CAR = True
            LAPS_REMAINING = random.randint(3,6)
            return SAFETY_CAR

        speed = self.efectivity_pneu(weather)
        s1 = (TIME_S1*random.uniform(0.99, 1.01)+self.skills/2+self.team.skill/2)/ speed
        s2 = (TIME_S2*random.uniform(0.99, 1.01)+self.skills/2+self.team.skill/2)/ speed
        s3 = (TIME_S3*random.uniform(0.99, 1.01)+self.skills/2+self.team.skill/2)/ speed
        if SAFETY_CAR:
            s1 = s1*2.5
            s2 = s2*2.5
            s3 = s3*2.5
        if self.drs:
            s1 = s1 - random.uniform(0.5, 0.7)
            s2 = s2 - random.uniform(0.5, 0.7)
            s3 = s3 - random.uniform(0.5, 0.7)
        if training == "1":
            s1 = s1 - random.uniform(0.1, 0.3)
            s2 = s2 - random.uniform(0.1, 0.3)
            s3 = s3 - random.uniform(0.1, 0.3)
        if speed_bonus:
            s1 = s1 - random.uniform(0.3, 0.5)
            s2 = s2 - random.uniform(0.3, 0.5)
            s3 = s3 - random.uniform(0.3, 0.5)
        if wettiness < 30 and self.pneu not in ["soft", "medium", "hard"]:
            s1 = s1+wettiness/2
            s2 = s2+wettiness/2
            s3 = s3+wettiness/2
        if wettiness > 55 and self.pneu not in ["wet" , "inter"]:
            s1 = s1+wettiness/2
            s2 = s2+wettiness/2
            s3 = s3+wettiness/2
        lap_time = s1 + s2 + s3
        time_laps.append((lap_time, self.name, self.team, s1, s2, s3))
        self.time = self.time + self.wear/8 + lap_time
        self.wear += PNEU_types[self.pneu]["wear"]
        prirustek = PNEU_types[self.pneu]["wear"] * random.uniform(0, 0.4)
        self.wear += prirustek
    def pit_stop(self, new_pneu):
        if not self.dnf:
            self.stints.append((self.last_stint_start, self.time - self.last_stint_start, self.pneu))
        if SAFETY_CAR is True:
            self.time += 50
        else: 
            self.time += 100
        self.box += 1
        self.last_pneu = self.pneu
        self.pneu = new_pneu
        self.wear = 0
        self.last_stint_start = self.time  

    def choose_ai(self, laps, max_laps, forecast):
        if self.dnf:
            return None, False
        unava = self.wear
        zustava = max_laps - laps
        ideal = self.vhodne_pneu(forecast[0])
        ideal_2 = self.vhodne_pneu(forecast[2])

        self.pit = False
        if self.pneu not in ideal and self.pneu not in ideal_2 and zustava > 5:
            self.pit = True
        elif unava >= 80 and random.random() < 0.95:
            self.pit = True
        elif unava > 90 or (self.pneu not in ideal and random.random() > 0.9):
            self.pit = True
        elif SAFETY_CAR and self.wear > 70 and zustava > 5:
            self.pit = True
        if forecast[3] == "transitional":
            ideal = "soft"
        elif forecast[0] in ["rain", "heavy rain"] and LAPS - lap < 70/k_wear[3] and forecast[2] == forecast[0]:
            ideal = "wet"
        elif forecast[0] in ["rain", "heavy rain"] and LAPS - lap < 70/k_wear[4] and forecast[2] == forecast[0]:
            ideal = "inter"
        elif forecast[0] == "sunny" and LAPS - lap < 70/k_wear[0] and forecast[2] == forecast[0]:
            ideal = "hard"
        elif forecast[0] == "sunny" and LAPS- lap < 70/k_wear[1] and forecast[2] == forecast[0]:
            ideal = "medium"
        elif forecast[0] == "sunny" and LAPS - lap < 70/k_wear[2] and forecast[2] == forecast[0]:
            ideal = "soft"
        elif forecast[0] in ["transitional", "sunny", "rain"] and forecast[3] in ["rain", "heavy rain"] or forecast[0] in ["rain", "heavy rain"] and forecast[2] == forecast[0] or forecast[2] in ["rain", "heavy rain"]:
            ideal = random.choice(["wet" ,"wet" , "inter"])
        elif forecast[0] == "sunny" and forecast[2] == forecast[0]:
            ideal = random.choice(["soft" , "medium", "hard", "medium", "hard"])
        elif forecast[0] in ["transitional", "sunny", "rain"] and forecast[3] in ["sunny"]:
            ideal = random.choice(["soft" , "medium", "hard", "medium", "hard"])
        return ideal if self.pit else None
    def player_info(self):
        if self.dnf is False:
            if SAFETY_CAR is True:
                print(random.choice(["Still safety car", "Still spinning slowly lap by lap."]))
                if self.wear > 60:
                    print(random.choice(["Why didn’t we pit? We’ve just thrown away the race.", "I had no grip even before the safety car!", "Come on! These weathers are dead — what are we doing?!", "Are we sure about staying out? Tyres are cooked."]))
            print(f"\n🚗 Your car {self.name}")
            RANK = [a.name for a in cars if not a.dnf]     
            if DRIVER_1 == self.name:
                position = RANK.index(DRIVER_1) + 1 if DRIVER_1 in RANK else COUNT_CARS
                print(f"Driver 1 - {player.name}")
            else:
                position = RANK.index(DRIVER_2) + 1 if DRIVER_2 in RANK else  COUNT_CARS
                print(f"Driver 2 - {player_2.name}")
            print(f"\n📊 Position: {position}. z {len(RANK)}")
            fake_o = int((self.wear) - random.uniform(-4, 4))
            if fake_o < 0:
                fake_o = 0
            print(f"🛞  Pneu: {self.pneu} | Wear: {fake_o}%")
            index = cars.index(self)
            difference = 0
            difference_2 = 0
            if 0 < index < len(cars):
                car_pred = cars[index - 1]
                if index + 1 < len(cars):
                    car_za = cars[index + 1]
                else:
                    car_za = cars[index]
                difference = self.time - car_pred.time    
                difference_2 = car_za.time - self.time
                print(f"Delta in front: {round(difference, 3)}s ({car_pred.team.name})| Delta za: {round(difference_2, 3)}s ({car_za.team.name})")
            elif index == 0:
                car_za = cars[index + 1]
                difference_2 = car_za.time - self.time
                print(f"Delta behind: {round(difference_2, 3)}s ({car_za.team.name})")
            else:
                car_pred = len(cars)
                difference = self.time - car_pred.time
                print(f"Delta in front: {round(difference, 3)}s ({car_pred.team.name})")
            if self.wear >= 70:
                print(random.choice(["The tyres are pretty done now.", "I don´t know what are you doing there, but I am boxing. Or at least I wish.", "The tyres are ***!", "Please, take me out from this hell." "Please box, please."]))
        return 
    def drss(self):
        for i in range(1, len(cars)): 
            current_time = self.time  
            previous_time = cars[i-1].time 
            time_difference = current_time - previous_time

            if time_difference < 1:
                self.drs = True
        return self.time, self.drs

    def simuluj_ai(self, training, WETTINESS):
        if self.is_player is False:
            new_pneu = self.choose_ai(lap, LAPS, forecast)
            if new_pneu:
                self.pit_stop(new_pneu)
        self.simuluj_lap(weather, training, WETTINESS)
    def vhodne_pneu(self, weather):
        if weather in ["heavy rain", "rain"]:
            best_pneu = ["wet", "inter"]
        elif weather == "transitional":
            best_pneu = ["wet", "inter", "soft", "medium", "hard"]
        else:
            best_pneu =  ["soft", "medium", "hard"]
        return best_pneu
    def vypocitej_points_jezdec(self, RANK):
        if self.dnf is False:
            position = RANK.index(self.name) + 1
            if position == 1:
                self.points += 50
            elif position == 2:
                self.points += 45
            elif position == 3:
                self.points += 40
            elif position == 4:
                self.points += 35
            elif position == 5:
                self.points += 30
            elif position == 6:
                self.points += 25
            elif position == 7:
                self.points += 22
            elif position == 8:
                self.points += 20
            elif position == 9:
                self.points += 18
            elif position == 10:
                self.points += 15
            elif position == 11:
                self.points += 12
            elif position == 12:
                self.points += 10
            elif position == 13:
                self.points += 9
            elif position == 14:
                self.points += 8
            elif position == 15:
                self.points += 7
            elif position == 16:
                self.points += 6
            elif position == 17:
                self.points += 5
            elif position == 18:
                self.points += 4
            elif position == 19:
                self.points += 3
            elif position == 20:
                self.points += 2
            elif position == 21:
                self.points += 1
            elif position == 22:
                self.points += 1
            elif position == 23:
                self.points += 1
class Team:
    def __init__(self, name, skill):
        self.name = name
        self.skill = skill
        self.drivers = [] 
        self.points = 0   

    def pridej_jezdce(self, car):
        self.drivers.append(car)
        car.team = self

    def vypocitej_points(self, RANK):
        for jezdec in self.drivers:
            if jezdec.name in RANK:
                position = RANK.index(jezdec.name) + 1
            else:
                position = COUNT_CARS
            if position == 1:
                self.points += 50
            elif position == 2:
                self.points += 45
            elif position == 3:
                self.points += 40
            elif position == 4:
                self.points += 35
            elif position == 5:
                self.points += 30
            elif position == 6:
                self.points += 25
            elif position == 7:
                self.points += 22
            elif position == 8:
                self.points += 20
            elif position == 9:
                self.points += 18
            elif position == 10:
                self.points += 15
            elif position == 11:
                self.points += 12
            elif position == 12:
                self.points += 10
            elif position == 13:
                self.points += 9
            elif position == 14:
                self.points += 8
            elif position == 15:
                self.points += 7
            elif position == 16:
                self.points += 6
            elif position == 17:
                self.points += 5
            elif position == 18:
                self.points += 4
            elif position == 19:
                self.points += 3
            elif position == 20:
                self.points += 2
            elif position == 21:
                self.points += 1
            elif position == 22:
                self.points += 1
            elif position == 23:
                self.points += 1
class Track:
    def __init__(self, name, pneu, speed, TIME_S1, TIME_S2, TIME_S3, laps, dnf_probability):
        self.name = name
        self.pneu = pneu
        self.speed = speed
        self.TIME_S1 = TIME_S1
        self.TIME_S2 = TIME_S2
        self.TIME_S3 = TIME_S3
        self.laps = laps
        self.dnf_probability = dnf_probability
tracks = []
tracks.append(Track("Huawei GP SPA", "hard", "quick", 22, 25, 18, 70, 4500))
tracks.append(Track("LG TV Grand Prix du France", "hard", "slow", 26, 19, 22, 74, 4500))
tracks.append(Track("Sony Varsava Grand Prix","hard", "medium", 35, 18, 24, 62, 5000))
tracks.append(Track("META China Grand Prix", "medium", "slow", 25, 34, 30, 56, 4500))
tracks.append(Track("Ostrava Apple GP", "medium", "quick", 20, 26, 18, 67, 4500))
tracks.append(Track("Python circuit Bahamas", "hard", "medium", 25, 23, 38, 72, 5000))
tracks.append(Track("HP Bulgarian GP", "medium", "medium", 23, 29, 20, 60, 5000))
tracks.append(Track("AWS Grand Prix de Espana", "medium", "quick", 26, 31, 16, 51, 6000))
tracks.append(Track("AirBNB Prague GP", "soft", "quick", 20, 33, 40, 42, 4500))
tracks.append(Track("eBay Skyline Turkey GP","medium", "slow", 27, 24, 36, 49, 4900))
tracks.append(Track("Java airlines Monza IBM Italy GP","soft", "quick", 30, 16, 18, 50, 5100))
drivers = ["Alex Storme","Matteo Blaze","Hiro Tanaka","Lukas Rennhardt","Diego Ventura","Aiden Falk","Pierre Lucien","Nilapsai Vetrovski","Riku Yamashita","Carlos Navarro","Johan Reißer","Theo Hartman","Enzo DaCosta","Sebastian Krell","Marco Falcone","Ivan Vasiliev","Tyler Quinn","Jae-Min Han","Felipe Marquez","Elias Northgate","Arjun Desai","Tomás Moreira","Leo Krüger","Mikhail Antonov","Julian Stroud","Renzo Morandi"]
x = 0
cars = []
for driver in drivers:
    cars.append(Car(driver,random.uniform(5, 6)))
player = Car(DRIVER_1, random.uniform(5, 6), is_player=True)
cars.append(player)
player_2 = Car(DRIVER_2, random.uniform(5, 6), is_player=True)
cars.append(player_2)
teams = []
def create_team(TEAM_PLAYER, player_1, player_2, teams, skill):
    tym = Team(TEAM_PLAYER, skill)
    tym.pridej_jezdce(player_1)
    tym.pridej_jezdce(player_2)
    teams.append(tym)
    return tym
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
championship = ["AWS Grand Prix de Espana", "AirBNB Prague GP", "eBay Skyline Turkey GP","Java airlines Monza IBM Italy GP","HP Bulgarian GP","Python circuit Bahamas", "Ostrava Apple GP", "META China Grand Prix", "Sony Varsava Grand Prix", "LG TV Grand Prix du France", "Huawei GP SPA"]
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
        weather_1 = generate_weather(weather)
        weather_2 = generate_weather(weather_1)
        weather_3 = generate_weather(weather_2)
        weather_4 = generate_weather(weather_3)
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
        speed_in_training = 0
        understeer_in_traning = 0
        oversteer_in_training = 0
        acceleration = 0
        grip = 0
        curb_handling = 0
        front_wing = None
        rear_wing = None
        brakes = None
        stabilizators = None
        suspension = None
        training = input("Do you want training for speed [1] or qualification [2]: ")
        for x in range(3):
            print("Settings of the car. You have three attemps")
            print("We are setting front wing. Value 0-11. Při menších rychlostech větší číslo. Lowers understeer. During rain bigger number.")
            front_wing = int(input(f"How do you want to set the front wing? Last value: {front_wing}\n"))
            if speed == "quick":
                front_wing_ideal = random.randint(0, 4)
            elif speed == "medium":
                front_wing_ideal = random.randint(4, 7) 
            else:
               front_wing_ideal = random.randint(6, 11)
            if climax == "transitional":
                front_wing_ideal += random.randint(3,5)
            if front_wing_ideal > 11:
                front_wing_ideal = 11
            diff = front_wing_ideal - front_wing
            speed_in_training += diff
            if diff > 2 or diff < -2:
                oversteer_in_training -= diff
            else:
                oversteer_in_training += diff
            understeer_in_traning -= diff
            acceleration += diff
            grip += diff


            print("We are setting rear wing.")
            rear_wing = int(input(f"How do you want to set the rear wing? Last value: {rear_wing}\n"))
            if speed == "quick":
                rear_wing_ideal = random.randint(0, 4)
            elif speed == "medium":
               rear_wing_ideal = random.randint(4, 7) 
            else:
                rear_wing_ideal = random.randint(6, 11)
            if climax == "transitional":
                rear_wing_ideal += random.randint(3,5)
            if rear_wing_ideal > 11:
                rear_wing_ideal = 11
            diff = rear_wing_ideal - rear_wing
            speed_in_training += diff
            if diff > 2 or diff < -2:
                oversteer_in_training -= diff
            else:
                oversteer_in_training += diff
            understeer_in_traning -= diff
            acceleration += diff
            grip += diff


            print("We are setting brakes.")
            brakes = int(input(f"How do you want to set the brakes? 50 - 60. Lower number means bigger oversteer, bigger understeer Last value: {brakes} \n"))
            brakes__ideal = random.randint (50, 60)
            if brakes < 40 or brakes > 70:
                brakes = 55
            diff = brakes__ideal - brakes
            understeer_in_traning += diff * 2
            oversteer_in_training += diff *-2

            print(f"We are setting anti-roll bars. 1 = softer, 2 = harder. If you have harder, the car is faster, but has lower grip. Last value: {stabilizators}")
            stabilizators = int(input("What anti-roll bars do you want\n"))
            if stabilizators == 1:
                grip -= 2
                curb_handling -=2
                speed_in_training +=2
                acceleration +=2
            else:
                grip += 2
                curb_handling +=2
                speed_in_training -=2
                acceleration -=2


            print("We are setting springs.")
            suspension = int(input(f"What springs do you want? 1-hard 2-soft. Hards have better acceleration, lower grip, unstable car, bigger understeer a oversteer. Last value: {suspension}\n"))
            if suspension == 1:
                acceleration += 2
                grip -=1
                curb_handling -=2
                oversteer_in_training -=1
                understeer_in_traning -=1
                speed_in_training +=3
            else:
                acceleration -= 2
                grip +=1
                curb_handling +=2
                oversteer_in_training +=1
                understeer_in_traning +=1
                speed_in_training -=3

            settings = [speed_in_training,understeer_in_traning,oversteer_in_training,acceleration,grip,curb_handling]
            #if speed == "quick":
             #   speed_sector_sim(settings)
            #elif speed == "medium":    
             #   medium_sector_sim(settings)
            #else:
            technical_sector_sim(settings)
            if understeer_in_traning > 3 :
                for car in cars:
                    if car.is_player:
                        car.safety_car_probability -= understeer_in_traning*250
            if oversteer_in_training > 3 :
                for car in cars:
                    if car.is_player:
                        car.safety_car_probability -= oversteer_in_training*250
            if grip > 3 :
                for car in cars:
                    if car.is_player:
                        car.safety_car_probability -= 250*grip
            if curb_handling >3:
                for car in cars:
                    if car.is_player:
                        car.safety_car_probability -= curb_handling*250     
            if oversteer_in_training < -2 :
                for car in cars:
                    if car.is_player:
                        car.safety_car_probability += oversteer_in_training*250
            if oversteer_in_training < -2 :
                for car in cars:
                    if car.is_player:
                        car.safety_car_probability += oversteer_in_training*250
            if grip < -2:
                for car in cars:
                    if car.is_player:
                        car.safety_car_probability += 250*grip
            if curb_handling <-2:
                for car in cars:
                    if car.is_player:
                        car.safety_car_probability += curb_handling*250     
            if oversteer_in_training + understeer_in_traning > 5:
                for car in cars:
                    if car.is_player:
                        car.safety_car_probability -= (oversteer_in_training + understeer_in_traning)*150
            if speed_in_training + acceleration > 5:
                speed_bonus = True
            else:
                speed_bonus = False
        #Quali
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
            info(WETTINESS)
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
                    car.player_info()

            cars.sort(key=lambda x: (x.dnf, x.time))
            car.drss()

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

            pit_player()
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
            drivers_table()
            for car in cars:
                car.simuluj_ai(training, WETTINESS)
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

            # posun weather
            weather = forecast.pop(0)
            weather_1 = forecast[0]
            weather_2 = forecast[1]
            weather_3 = forecast[2]
            forecast.append(generate_weather(weather_3))
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
            team.vypocitej_points(RANK)
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
        colours_graphs()
        # Last stint for every car
        for a in cars:
            if not a.dnf:
                a.stints.append((a.last_stint_start, a.time - a.last_stint_start, a.pneu))
        # Print graph
        plt.figure(figsize=(12, 6))
        plt.barh(jmena[::-1], [c if c is not None else 0 for c in timey][::-1], color=colours[::-1])
        plt.xlabel("time (min)")
        plt.ylabel("Drivers")
        plt.title("🏁 Výsledky race")
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
        reset_race()
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