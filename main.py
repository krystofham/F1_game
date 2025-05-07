import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#import csv
rank = 0
wettiness = 0
names_free_drivers = [    "Maximilian Becker", "Santiago Cruz",   "Oliver Wright", "Hiroshi Takeda",     "Sebastian Fontaine", "Mateo Silva",     "Jonas Lindberg", "Ivan Kuznetsov",     "Lorenzo Bianchi", "Connor Mitchell",    "Rafael Ortega", "Tobias Schmidt",     "Yuto Nakamura", "Charles Lambert",     "Gabriel Costa", "Andrei Petrescu",    "Lutime Meyer", "Zhang Wei",     "Finn Gallagher", "Ricardo Santos"]
TIME_S1 = 15
TIME_S2 = 23
TIME_S3 = 22
time_laps = []
LAPS = 0
laps_remaining = 0
driver_1 = "Max Vershaeren"
driver_2 = "Kim Nguyen"
team_player = "MySql AWS Maxim racing team"
count_cars = 28

WEATHER_TYPES = ["slunečno", "přechodný", "déšť", "silný déšť"]
pneu_colours = {
    "tvrdé": "gray",
    "medium": "yellow",
    "měkké": "red",
    "inter": "green",
    "mokré": "deepskyblue"
}
def mokré_track(weather, wettiness):
    if weather == "silný déšť":
        wettiness += 30
    if weather == "déšť":
        wettiness += 20
    if weather == "přechodný":
        if wettiness < 60:
            wettiness += 10
        else:   
            wettiness -= 10
    if weather == "slunečno":
        wettiness -= 20
    if wettiness > 100:
        wettiness = 100
    if wettiness < 0:
        wettiness = 0
    return wettiness
def colours_graphs():
    for c in cars:
        if c.dnf:
            colours.append("red")
        elif c.pneu.lower() == "tvrdé":
            colours.append("gray")
        elif c.pneu.lower() == "medium":
            colours.append("yellow")
        elif c.pneu.lower() == "měkké":
            colours.append("red")
        elif c.pneu.lower() == "mokré":
            colours.append("blue")
        elif c.pneu.lower() == "inter":
            colours.append("green")
        else:
            colours.append("green")  
    return colours
def info(wettiness):
    Forecast = [weather_1, weather_2, weather_3, weather_4]
    if lap == 0:
        print(f"Kvalifikace | Aktuální počasí: {weather}")
    else:
        print(f"\n🌤️  kolo {lap}/{LAPS} | Aktuální počasí: {weather}")
    if wettiness > 0:
        print(f"Mokrá trať {wettiness}%")
    if random.randint(1, 10) < 8:
        print(f"🔮 Předpověd: {', '.join(Forecast)}")
        if weather_1 == "slunečno" and weather_4 in ["déšť", "silný déšť"]:
            print(random.choice(["We’re monitoring the weather, expect déšť in 3 laps.", "Rain is coming in now, you should start thinking about mokré tires soon.", "Rain intensity increasing, we expect full mokré conditions in the next 3 laps."]))
            print(random.choice(["Copy that, adjusting my pace.", "Understood, I’m keeping an eye on it.","OK"]))
    else:
        fake = [generate_weather(weather) for _ in range(4)]
        print(f"🔮 Předpověd: {', '.join(fake)}")
        if fake[0] == "slunečno" and fake[3] in ["déšť", "silný déšť"]:
            print(random.choice(["We’re monitoring the weather, expect déšť in 3 laps.", "Rain is coming in now, you should start thinking about mokré tires soon.", "Rain intensity increasing, we expect full mokré conditions in the next 3 laps."]))
            print(random.choice(["Copy that, adjusting my pace.", "Understood, I’m keeping an eye on it.","OK"]))
    return Forecast
def generate_weather(weather):
    if climax == "přechodný":
        if weather == "slunečno":
            weather = random.choice(["slunečno", "slunečno","slunečno","slunečno", "slunečno", "slunečno","slunečno","slunečno","slunečno", "slunečno","slunečno","slunečno", "slunečno", "slunečno","slunečno","slunečno","slunečno", "slunečno","slunečno","slunečno", "slunečno", "slunečno","slunečno","slunečno", "slunečno", "slunečno","slunečno","slunečno", "přechodný"])
        elif weather == "přechodný":
            weather = random.choice(["slunečno", "přechodný", "přechodný","přechodný","déšť"])
        elif weather == "déšť":
            weather = random.choice(["přechodný", "déšť", "déšť", "déšť", "déšť", "déšť", "déšť", "déšť", "déšť", "déšť", "silný déšť"])
        elif weather == "silný déšť":
            weather = random.choice(["déšť", "déšť", "silný déšť", "silný déšť", "silný déšť", "silný déšť", "silný déšť", "silný déšť", "silný déšť", "silný déšť"])
    if climax == "slunečno":
        weather = "slunečno"
    return weather
safety_car = False
def drivers_table():
    for i, a in enumerate(cars[:6], 1):
        if a.dnf:
            status = count_cars
        
        status = round(a.time, 3)
        if i == 1:
            status_1 = round(status/60, 3)
            print(f"{i}. {a.name} – {status} min")
            heloo = round(a.wear) * random.uniform(0.9, 1.1)
            heloo = round(heloo, 1)
            print(f"Počet pit stopů: {a.box} Opotřebení: {heloo}%")
            status_1 = round(status, 3)
        else:
            distance = round(status - status_1, 3)
            print(f"{i}. {a.name} + {distance} s")
            heloo = round(a.wear) * random.uniform(0.9, 1.1)
            heloo = round(heloo, 1)
            print(f"Počet pit stopů: {a.box} Opotřebení: {heloo}%")
            status_1 = status
def reset_race():
    global lap, time_laps, safety_car, laps_remaining, Forecast, weather
    lap = 0
    time_laps = []
    safety_car = False
    laps_remaining = 0
    weather = "slunečno"
    Forecast = [generate_weather(weather)]
    for _ in range(3):
        Forecast.append(generate_weather(Forecast[-1]))
    for a in cars:
        a.time = 0
        a.dnf = False
        a.wear = 0
        a.position = []
        a.puncture = False
        a.box = 0
        a.stints = []
        a.last_stint_start = 0
    return lap, time_laps, safety_car, laps_remaining, weather, Forecast, cars
def pit_player():
    pick = 1
    pick_2 = 1
    if player.dnf is False:
        print("Akce: [1] pokračovat [2] box pro řidiče 1")
        pick = input("> ").strip()
        if pick == "2":
            print("Vyber pneu pro řidiče 1: [tvrdé / medium / měkké / mokré / inter]")
            strategy(LAPS-lap, TIME_S1, TIME_S2, TIME_S3, pneu, speed)                
            new = input("> ").strip().lower()
            while new not in PNEU_types:
                new = input("Špatná volba. Vyber pneu pro řidiče 1: [tvrdé / medium / měkké / mokré / inter]\n")
            player.pit_stop(new)
    if player_2.dnf is False:
        print("Akce: [1] pokračovat [2] box pro řidiče 2")
        pick_2 = input("> ").strip()
        if pick_2 == "2":
            print("Vyber pneu pro řidiče 2: [tvrdé / medium / měkké / mokré / inter]")
            strategy(LAPS-lap, TIME_S1, TIME_S2, TIME_S3, pneu, speed)  
            new = input("> ").strip().lower()
            while new not in PNEU_types:
                new = input("Špatná volba. Vyber pneu pro řidiče 2: [tvrdé / medium / měkké / mokré / inter]\n")
            player_2.pit_stop(new)
            print("Neplatná volba – pokračuješ.")
    if player.dnf == True or player_2.dnf==True:
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
    elif pneu == "měkké":
        k_wear = [2,7,12,5,9]       
    else:
        k_wear = [1,4,7,4,8]
    if speed == "medium":
        k_speed = [1,1.04,1.08,0.6,0.65]
    elif speed == "quick":
        k_speed = [1.05,1.09,1.13,0.65,0.7]
    else:
        k_speed = [0.95,0.99,1.03,0.55,0.6]
    vydrz_s = 60/k_wear[2]*k_speed[2]
    vydrz_m = 60/k_wear[1]*k_speed[1]
    vydrz_h =60/k_wear[0]*k_speed[0]
    wear = [vydrz_h, vydrz_m, vydrz_s]
    nazev = ["Hard", "Medium", "Soft"]
    print(f"Měkké vydrží {vydrz_s}, medium {vydrz_m}, tvrdé {vydrz_h}")
    box_time = (100/60)
    for i, stint in enumerate(wear, 0):
        if count_laps + 4 < wear[i] < count_laps +20:
            remain = wear[i] - count_laps
            average_speed = (wear[i] - remain)*k_speed[i]/count_laps
            time = round((lap_time*LAPS)/average_speed, 2)

            print(f"Možná strategie - {round(stint, 0)} kol - {time} minuty - {nazev[i]}")



    for i in range(len(wear)):
        if count_laps + 4 < wear[i] + wear[0] < count_laps +20:
            remain = wear[i] + wear[0]- count_laps
            countlapsvydrz2 = wear[0] - remain
            average_speed = (k_speed[i]*wear[i] + countlapsvydrz2*k_speed[0])/count_laps
            time = round(((lap_time*LAPS)/average_speed) + box_time, 2)
            if countlapsvydrz2 > 0:
                print(f"Možná strategie - {round(wear[i] + wear[0],0)} kol - {time} minuty - {nazev[i]}, {nazev[0]}")
        if count_laps + 4 < wear[i] + wear[1]  < count_laps +20:
            remain = wear[i] + wear[1]- count_laps
            countlapsvydrz2 = wear[1] - remain
            average_speed = (k_speed[i]*wear[i] + countlapsvydrz2*k_speed[1])/count_laps
            time = round(((lap_time*LAPS)/average_speed) + box_time, 2)
            if countlapsvydrz2 > 0:
                print(f"Možná strategie - {round(wear[i] + wear[1],0)} kol - {time} minuty - {nazev[i]}, {nazev[1]}")
        if count_laps + 4 < wear[i] + wear[2]  < count_laps +20:
            remain = wear[i]+ wear[2] - count_laps
            countlapsvydrz2 = wear[2] - remain
            average_speed = (k_speed[i]*wear[i] + countlapsvydrz2*k_speed[2])/count_laps
            time = round(((lap_time*LAPS)/average_speed) + box_time, 2)
            if countlapsvydrz2 > 0:
                print(f"Možná strategie - {round(wear[i] + wear[2], 0)} kol - {time} minuty - {nazev[i]}, {nazev[2]}")
    for i in range(len(wear)):
        for j in range(len(wear)):
            if count_laps + 4 <wear[i] + wear[j] + wear[0]  < count_laps +20:
                remain = wear[i] + wear[j]  + wear[0] - count_laps
                countlapsvydrz2 = wear[0] - remain
                average_speed = (k_speed[i]*wear[i] + k_speed[j]*wear[j]+ countlapsvydrz2*k_speed[0])/count_laps
                time = round((lap_time*LAPS/average_speed) + box_time*2, 2)
                if countlapsvydrz2 > 0:
                    print(f"Možná strategie - {round(wear[i] + wear[j] + wear[0], 0)} kol - {round(lap_time*(wear[i] + wear[j]+wear[0]) + box_time*2, 0)} minuty - {nazev[i]}, {nazev[j]}, {nazev[0]}")
            if count_laps + 4 <wear[i] + wear[j] + wear[1]  < count_laps +20:
                remain = wear[i] + wear[j]  + wear[1]- count_laps
                countlapsvydrz2 = wear[1] - remain
                average_speed = (k_speed[i]*wear[i] + k_speed[j]*wear[j]+ countlapsvydrz2*k_speed[1])/count_laps
                time = round(((lap_time*LAPS)/average_speed) + box_time*2, 2)
                if countlapsvydrz2 > 0:
                    print(f"Možná strategie - {round(wear[i] + wear[j] + wear[1], 0)} kol - {round(lap_time*(wear[i] + wear[j]+wear[1]) + box_time*2, 0)} minuty - {nazev[i]}, {nazev[j]}, {nazev[1]}")
            if count_laps + 4 <wear[i] + wear[j] + wear[2]  < count_laps +20:
                remain = wear[i] + wear[j] + wear[2]- count_laps
                countlapsvydrz2 = wear[2] - remain
                average_speed = (k_speed[i]*wear[i] + k_speed[j]*wear[j]+ countlapsvydrz2*k_speed[2])/count_laps
                time =  round(((lap_time*LAPS)/average_speed) + box_time*2, 2)
                if countlapsvydrz2 > 0:
                    print(f"Možná strategie - {round(wear[i] + wear[j] + wear[2], 0)} kol - {time} minuty - {nazev[i]}, {nazev[j]}, {nazev[2]}")
drivers_mmr2 = [
    "Noah Blake", "Felipe Sandoval", "Luca Moretti", "Brian Chen", "Adam Kerdöl", "Pierre Gauthier",
    "Viktor Orlov", "Daisuke Tanaka", "Elias Müller", "Jordan Evans", "Diego Ramirez", "Anton Petrov",
    "Kenji Nakamura", "Nicolas Dubois", "Thomas Fischer", "Miguel Lopéz", "Alexei Solapov", "Ethan Zhang",
    "Leo Harrington", "Marco Silva"
]

# Class to represent each driver
class drivermmr2:
    def __init__(self, name, skill):
        self.name = name
        self.skill = skill
        self.time = 0.0

# Function to simulate the season
def simulate_season_MMR2(drivers):
    for driver in drivers:
        for race in range(12):  # For 12 races
            for lap in range(50):  # For 50 laps per race
                driver.time += driver.skill * random.uniform(0.97, 1.02)  # Add time based on experience
    
    # Sort drivers by their time (lower is better)
    mmr2_sorted = sorted(drivers, key=lambda x: x.time)
    
    # Best driver is the one with the lowest time
    best = mmr2_sorted[0]
    # Worst driver is the one with the highest time
    worst = mmr2_sorted[-1]  
    
    return best, worst

# Create a list of drivers with random experience
list_drivers_mmr2 = [drivermmr2(name, random.uniform(5.95, 8.05)) for name in drivers_mmr2]

# Run the simulation
best, worst = simulate_season_MMR2(list_drivers_mmr2)

class Car:
    def __init__(self, name, skill, is_player=False):
        self.name = name
        self.box = 0
        self.stints = []  
        self.position = []
        self.last_stint_start = 0 
        self.is_player = is_player
        self.pneu = random.choice(["medium", "tvrdé"])
        self.wear = 0.0
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

        if weather in ["déšť", "silný déšť"] and self.pneu not in ["mokré", "inter"]:
            base *= 0.3
        if weather == "silný déšť" and self.pneu not in ["mokré", "inter"]:
            base *= 0.2
        if weather == "slunečno" and self.pneu in ["mokré", "inter"]:
            base *= 0.5

        return base


    def simuluj_lap(self, weather, training, wettiness):
        global safety_car
        if self.dnf:
            return
        
        if self.wear >= 100:
            print(f"{self.name} – extrémní opotřebení! ❌")
            self.dnf = True
            return

        if self.puncture:
            print(f"{self.name} – defekt! ❌")
            safety_car = True
            return safety_car
        if self.wear > 80 and random.random() < 0.55:
            print(f"{self.name} – defekt! ❌")
            self.puncture = True
            self.dnf = True
            safety_car = True
            return safety_car

        speed = self.efectivity_pneu(weather)
        s1 = (TIME_S1*random.uniform(0.99, 1.01)+self.skills/2+self.team.skill/2)/ speed
        s2 = (TIME_S2*random.uniform(0.99, 1.01)+self.skills/2+self.team.skill/2)/ speed
        s3 = (TIME_S3*random.uniform(0.99, 1.01)+self.skills/2+self.team.skill/2)/ speed
        if safety_car:
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
        if wettiness < 30 and self.pneu not in ["měkké", "medium", "tvrdé"]:
            s1 = s1+wettiness/2
            s2 = s2+wettiness/2
            s3 = s3+wettiness/2
        if wettiness > 55 and self.pneu not in ["mokré" , "inter"]:
            s1 = s1+wettiness/2
            s2 = s2+wettiness/2
            s3 = s3+wettiness/2
        lap_time = s1 + s2 + s3
        time_laps.append((lap_time, self.name, self.team, s1, s2, s3))
        self.time = self.time + self.wear/8 + lap_time

            

        index = cars.index(self)
        self.wear += PNEU_types[self.pneu]["wear"]
        prirustek = PNEU_types[self.pneu]["wear"] * random.uniform(0, 0.4)
        self.wear += prirustek
    def pit_stop(self, new_pneu):
        if not self.dnf:
            self.stints.append((self.last_stint_start, self.time - self.last_stint_start, self.pneu))
        if safety_car == True:
            self.time += 50
        else: 
            self.time += 100
        self.box += 1
        self.last_pneu = self.pneu
        self.pneu = new_pneu
        self.wear = 0
        self.last_stint_start = self.time  

    def rozhodni_ai(self, weather, laps, max_laps, Forecast):
        if self.dnf:
            return None, False
        unava = self.wear
        zustava = max_laps - laps
        idealni = self.vhodne_pneu(Forecast[0])
        ideal_2 = self.vhodne_pneu(Forecast[2])

        self.pit = False
        if self.pneu not in idealni and self.pneu not in ideal_2 and zustava > 5:
            self.pit = True
        elif unava >= 80 and random.random() < 0.95:
            self.pit = True
        elif unava > 90 or (self.pneu not in idealni and random.random() > 0.9):
            self.pit = True
        elif safety_car and self.wear > 70 and zustava > 5:
            self.pit = True
        if Forecast[3] == "přechodný":
            idealni = "měkké"
        elif Forecast[0] in ["déšť", "silný déšť"] and LAPS - lap < 70/k_wear[3] and Forecast[2] == Forecast[0]:
            idealni = "mokré"
        elif Forecast[0] in ["déšť", "silný déšť"] and LAPS - lap < 70/k_wear[4] and Forecast[2] == Forecast[0]:
            idealni = "inter"
        elif Forecast[0] == "slunečno" and LAPS - lap < 70/k_wear[0] and Forecast[2] == Forecast[0]:
            idealni = "tvrdé"
        elif Forecast[0] == "slunečno" and LAPS- lap < 70/k_wear[1] and Forecast[2] == Forecast[0]:
            idealni = "medium"
        elif Forecast[0] == "slunečno" and LAPS - lap < 70/k_wear[2] and Forecast[2] == Forecast[0]:
            idealni = "měkké"
        elif Forecast[0] in ["přechodný", "slunečno", "déšť"] and Forecast[3] in ["déšť", "silný déšť"] or Forecast[0] in ["déšť", "silný déšť"] and Forecast[2] == Forecast[0] or Forecast[2] in ["déšť", "silný déšť"]:
            idealni = random.choice(["mokré" ,"mokré" , "inter"])
        elif Forecast[0] == "slunečno" and Forecast[2] == Forecast[0]:
            idealni = random.choice(["měkké" , "medium", "tvrdé", "medium", "tvrdé"])
        elif Forecast[0] in ["přechodný", "slunečno", "déšť"] and Forecast[3] in ["slunečno"]:
            idealni = random.choice(["měkké" , "medium", "tvrdé", "medium", "tvrdé"])
        return idealni if self.pit else None
    def player_info(self):
        if self.dnf == False:
            if safety_car == True:
                print(random.choice(["Still safety car", "Still spinning slowly lap by lap."]))
                if self.wear > 60:
                    print(random.choice(["Why didn’t we pit? We’ve just thrown away the race.", "I had no grip even before the safety car!", "Come on! These weathers are dead — what are we doing?!", "Are we sure about staying out? Tyres are cooked."]))
            print(f"\n🚗 Tvé auto {self.name}")
            rank = [a.name for a in cars if not a.dnf]     
            if driver_1 == self.name:
                position = rank.index(driver_1) + 1 if driver_1 in rank else count_cars
                print(f"Řidič 1 - {player.name}")
            else:
                position = rank.index(driver_2) + 1 if driver_2 in rank else  count_cars
                print(f"Řidič 2 - {player_2.name}")
            print(f"\n📊 Pozice: {position}. z {len(rank)}")
            fake_o = int(self.wear) - random.uniform(-4, 4)
            fake_o = int(fake_o)
            if fake_o < 0:
                fake_o = 0
            print(f"🛞  Pneu: {self.pneu} | Opotřebení: {fake_o}%")
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
                print(f"Delta před: {round(difference, 3)}s ({car_pred.team.nazev})| Delta za: {round(difference_2, 3)}s ({car_za.team.nazev})")
            elif index == 0:
                car_za = cars[index + 1]
                difference_2 = car_za.time - self.time
                print(f"Delta za: {round(difference_2, 3)}s ({car_za.team.nazev})")
            else:
                car_pred = len(cars)
                difference = self.time - car_pred.time
                print(f"Delta před: {round(difference, 3)}s ({car_pred.team.nazev})")
            if self.wear >= 70:
                print(random.choice(["The weathers are pretty done now.", "I don´t know what are you doing there, but I am boxing. Or at least I wish.", "The weathers are ***!", "Please, take me out from this hell." "Please box, please."]))
        return 
    def drss(self):
        for i in range(1, len(cars)): 
            current_time = self.time  
            previous_time = cars[i-1].time 

            time_difference = current_time - previous_time

            if time_difference < 1:
                self.drs = True
        return self.time, self.drs

    def simuluj_ai(self, training, wettiness):
        if self.is_player == False:
            new_pneu = self.rozhodni_ai(weather, lap, LAPS, Forecast)
            if new_pneu:
                self.pit_stop(new_pneu)
        wettiness = wettiness

        self.simuluj_lap(weather, training, wettiness)
    def vhodne_pneu(self, weather):
        if weather in ["silný déšť", "déšť"]:
                return ["mokré", "inter"]
        elif weather == "přechodný":
            return ["mokré", "inter", "měkké", "medium", "tvrdé"]
        else:
            return ["měkké", "medium", "tvrdé"]
    def vypocitej_points_jezdec(self, rank):
        if self.dnf == False:
            position = rank.index(self.name) + 1
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
    def __init__(self, nazev, skill):
        self.nazev = nazev
        self.skill = skill
        self.drivers = [] 
        self.points = 0   

    def pridej_jezdce(self, car):
        self.drivers.append(car)
        car.team = self

    def vypocitej_points(self, rank):
        for jezdec in self.drivers:
            if jezdec.name in rank:
                position = rank.index(jezdec.name) + 1
            else:
                position = count_cars
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
drivers = ["Alex Storme","Matteo Blaze","Hiro Tanaka","Lukas Renntvrdét","Diego Ventura","Aiden Falk","Pierre Lucien","Nikolai Vetrovski","Riku Yamashita","Carlos Navarro","Johan Reißer","Theo Hartman","Enzo DaCosta","Sebastian Krell","Marco Falcone","Ivan Vasiliev","Tyler Quinn","Jae-Min Han","Felipe Marquez","Elias Northgate","Arjun Desai","Tomás Moreira","Leo Krüger","Mikhail Antonov","Julian Stroud","Renzo Morandi"]
x = 0
cars = []
for driver in drivers:
    cars.append(Car(driver,random.uniform(5, 6)))
player = Car(driver_1, random.uniform(5, 6), is_player=True)
cars.append(player)
player_2 = Car(driver_2, random.uniform(5, 6), is_player=True)
cars.append(player_2)
teams = []
def create_team(team_player, player_1, player_2, teams, skill):
    tym = Team(team_player, skill)
    tym.pridej_jezdce(player_1)
    tym.pridej_jezdce(player_2)
    teams.append(tym)
    return tym
create_team(team_player, player, player_2, teams,                               random.uniform(5,   6))
create_team("Scuderia Python", cars[0], cars[1], teams,                         random.uniform(4,   6.9))
create_team("Racing 404",cars[2],cars[3], teams,                                random.uniform(4.5, 6))
create_team("Formula 1.0 racing team",cars[4],cars[5], teams,                   random.uniform(4,   6))
create_team("Microměkké PitStop Protocol racing team",cars[6],cars[7], teams,    random.uniform(4,   6))
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
lenght = int(input("Jaká je délka šampionátu: "))
hi = len(championship) - lenght
if hi > 0:
    for _ in range(hi):
        championship.pop(random.randint(0, len(championship)-1))
season_count = 1
while len(names_free_drivers) >= 0:
    print(f"Sezóna {season_count}")
    b = 1
    for race in championship:
        climax = random.choice(["přechodný","slunečno","slunečno","slunečno"])
        lap = 0
        if race == "Huawei GP SPA":
            pneu = "tvrdé"
            speed = "quick"
            TIME_S1 = 22
            TIME_S2 = 25
            TIME_S3 = 18
            LAPS = 70
            dnf_probability = 4500
        if race == "LG TV Grand Prix du France":
            pneu = "tvrdé"
            speed = "quick"
            TIME_S1 = 26
            TIME_S2 = 19
            TIME_S3 = 22
            LAPS = 74
            dnf_probability = 4500
        if race == "Sony Varsava Grand Prix":
            pneu = "tvrdé"
            speed = "medium"
            TIME_S1 = 35
            TIME_S2 = 18
            TIME_S3 = 24
            LAPS = 62
            dnf_probability = 5000
        if race == "META China Grand Prix":
            pneu = "medium"
            speed = "slow"
            TIME_S1 = 25
            TIME_S2 = 34
            TIME_S3 = 30
            LAPS = 56
            dnf_probability = 4500
        if race == "Ostrava Apple GP":
            pneu = "medium"
            speed = "quick"
            TIME_S1 = 20
            TIME_S2 = 26
            TIME_S3 = 18
            LAPS = 67
            dnf_probability = 4500
        if race == "Python circuit Bahamas":
            pneu = "tvrdé"
            speed = "medium"
            TIME_S1 = 25
            TIME_S2 = 23
            TIME_S3 = 38
            LAPS = 72  
            dnf_probability = 5000
        if race == "HP Bulgarian GP":
            pneu = "medium"
            speed = "medium"
            TIME_S1 = 23
            TIME_S2 = 29
            TIME_S3 = 20
            LAPS = 60
            dnf_probability = 5000
        if race == "AWS Grand Prix de Espana":
            pneu = "medium"
            speed = "quick"
            TIME_S1 = 26
            TIME_S2 = 31
            TIME_S3 = 12
            LAPS = 51
            dnf_probability = 6000
        if race == "AirBNB Prague GP":
            pneu = "měkké"
            speed = "quick"
            TIME_S1 = 20
            TIME_S2 = 33
            TIME_S3 = 40
            LAPS = 42
            dnf_probability = 4500
        if race == "eBay Skyline Turkey GP":
            pneu = "medium"
            speed = "slow"
            TIME_S1 = 27
            TIME_S2 = 24
            TIME_S3 = 36
            LAPS = 49
            dnf_probability = 4900
        if race == "Java airlines Monza IBM Italy GP":
            pneu = "měkké"
            speed = "quick"
            TIME_S1 = 30
            TIME_S2 = 16
            TIME_S3 = 18
            LAPS = 50
            dnf_probability = 5100
        print(f"Aktuální závod {race} {b}/{len(championship)}")
        print(f"Trať je charakteristická pro {pneu} pneu a {speed} rychlost. Má {LAPS} kol")
        strategy(LAPS, TIME_S1, TIME_S2, TIME_S3, pneu, speed)

        if pneu == "medium":
            k_wear = [1.5,5,9,4.4,8.4]
        elif pneu == "měkké":
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
        "tvrdé": {"wear": k_wear[0], "speed": k_speed[0]},
        "medium": {"wear": k_wear[1], "speed": k_speed[1]},
        "měkké": {"wear": k_wear[2], "speed": k_speed[2]},
        "mokré": {"wear": k_wear[3], "speed": k_speed[3]},
        "inter": {"wear": k_wear[4], "speed": k_speed[4]},
        }
        if climax == "slunečno":
            weather = "slunečno"
        else:
            weather = random.choice(WEATHER_TYPES)
        if weather == "déšť" or weather == "silný déšť":
            wettiness = 100
        weather_1 = generate_weather(weather)
        weather_2 = generate_weather(weather_1)
        weather_3 = generate_weather(weather_2)
        weather_4 = generate_weather(weather_3)
        Forecast = [weather_1, weather_2, weather_3, weather_4]
        print(f"Bude {climax}")
        for x in Forecast:
            print (f"Počasí: 🌤️ ☁️  {x}")
        for car in cars:
            car.pneu = random.choice(["tvrdé", "medium"])
        player.pneu = input("Vyber pneu pro řidiče 1: [tvrdé / medium / měkké / mokré / inter]\n")
        while player.pneu not in PNEU_types:
            player.pneu = input("Špatná volba. Vyber pneu pro řidiče 1: [tvrdé / medium / měkké / mokré / inter]\n")
            if player.pneu == "exit":
                continue
        player_2.pneu = input("Vyber pneu pro řidiče 2: [tvrdé / medium / měkké / mokré / inter]\n")
        while player_2.pneu not in PNEU_types:
            player_2.pneu = input("Špatná volba. Vyber pneu pro řidiče 2: [tvrdé / medium / měkké / mokré / inter]\n")
            if player.pneu == "exit":
                continue
        for c in cars:
            if c.is_player == False:
                if weather_1 == "déšť" or weather_1 == "silný déšť":
                    c.pneu = random.choice(["mokré", "inter"])
                if weather_1 == "přechodný":
                    c.pneu = random.choice(["měkké", "inter"])
        simulation = []
        #Tdéšťing
        training = input("Chceš trénink na [1] nebo kvalifikaci [2]: ")
        #Quali
        for car in cars:
            sim_time = TIME_S1 * random.uniform(0.9, 1.1) + TIME_S2 * random.uniform(0.9, 1.1) + TIME_S3 * random.uniform(0.9, 1.1)
            if car.is_player and training == "2":
                sim_time = sim_time/1.5 
            simulation.append((car, sim_time))
        simulation.sort(key=lambda x: x[1])
        for i, (car, sim_time) in enumerate(simulation):
            penalizovany_time =  5 * i
            car.time += penalizovany_time
        ######################################################################################################################################################################
        while lap <= LAPS:
            if lap == LAPS:
                print("Poslední kolo. Push push.")
            info(wettiness)
            for car in cars:


                if weather == "slunečno":
                    if random.randint(1, dnf_probability) == 1:
                        if lap >= 3:
                            car.dnf = True
                            safety_car = True
                            laps_remaining = random.randint(3,6)
                            print(f"{car.name} recieved DNF")
                            print(random.choice([
                        "Radio: Crash ahead, safety car is out!",
                        "Radio: We’ve got yellow flags – full course yellow!",
                        "Radio: Big crash, bring the delta in check.",
                        "Radio: Watch the debris – SC deployed!"
                    ]))
                else:
                    if random.randint(1, (dnf_probability/5)) == 1:
                        if lap >= 3:
                            car.dnf = True
                            safety_car = True
                            laps_remaining = random.randint(3,6)
                            print(f"{car.name} recieved DNF")
                            print(random.choice([
                        "Radio: Crash ahead, safety car is out!",
                        "Radio: We’ve got yellow flags – full course yellow!",
                        "Radio: Big crash, bring the delta in check.",
                        "Radio: Watch the debris – SC deployed!"
                    ]))
            if safety_car == True:
                laps_remaining -=1
            if laps_remaining == 0:
                safety_car = False
            cars.sort(key=lambda x: (x.dnf, x.time))
            for car in cars:
            # sem patří tvůj kód

                if car.is_player:
                    car.player_info()

            cars.sort(key=lambda x: (x.dnf, x.time))
            cars = [a for a in cars] 

            car.drss()

            for i, car in enumerate(cars):
                cars = [a for a in cars] 

                if i > 0:
                    car_pred = cars[i - 1]
                    difference = car.time - car_pred.time
                    if difference < 1.5 and difference > 0:
                        defence = random.uniform(0.6, 0.95)
                        chance_predjeti = max(0.1, 1.5 - difference) * 0.4  # 
                        if car.drs == True:
                            chance_predjeti += 0.3
                        if defence  < chance_predjeti:
                            car.wear += 3
                            cars[i], cars[i - 1] = cars[i - 1], cars[i]
            cars.sort(key=lambda x: (x.dnf, x.time))

            pit_player()
            cars.sort(key=lambda x: (x.dnf, x.time))
            timecar = 0
            rank = [a.name for a in cars if not a.dnf]  # Move this line here
            position = rank.index(driver_1) + 1 if driver_1 in rank else count_cars
            position_2 = rank.index(driver_2) + 1 if driver_2 in rank else count_cars


            #rank = [a.name for a in cars if not a.dnf]
            wettiness = mokré_track(weather_1, wettiness)
            #position = rank.index(driver_1) + 1 if driver_1 in rank else "DNF"
            print(f"\n📊 Pořadí {driver_1}: {position}. místo z {len(rank)}")
            #position_2 = rank.index(driver_2) + 1 if driver_2 in rank else "DNF"
            print(f"\n📊 Pořadí {driver_2}: {position_2}. místo z {len(rank)}")
            drivers_table()
            for car in cars:
                car.simuluj_ai(training, wettiness)
            boxy_po_teamu = {}
            for a in cars:
                if not a.is_player and a.pit: 
                    team = a.team
                    if team not in boxy_po_teamu:
                        boxy_po_teamu[team] = 0
                    boxy_po_teamu[team] += 1

            for team, count in boxy_po_teamu.items():
                if count >= 2:
                    print(f"{team.nazev} jde do double stacku.")
                    for a in cars:
                        if a.team == team and a.pit:
                            position = rank.index(a) + 1 if a in rank else count_cars
                            a.time += 50
            boxy_po_teamu.clear()
            cars.sort(key=lambda x: (x.dnf, x.time))
            rank = [a for a in cars if not a.dnf]  
            for a in cars:
                if a in rank:  
                    position = rank.index(a) + 1  
                else:
                    position = count_cars  
                a.position.append(position)  # Add position

            # posun počasí
            weather = Forecast.pop(0)
            weather_1 = Forecast[0]
            weather_2 = Forecast[1]
            weather_3 = Forecast[2]
            Forecast.append(generate_weather(weather_3))
            weather_4 = Forecast[3]
            lap += 1
        print("\n🏁 KONEC ZÁVODU!!")
        
        time_laps.sort()
        print(f"{time_laps[0][1]} ({time_laps[0][2].nazev}) má nejrychlejší kolo: {round(time_laps[0][0], 3)}")
        for a in cars:
            a.skills -= 0.01
        sector_1 = min(time_laps, key=lambda x: x[3])
        sector_2 = min(time_laps, key=lambda x: x[4])
        sector_3 = min(time_laps, key=lambda x: x[5])

        print(f"{sector_1[1]} ({sector_1[2].nazev}) má nejrychlejší sektor 1 {round(sector_1[3], 3)}")
        print(f"{sector_2[1]} ({sector_2[2].nazev}) má nejrychlejší sektor 2 {round(sector_2[4], 3)}")
        print(f"{sector_3[1]} ({sector_3[2].nazev}) má nejrychlejší sektor 3 {round(sector_3[5], 3)}")

        time_laps[0][2].points += 2
        for d in range(len(time_laps)):
            if time_laps[d][1] == player.name:
                print(f"{time_laps[d][1]} ({time_laps[d][2].nazev}) má nejrychlejší kolo {round(time_laps[d][0], 3)}, sektor 1 {round(time_laps[d][3], 3)}, sektor 2 {round(time_laps[d][4], 3)}, sektor 3 {round(time_laps[d][5], 3)}")
                break
        for d in range(len(time_laps)):
            if time_laps[d][1] == player_2.name:
                print(f"{time_laps[d][1]} ({time_laps[d][2].nazev}) má nejrychlejší kolo {round(time_laps[d][0], 3)}, sektor 1 {round(time_laps[d][3], 3)}, sektor 2 {round(time_laps[d][4], 3)}, sektor 3 {round(time_laps[d][5], 3)}")
                break
        #time.sleep(6)
        #
        ## Import to CSV
        #with open("vysledky_zavodu.csv", "w", newline="", encoding="utf-8") as file:
        #    writer = csv.writer(file)
        #    writer.writerow(["Rank", "Jezdec", "Čas (min)", "Počet pit stopů", "DNF", "Stinty"])
        #    for i, a in enumerate(cars, 1):
        #        time = round(a.time / 60, 2) if not a.dnf else "DNF"
        #        stint_popis = "; ".join(
        #            [f"{round(start/60, 1)}–{round((start+doba)/60, 1)}min: {typ}" for start, doba, typ in a.stints]
        #        )
        #        writer.writerow([i, a.name, time, a.box, a.dnf, stint_popis])


        # Make sure, list is without dnf
        rank = [a.name for a in cars if not a.dnf]
        for driver in cars:
            driver.vypocitej_points_jezdec(rank)
            driver.skills -= 0.01
        for team in teams:
            team.vypocitej_points(rank)
        points = sorted(teams, key=lambda x: (x.points))
        # Rank count
        position_1 = rank.index(driver_1) + 1 if driver_1 in rank else "DNF"
        position_2 = rank.index(driver_2) + 1 if driver_2 in rank else "DNF"
        print(f"\n🏁 Finalní pozice:")
        print(f"{driver_1}: {position_1}. místo")
        print(f"{driver_2}: {position_2}. místo")
        #time.sleep(4)
        # Results
        cars.sort(key=lambda x: (x.dnf, x.time))
        for i, a in enumerate(cars, 1):
            stav = "DNF" if a.dnf else f"{round(a.time, 2)}s"
            print(f"{i}. {a.name} ({a.team.nazev}) {a.points} body")
        teams.sort(key=lambda team: team.points, reverse=True)
        #time.sleep(8)
        for i, team in enumerate(teams,1):
            print (f"{i}.{team.nazev} {team.points} body")
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
        plt.xlabel("Čas (min)")
        plt.ylabel("řidiči")
        plt.title("🏁 Výsledky závodu")
        plt.tight_layout()
        plt.show()
        plt.figure(figsize=(10, 6))
        for a in cars:
            plt.plot(range(1, len(a.position) + 1), a.position, label=a.name)

        plt.gca().invert_yaxis()  # cause first place is the best
        plt.xlabel("Kolo")
        plt.ylabel("Pozice")
        plt.title("Pozice během závodu")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        plt.figure(figsize=(10, 6))
        players = [player, player_2]
        for a in players:
            plt.plot(range(len(a.position)), a.position, label=a.name)

        plt.gca().invert_yaxis()  # cause first place is the best
        plt.xlabel("Kolo")
        plt.ylabel("Pozice")
        plt.title("Pozice během závodu")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        reset_race()
        b += 1
    print("\n🏁 Jezdci na konci šmapionátu:")
    best, worst = simulate_season_MMR2(list_drivers_mmr2)
    season_count +=1
    for d in list_drivers_mmr2:
        d.skill -= 1/(season_count*2)
    random_name = random.choice(names_free_drivers)
    names_free_drivers.pop(names_free_drivers.index(random_name))
    worst.nazev, worst.skill = random_name, random.uniform(0.95,1.05)
    cars.sort(key=lambda x: x.points, reverse=True)
    for i, a in enumerate(cars, 1):
        print(f"{i}. {a.name} – {a.points} body ({a.team.nazev})")
        if i == len(cars):
            new = best.name
            skill = best.skill
            print(f"Breaking!!!\n{new} mění {a.name} ({a.team.nazev})\nBreaking!!!")
            if a.is_player:
                if driver_1 == a.name:
                    driver_1 = new
                    player.name, player.skills = new, skill
                if driver_2 == a.name:
                    driver_2 = new
                    player_2.name, player_2.skills = new, skill
            best.name, best.skill = a.name, a.skills
            a.name, a.skills = new, skill
    print("\n🏆 Týmy na konci šmapionátu:")
    teams.sort(key=lambda t: t.points, reverse=True)
    for i, t in enumerate(teams, 1):
        if i == 1:  
            t.skill += 1
            img = mpimg.imread(f'{t.nazev}.png')
            plt.imshow(img)
            plt.axis('off')  # Optional: hides axis for image display
            plt.show()
        print(f"{i}. {t.nazev} – {t.points} body")
        if i == len(teams):
            t.skill -=1
    wettiness = 0
    for c in cars:
        c.points = 0
    for t in teams:
        t.points = 0   