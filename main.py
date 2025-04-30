import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#import csv
rank = 0
names_free_drivers = [    "Maximilian Becker", "Santiago Cruz",   "Oliver Wright", "Hiroshi Takeda",     "Sebastian Fontaine", "Mateo Silva",     "Jonas Lindberg", "Ivan Kuznetsov",     "Lorenzo Bianchi", "Connor Mitchell",    "Rafael Ortega", "Tobias Schmidt",     "Yuto Nakamura", "Charles Lambert",     "Gabriel Costa", "Andrei Petrescu",    "Lutime Meyer", "Zhang Wei",     "Finn Gallagher", "Ricardo Santos"]
TIME_S1 = 15
TIME_S2 = 23
TIME_S3 = 22
time_laps = []
LAPS = 0
laps_rem = 0
driver_1 = "Max"
driver_2 = "Kim"
team_player = "MySql AWS Maxim racing team"
count_cars = 28

WEATHER_TYPES = ["sunny", "transitional", "rain", "strong_rain"]
pneu_colours = {
    "hard": "gray",
    "medium": "yellow",
    "soft": "red",
    "inter": "green",
    "wet": "deepskyblue"
}
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
            colours.append("green")  # fallback
    return colours
def info():
    Forecast = [weather_1, weather_2, weather_3, weather_4]
    if lap == 0:
        print(f"Qualification | Actual weather: {tyre}")
    else:
        print(f"\n🌤️  lap {lap}/{LAPS} | Actual weather: {tyre}")
    if random.randint(1, 10) < 8:
        print(f"🔮 Forecast: {', '.join(Forecast)}")
        if weather_1 == "sunny" and weather_4 in ["rain", "strong_rain"]:
            print(random.choice(["We’re monitoring the weather, expect rain in 3 laps.", "Rain is coming in now, you should start thinking about wet tires soon.", "Rain intensity increasing, we expect full wet conditions in the next 3 laps."]))
            print(random.choice(["Copy that, adjusting my pace.", "Understood, I’m keeping an eye on it.","OK"]))
    else:
        fake = [generate_weather(tyre) for _ in range(4)]
        print(f"🔮 Forecast: {', '.join(fake)}")
        if fake[0] == "sunny" and fake[3] in ["rain", "strong_rain"]:
            print(random.choice(["We’re monitoring the weather, expect rain in 3 laps.", "Rain is coming in now, you should start thinking about wet tires soon.", "Rain intensity increasing, we expect full wet conditions in the next 3 laps."]))
            print(random.choice(["Copy that, adjusting my pace.", "Understood, I’m keeping an eye on it.","OK"]))
    return Forecast
def generate_weather(tyre):
    if tyre == "sunny":
        tyre = random.choice(["sunny", "sunny","sunny","sunny", "sunny", "sunny","sunny","sunny","sunny", "sunny","sunny","sunny", "sunny", "sunny","sunny","sunny","sunny", "sunny","sunny","sunny", "sunny", "sunny","sunny","sunny", "sunny", "sunny","sunny","sunny", "transitional"])
    elif tyre == "transitional":
        tyre = random.choice(["sunny", "transitional", "transitional","transitional","rain"])
    elif tyre == "rain":
        tyre = random.choice(["transitional", "rain", "rain", "rain", "rain", "rain", "rain", "rain", "rain", "rain", "strong_rain"])
    elif tyre == "strong_rain":
        tyre = random.choice(["rain", "rain", "strong_rain", "strong_rain", "strong_rain", "strong_rain", "strong_rain", "strong_rain", "strong_rain", "strong_rain"])
    return tyre
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
            print(f"Number of pit stops: {a.box} Tyre wear: {heloo}%")
            status_1 = round(status, 3)
        else:
            distance = round(status - status_1, 3)
            print(f"{i}. {a.name} + {distance} s")
            heloo = round(a.wear) * random.uniform(0.9, 1.1)
            heloo = round(heloo, 1)
            print(f"Number of pit stops: {a.box} Tyre wear: {heloo}%")
            status_1 = status
def reset_race():
    global lap, time_laps, safety_car, laps_rem, Forecast, tyre
    lap = 0
    time_laps = []
    safety_car = False
    laps_rem = 0
    tyre = "sunny"
    Forecast = [generate_weather(tyre)]
    for _ in range(3):
        Forecast.append(generate_weather(Forecast[-1]))
    for a in cars:
        a.time = 0
        a.dnf = False
        a.wear = 0
        a.position = []
        a.puncture = False
        a.box = 0
        a.stinty = []
        a.last_stint_start = 0
    return lap, time_laps, safety_car, laps_rem, tyre, Forecast, cars
def pit_player():
    volba = 1
    volba_2 = 1
    if player.dnf is False:
        print("Action: [1] Continue [2] Box for driver 1")
        volba = input("> ").strip()
        if volba == "2":
            print("Choose pneu for driver 1: [hard / medium / soft / wet / inter]")
            strategy(LAPS-lap, TIME_S1, TIME_S2, TIME_S3, pneu, speed)                
            new = input("> ").strip().lower()
            while new not in PNEU_types:
                new = input("Incorrect choice. Choose pneu for driver 2: [hard / medium / soft / wet / inter]\n")
            if new in PNEU_types:
                player.pit_stop(new)
            else:
                print("Neplatná volba – pokračuješ.")
    if player_2.dnf is False:
        print("Action: [1] Continue [2] Box for driver 2")
        volba_2 = input("> ").strip()
        if volba_2 == "2":
            print("Choose pneu for driver 2: [hard / medium / soft / wet / inter]")
            strategy(LAPS-lap, TIME_S1, TIME_S2, TIME_S3, pneu, speed)  
            new = input("> ").strip().lower()
            while new not in PNEU_types:
                new = input("Incorrect choice. Choose pneu for driver 2: [hard / medium / soft / wet / inter]\n")
            if new in PNEU_types:
                player_2.pit_stop(new)
            else:
                print("Neplatná volba – pokračuješ.")
    if player.dnf == True or player_2.dnf==True:
        if volba == "2" and volba_2 == "2":
            print(random.choice(["Box now, double stack. Maintain gap, all planned.",  "Box, box, double stack! Close gap, no mistakes!",  "Box this lap, we’re double stacking. Maintain delta, we’ve got margin.",  "Plan B, box now. You’ll be second in the stack, minimal delay expected.",  "Box this lap for double stack. First car in now, stand by for release.",  "Box this lap, we are double stacking. Pit crew is prepped for both."]))
            print( "Copy. Keeping gap, I’m right behind.",  "Understood. Staying tight.",  "Copy. I’m ready.",  "Confirmed. I’ll hit my marks.")
            player.time += 3
            player_2.time += 3
        elif volba_2 == "2" and volba != "2" or volba == "2" and volba_2 != "2":
            print(random.choice(["Box, box. Box this lap. Tyres ready, confirm entry.",  "Pit window is open. Box this lap for new tyres.",  "Box now. Hitting your marks is critical.",  "Box, box. Tyre temps look good — execute clean entry.",  "Pit this lap. We’re switching compound."]))
            print(random.choice([ "Copy. In this lap.",  "Understood. Coming in.",  "On my way in.", "Copy. Box, box",  "Copy, box this lap.", "Copy, confirmed."]))
def strategy(LAPS, TIME_S1, TIME_S2, TIME_S3, pneu, speed):
    pocet_laps = LAPS
    lap_time = (TIME_S1 + TIME_S2 + TIME_S3)/60
    if pneu == "medium":
        k_wear = [1.5,5,9,4.4,8.4]
    elif pneu == "soft":
        k_wear = [2,7,12,5,9]       
    else:
        k_wear = [1,4,7,4,8]
    if speed == "medium":
        k_speed = [1,1.05,1.12,0.6,0.65]
    elif speed == "quick":
        k_speed = [1.05,1.12,1.15,0.65,0.7]
    else:
        k_speed = [0.95,1,1.05,0.55,0.6]
    vydrz_s = 65/k_wear[2]*k_speed[2]
    vydrz_m = 65/k_wear[1]*k_speed[1]
    vydrz_h =65/k_wear[0]*k_speed[0]
    vydrze = [vydrz_h, vydrz_m, vydrz_s]
    nazev = ["Hard", "Medium", "Soft"]
    box_time = (100/60)
#    time = round((lap_time*LAPS)/60*prych, 0)
    for i, stint in enumerate(vydrze, 0):
        if pocet_laps + 4 < vydrze[i] < pocet_laps +20:
            #zbytek = pocet_laps - vydrze[i]
            zbytek = vydrze[i] - pocet_laps
            prych = (vydrze[i] - zbytek)*k_speed[i]/pocet_laps
            #prych = (k_speed[i]*vydrze[i])/pocet_laps
            time = round((lap_time*LAPS)/prych, 2)

            print(f"Theoretical strategy - {round(stint, 0)} laps - {time} minut - {nazev[i]}")

#    zbytek = vydrz1 + vydrz2 - laps
#    pocetlapsvydrz2 = vydrz2 - zbytek 
#    prych = (k_speed[i]*vydrz1 + pocet_lapsvydrz2*k_speed[0])/pocet_laps

    for i in range(len(vydrze)):
        if pocet_laps + 4 < vydrze[i] + vydrze[0] < pocet_laps +20:
            zbytek = vydrze[i] + vydrze[0]- pocet_laps
            pocetlapsvydrz2 = vydrze[0] - zbytek
            prych = (k_speed[i]*vydrze[i] + pocetlapsvydrz2*k_speed[0])/pocet_laps
            time = round(((lap_time*LAPS)/prych) + box_time, 2)
            if pocetlapsvydrz2 > 0:
                print(f"Theoretical strategy - {round(vydrze[i] + vydrze[0],0)} laps - {time} minut - {nazev[i]}, {nazev[0]}")
        if pocet_laps + 4 < vydrze[i] + vydrze[1]  < pocet_laps +20:
            zbytek = vydrze[i] + vydrze[1]- pocet_laps
            pocetlapsvydrz2 = vydrze[1] - zbytek
            prych = (k_speed[i]*vydrze[i] + pocetlapsvydrz2*k_speed[1])/pocet_laps
            time = round(((lap_time*LAPS)/prych) + box_time, 2)
            if pocetlapsvydrz2 > 0:
                print(f"Theoretical strategy - {round(vydrze[i] + vydrze[1],0)} laps - {time} minut - {nazev[i]}, {nazev[1]}")
        if pocet_laps + 4 < vydrze[i] + vydrze[2]  < pocet_laps +20:
            zbytek = vydrze[i]+ vydrze[2] - pocet_laps
            pocetlapsvydrz2 = vydrze[2] - zbytek
            prych = (k_speed[i]*vydrze[i] + pocetlapsvydrz2*k_speed[2])/pocet_laps
            time = round(((lap_time*LAPS)/prych) + box_time, 2)
            if pocetlapsvydrz2 > 0:
                print(f"Theoretical strategy - {round(vydrze[i] + vydrze[2], 0)} laps - {time} minut - {nazev[i]}, {nazev[2]}")
    for i in range(len(vydrze)):
        for j in range(len(vydrze)):
            if pocet_laps + 4 <vydrze[i] + vydrze[j] + vydrze[0]  < pocet_laps +20:
                zbytek = vydrze[i] + vydrze[j]  + vydrze[0] - pocet_laps
                pocetlapsvydrz2 = vydrze[0] - zbytek
                prych = (k_speed[i]*vydrze[i] + k_speed[j]*vydrze[j]+ pocetlapsvydrz2*k_speed[0])/pocet_laps
                time = round((lap_time*LAPS/prych) + box_time*2, 2)
                if pocetlapsvydrz2 > 0:
                    print(f"Theoretical strategy - {round(vydrze[i] + vydrze[j] + vydrze[0], 0)} laps - {round(lap_time*(vydrze[i] + vydrze[j]+vydrze[0]) + box_time*2, 0)} minut - {nazev[i]}, {nazev[j]}, {nazev[0]}")
            if pocet_laps + 4 <vydrze[i] + vydrze[j] + vydrze[1]  < pocet_laps +20:
                zbytek = vydrze[i] + vydrze[j]  + vydrze[1]- pocet_laps
                pocetlapsvydrz2 = vydrze[1] - zbytek
                prych = (k_speed[i]*vydrze[i] + k_speed[j]*vydrze[j]+ pocetlapsvydrz2*k_speed[1])/pocet_laps
                time = round(((lap_time*LAPS)/prych) + box_time*2, 2)
                if pocetlapsvydrz2 > 0:
                    print(f"Theoretical strategy - {round(vydrze[i] + vydrze[j] + vydrze[1], 0)} laps - {round(lap_time*(vydrze[i] + vydrze[j]+vydrze[1]) + box_time*2, 0)} minut - {nazev[i]}, {nazev[j]}, {nazev[1]}")
            if pocet_laps + 4 <vydrze[i] + vydrze[j] + vydrze[2]  < pocet_laps +20:
                zbytek = vydrze[i] + vydrze[j] + vydrze[2]- pocet_laps
                pocetlapsvydrz2 = vydrze[2] - zbytek
                prych = (k_speed[i]*vydrze[i] + k_speed[j]*vydrze[j]+ pocetlapsvydrz2*k_speed[2])/pocet_laps
                time =  round(((lap_time*LAPS)/prych) + box_time*2, 2)
                if pocetlapsvydrz2 > 0:
                    print(f"Theoretical strategy - {round(vydrze[i] + vydrze[j] + vydrze[2], 0)} laps - {time} minut - {nazev[i]}, {nazev[j]}, {nazev[2]}")
drivers_mmr2 = [
    "Noah Blake", "Felipe Sandoval", "Luca Moretti", "Brian Chen", "Adam newk", "Pierre Gauthier",
    "Viktor Orlov", "Daisuke Tanaka", "Elias Müller", "Jordan Evans", "Diego Ramirez", "Anton Petrov",
    "Kenji Nakamura", "Nicolas Dubois", "Thomas Fischer", "Miguel Lopez", "Alexei Solapv", "Ethan Zhang",
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
        for zavod in range(12):  # For 12 races
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
list_drivers_mmr2 = [drivermmr2(name, random.uniform(0.95, 1.05)) for name in drivers_mmr2]

# Run the simulation
best, worst = simulate_season_MMR2(list_drivers_mmr2)
#for driver in drivers_mmr2:
#    drivermmr2(driver,random.uniform(0.95, 1))
class Car:
    def __init__(self, name, skill, is_player=False):
        self.name = name
        self.box = 0
        self.stinty = []  # seznam úseků race (start_time, délka, pneu)
        self.position = []
        self.last_stint_start = 0  # čas začátku aktuálního stintu
        self.is_player = is_player
        self.pneu = random.choice(["medium", "hard"])
        self.wear = 0.0
        self.skills = skill
        self.time = 0.0
        self.points = 0
        self.drs = False
        self.team = None
        self.dnf = False
        self.puncture = False

    def efectivity_pneu(self, tyre):
        # Zajisti, že pneumatika je string
        if isinstance(self.pneu, list):
            self.pneu = self.pneu[0]

        base = PNEU_types[self.pneu]["speed"]

        if tyre in ["rain", "strong_rain"] and self.pneu not in ["wet", "inter"]:
            base *= 0.3
        if tyre == "strong_rain" and self.pneu not in ["wet", "inter"]:
            base *= 0.2
        if tyre == "sunny" and self.pneu in ["wet", "inter"]:
            base *= 0.5

        return base


    def simuluj_lap(self, tyre, training):
        global safety_car
        if self.dnf:
            return
        
        if self.wear >= 100:
            print(f"{self.name} – extrémní wear! ❌")
            self.dnf = True
            return

        if self.puncture:
            print(f"{self.name} – puncture! ❌")
            safety_car = True
            return safety_car
        if self.wear > 80 and random.random() < 0.55:
            print(f"{self.name} – puncture! ❌")
            self.puncture = True
            self.dnf = True
            safety_car = True
            return safety_car

        speed = self.efectivity_pneu(tyre)
        s1 = TIME_S1*random.uniform(0.98, 1.02)*self.skills*self.team.skill/ speed
        s2 = TIME_S2*random.uniform(0.98, 1.02)*self.skills*self.team.skill/ speed
        s3 = TIME_S3*random.uniform(0.98, 1.03)*self.skills*self.team.skill/ speed
        if safety_car:
            s1 = s1*2.5
            s2 = s2*2.5
            s3 = s3*2.5
        if self.drs:
            s1 = s1 - random.uniform(0.2, 0.3)
            s2 = s2 - random.uniform(0.2, 0.3)
            s3 = s3 - random.uniform(0.2, 0.3)
        if training == "2":
            s1 = s1 - random.uniform(0.1, 0.3)
            s2 = s2 - random.uniform(0.1, 0.3)
            s3 = s3 - random.uniform(0.1, 0.3)
        if tyre in ["sunny"] and self.pneu not in ["soft", "medium", "hard"]:
            s1 = s1*3
            s2 = s2*3
            s3 = s3*3
        if tyre in ["rain", "strong_rain"] and self.pneu not in ["wet" , "inter"]:
            s1 = s1*3
            s2 = s2*3
            s3 = s3*3
        lap_time = s1 + s2 + s3
        time_laps.append((lap_time, self.name, self.team, s1, s2, s3))
        self.time = self.time + self.wear/10 + lap_time

            
        #global cars  # použijeme globální seznam aut
        #cars.sort(key=lambda x: (x.dnf, x.time))  # seřadíme cars podle času
        index = cars.index(self)
        self.wear += PNEU_types[self.pneu]["wear"]
        prirustek = PNEU_types[self.pneu]["wear"] * random.uniform(0, 0.4)
        self.wear += prirustek
    def pit_stop(self, new_pneu):
    # Ulož předchozí stint
        if not self.dnf:
            self.stinty.append((self.last_stint_start, self.time - self.last_stint_start, self.pneu))
        if safety_car == True:
            self.time += 50
        else: 
            self.time += 100
        self.box += 1
        self.predchozi_pneu = self.pneu
        self.pneu = new_pneu
        self.wear = 0
        self.last_stint_start = self.time  # nový stint začíná od nového času

    def rozhodni_ai(self, tyre, laps, max_laps, Forecast):
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
        if Forecast[3] == "transitional":
            idealni = "soft"
        elif Forecast[0] in ["rain", "strong_rain"] and LAPS - lap < 70/k_wear[3] and Forecast[2] == Forecast[0]:
            idealni = "wet"
        elif Forecast[0] in ["rain", "strong_rain"] and LAPS - lap < 70/k_wear[4] and Forecast[2] == Forecast[0]:
            idealni = "inter"
        elif Forecast[0] == "sunny" and LAPS - lap < 70/k_wear[0] and Forecast[2] == Forecast[0]:
            idealni = "hard"
        elif Forecast[0] == "sunny" and LAPS- lap < 70/k_wear[1] and Forecast[2] == Forecast[0]:
            idealni = "medium"
        elif Forecast[0] == "sunny" and LAPS - lap < 70/k_wear[2] and Forecast[2] == Forecast[0]:
            idealni = "soft"
        elif Forecast[0] in ["transitional", "sunny", "rain"] and Forecast[3] in ["rain", "strong_rain"] or Forecast[0] in ["rain", "strong_rain"] and Forecast[2] == Forecast[0] or Forecast[2] in ["rain", "strong_rain"]:
            idealni = random.choice(["wet" ,"wet" , "inter"])
        elif Forecast[0] == "sunny" and Forecast[2] == Forecast[0]:
            idealni = random.choice(["soft" , "medium", "hard", "medium", "hard"])
        elif Forecast[0] in ["transitional", "sunny", "rain"] and Forecast[3] in ["sunny"]:
            idealni = random.choice(["soft" , "medium", "hard", "medium", "hard"])
        return idealni if self.pit else None
    def player_info(self):
        if self.dnf == False:
            if safety_car == True:
                print(random.choice(["Still safety car", "Still spinning slowly lap by lap."]))
                if self.wear > 60:
                    print(random.choice(["Why didn’t we pit? We’ve just thrown away the race.", "I had no grip even before the safety car!", "Come on! These tyres are dead — what are we doing?!", "Are we sure about staying out? Tyres are cooked."]))
            print(f"\n🚗 Your car {self.name}")
            rank = [a.name for a in cars if not a.dnf]  # Move this line here            
            if driver_1 == self.name:
                position = rank.index(driver_1) + 1 if driver_1 in rank else count_cars
                print(f"Driver 1 - {player.name}")
            else:
                position = rank.index(driver_2) + 1 if driver_2 in rank else  count_cars
                print(f"Driver 2 - {player_2.name}")
            print(f"\n📊 Rank: {position}. from {len(rank)}")
            fake_o = int(self.wear) - random.uniform(-4, 4)
            fake_o = int(fake_o)
            if fake_o < 0:
                fake_o = 0
            print(f"🛞  Pneu: {self.pneu} | Tyre wear: {fake_o}%")
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
                car_pred = cars[index - 1]
                difference = self.time - car_pred.time
                print(f"Delta před: {round(difference, 3)}s ({car_pred.team.nazev})")
            if self.wear >= 70:
                print(random.choice(["The tyres are pretty done now.", "I don´t know what are you doing there, but I am boxing. Or at least I wish.", "The tyres are ***!", "Please, take me out from this hell." "Please box, please."]))
        return 
    def drss(self):
        for i in range(1, len(cars)):  # Začínáme od 1, abychom měli i-1 pro předchozí car
    # Čas aktuálního a předchozího cars
            current_time = self.time  # Čas aktuálního cars
            previous_time = cars[i-1].time  # Předpokládám, že cars mají atribut 'time'

    # Vypočítáme rozdíl mezi časy
            time_difference = current_time - previous_time

    # Pokud je rozdíl menší než 1 sekunda, aktivujeme DRS
            if time_difference < 1:
                self.drs = True
        return self.time, self.drs

    def simuluj_ai(self, training):
        if self.is_player == False:
            new_pneu = self.rozhodni_ai(tyre, lap, LAPS, Forecast)
            if new_pneu:
                self.pit_stop(new_pneu)

        self.simuluj_lap(tyre, training)
    def vhodne_pneu(self, tyre):
        if tyre in ["strong_rain", "rain"]:
                return ["wet", "inter"]
        elif tyre == "transitional":
            return ["wet", "inter", "soft", "medium", "hard"]
        else:
            return ["soft", "medium", "hard"]
    def vypocitej_points_jezdec(self, rank):
        if self.dnf == False:
            position = rank.index(self.name) + 1
            if position == 1:
                self.points += 50
            elif position == 2:
                self.points += 42
            elif position == 3:
                self.points += 36
            elif position == 4:
                self.points += 32
            elif position == 5:
                self.points += 28
            elif position == 6:
                self.points += 25
            elif position == 7:
                self.points += 22
            elif position == 8:
                self.points += 19
            elif position == 9:
                self.points += 16
            elif position == 10:
                self.points += 14
            elif position == 11:
                self.points += 12
            elif position == 12:
                self.points += 10
            elif position == 13:
                self.points += 8
            elif position == 14:
                self.points += 6
            elif position == 15:
                self.points += 5
            elif position == 16:
                self.points += 4
            elif position == 17:
                self.points += 3
            elif position == 18:
                self.points += 2
            elif position == 19:
                self.points += 1
class Team:
    def __init__(self, nazev, skill):
        self.nazev = nazev
        self.skill = skill
        self.drivers = []  # seznam instancí třídy car
        self.points = 0     # points celého týmu

    def pridej_jezdce(self, car):
        self.drivers.append(car)
        car.team = self

    def vypocitej_points(self, rank):
        for jezdec in self.drivers:
            if jezdec.name in rank:
                position = rank.index(jezdec.name) + 1
                if position == 1:
                    self.points += 50
                elif position == 2:
                    self.points += 42
                elif position == 3:
                    self.points += 36
                elif position == 4:
                    self.points += 32
                elif position == 5:
                    self.points += 	28
                elif position == 6:
                    self.points += 25
                elif position == 7:
                    self.points += 22
                elif position == 8:
                    self.points += 19
                elif position == 9:
                    self.points += 16
                elif position == 10:
                    self.points += 14
                elif position == 11:
                    self.points += 12
                elif position == 12:
                    self.points += 10
                elif position == 13:
                    self.points += 8
                elif position == 14:
                    self.points += 6
                elif position == 15:
                    self.points += 5
                elif position == 16:
                    self.points += 4
                elif position == 17:
                    self.points += 3
                elif position == 18:
                    self.points += 2
                elif position == 19:
                    self.points += 1
drivers = ["Lightning McQueen","Francesco Bernoulli","Ghost rider","Lando Norris", "Alain Prost", "Niki Lauda", "James Hunt",  "Robert Kubica","Jiří Král","Števo Eisele","Oscar Piastri", "Charles Leclerc", "Lewis Hamilton", "George Russel", "Andrea Kimi Antoneli", "Lance Stroll", "Fernando Alonso", "Mick Schumacher", "Michael Schumacher", "Sergio Perez", "Ayrton Senna", "Jaquez Villenueve", "Valterri Bottas", "Guan Zhou", "Yuki Tsunoda", "Kimi Raikonen"]
x = 0
cars = []
for driver in drivers:
    cars.append(Car(driver,random.uniform(0.9, 1)))
player = Car(driver_1, random.uniform(0.9, 1), is_player=True)
cars.append(player)

player_2 = Car(driver_2, random.uniform(0.95, 1), is_player=True)
cars.append(player_2)
teams = []
def create_team(team_player, player_1, player_2, teams, skill):
    tym = Team(team_player, skill)
    tym.pridej_jezdce(player_1)
    tym.pridej_jezdce(player_2)
    teams.append(tym)
    return tym
create_team(team_player, player, player_2, teams, random.uniform(0.85, 1))
create_team("Scuderia Python", cars[0], cars[1], teams, random.uniform(0.8, 0.9))
create_team("Racing 404",cars[2],cars[3], teams, random.uniform(0.95, 1))
create_team("Formula 1.0 racing team",cars[4],cars[5], teams, random.uniform(0.9, 1))
create_team("Microsoft PitStop Protocol racing team",cars[6],cars[7], teams, random.uniform(0.8, 1))
create_team("Intel QWERTY GP",cars[8],cars[9], teams, random.uniform(0.95, 1))
create_team("Underbyte Nvidia GP",cars[10],cars[11], teams, random.uniform(0.8, 0.85))
create_team("JavaScript Racing team",cars[12],cars[13], teams, random.uniform(0.8, 0.85))
create_team("Java motors",cars[14],cars[15], teams, random.uniform(0.8, 1))
create_team("Jawa Surenate Linux racing team",cars[16],cars[17], teams, random.uniform(0.8, 1))
create_team("AMD Assemblyte GP",cars[18],cars[19], teams, random.uniform(0.8, 1))
create_team("VS racing 22",cars[20],cars[21], teams, random.uniform(0.8, 1))
create_team("PyCharm motors",cars[22],cars[23], teams, random.uniform(0.8, 1))
create_team("Pixel motors",cars[24],cars[25], teams, random.uniform(0.8, 1))
sampionat = ["AWS Grand Prix de Espana", "AirBNB Prague GP", "eBay Skyline Turkey GP","Java airlines Monza IBM Italy GP","HP Bulgarian GP","Python circuit Bahamas", "Ostrava Apple GP", "META China Grand Prix", "Sony Varsava Grand Prix", "LG TV Grand Prix du France", "Huawei GP SPA"]
b = 1
lenght = int(input("What is the lenght of the championship: "))
hi = len(sampionat) - lenght
if hi > 0:
    for _ in range(hi):
        sampionat.pop(random.randint(0, len(sampionat)-1))
while len(names_free_drivers) > 1:
    b = 0
    for zavod in sampionat:
        lap = 0
        if zavod == "Huawei GP SPA":
            pneu = "soft"
            speed = "quick"
            TIME_S1 = 22
            TIME_S2 = 25
            TIME_S3 = 18
            LAPS = 70
        if zavod == "LG TV Grand Prix du France":
            pneu = "soft"
            speed = "quick"
            TIME_S1 = 26
            TIME_S2 = 19
            TIME_S3 = 22
            LAPS = 74
        if zavod == "Sony Varsava Grand Prix":
            pneu = "hard"
            speed = "medium"
            TIME_S1 = 35
            TIME_S2 = 18
            TIME_S3 = 24
            LAPS = 62
        if zavod == "META China Grand Prix":
            pneu = "medium"
            speed = "slow"
            TIME_S1 = 25
            TIME_S2 = 34
            TIME_S3 = 30
            LAPS = 56
        if zavod == "Ostrava Apple GP":
            pneu = "soft"
            speed = "quick"
            TIME_S1 = 20
            TIME_S2 = 26
            TIME_S3 = 18
            LAPS = 67
        if zavod == "Python circuit Bahamas":
            pneu = "hard"
            speed = "medium"
            TIME_S1 = 25
            TIME_S2 = 23
            TIME_S3 = 38
            LAPS = 72  
        if zavod == "HP Bulgarian GP":
            pneu = "medium"
            speed = "medium"
            TIME_S1 = 23
            TIME_S2 = 29
            TIME_S3 = 20
            LAPS = 60
        if zavod == "AWS Grand Prix de Espana":
            pneu = "medium"
            speed = "quick"
            TIME_S1 = 26
            TIME_S2 = 31
            TIME_S3 = 12
            LAPS = 51
        if zavod == "AirBNB Prague GP":
            pneu = "soft"
            speed = "quick"
            TIME_S1 = 20
            TIME_S2 = 33
            TIME_S3 = 40
            LAPS = 42
        if zavod == "eBay Skyline Turkey GP":
            pneu = "hard"
            speed = "slow"
            TIME_S1 = 27
            TIME_S2 = 24
            TIME_S3 = 36
            LAPS = 49
        if zavod == "Java airlines Monza IBM Italy GP":
            pneu = "soft"
            speed = "quick"
            TIME_S1 = 30
            TIME_S2 = 16
            TIME_S3 = 18
            LAPS = 70
        print(f"Current race {zavod} {b}/{len(sampionat)}")
        print(f"This track is characteristic for {pneu} pneu and {speed} pace. It has {LAPS} laps")
        strategy(LAPS, TIME_S1, TIME_S2, TIME_S3, pneu, speed)

        if pneu == "medium":
            k_wear = [1.5,5,9,4.4,8.4]
        elif pneu == "soft":
            k_wear = [2,7,12,5,9]       
        else:
            k_wear = [1,4,7,4,8]
        if speed == "medium":
            k_speed = [1,1.05,1.12,0.6,0.65]
        elif speed == "quick":
            k_speed = [1.05,1.12,1.15,0.65,0.7]
        else:
            k_speed = [0.95,1,1.05,0.55,0.6]
        PNEU_types = {
        "hard": {"wear": k_wear[0], "speed": k_speed[0]},
        "medium": {"wear": k_wear[1], "speed": k_speed[1]},
        "soft": {"wear": k_wear[2], "speed": k_speed[2]},
        "wet": {"wear": k_wear[3], "speed": k_speed[3]},
        "inter": {"wear": k_wear[4], "speed": k_speed[4]},
        }
        tyre = "sunny"
        weather_1 = generate_weather(tyre)
        weather_2 = generate_weather(weather_1)
        weather_3 = generate_weather(weather_2)
        weather_4 = generate_weather(weather_3)
        Forecast = [weather_1, weather_2, weather_3, weather_4]
        for x in Forecast:
            print (f"Weather: 🌤️ ☁️  {x}")
        for car in cars:
            car.pneu = random.choice(["hard", "medium"])
        player.pneu = input("Choose pneu for driver 2: [hard / medium / soft / wet / inter]\n")
        while player.pneu not in PNEU_types:
            player.pneu = input("Incorrect choice. Choose pneu for driver 2: [hard / medium / soft / wet / inter]\n")
            if player.pneu == "exit":
                continue
        player_2.pneu = input("Choose pneu for driver 2: [hard / medium / soft / wet / inter]\n")
        while player_2.pneu not in PNEU_types:
            player_2.pneu = input("Incorrect choice. Choose pneu for driver 2: [hard / medium / soft / wet / inter]\n")
            if player.pneu == "exit":
                continue
        simulation = []
        #Tréninky
        training = input("Action: Chceš trénink na výdrž pneu [1], speed [2] nebo kvalikaci [3]: ")
        #Kvalifikace
        for car in cars:
            sim_time = TIME_S1 * random.uniform(0.9, 1.1) + TIME_S2 * random.uniform(0.9, 1.1) + TIME_S3 * random.uniform(0.9, 1.1)
            if car.is_player and training == "3":
                sim_time = sim_time/1.5 
            simulation.append((car, sim_time))
        simulation.sort(key=lambda x: x[1])
        for i, (car, sim_time) in enumerate(simulation):
            penalizovany_time =  1 * i
            car.time += penalizovany_time
        ######################################################################################################################################################################
        while lap <= LAPS:
            if lap == LAPS:
                print("Last lap. Push push.")
            info()
            for car in cars:
            # sem patří tvůj kód

                if tyre == "sunny":
                    if random.randint(1, 5000) == 1:
                        if lap >= 3:
                            car.dnf = True
                            safety_car = True
                            laps_rem = random.randint(3,6)
                            print(f"{car.name} obdrželo DNF")
                            print(random.choice([
                        "Radio: Crash ahead, safety car is out!",
                        "Radio: We’ve got yellow flags – full course yellow!",
                        "Radio: Big crash, bring the delta in check.",
                        "Radio: Watch the debris – SC deployed!"
                    ]))
                else:
                    if random.randint(1, 1000) == 1:
                        if lap >= 3:
                            car.dnf = True
                            safety_car = True
                            laps_rem = random.randint(3,6)
                            print(f"{car.name} obdrželo DNF")
                            print(random.choice([
                        "Radio: Crash ahead, safety car is out!",
                        "Radio: We’ve got yellow flags – full course yellow!",
                        "Radio: Big crash, bring the delta in check.",
                        "Radio: Watch the debris – SC deployed!"
                    ]))
            if safety_car == True:
                laps_rem -=1
            if laps_rem == 0:
                safety_car = False
            cars.sort(key=lambda x: (x.dnf, x.time))
            for car in cars:
            # sem patří tvůj kód

                if car.is_player:
                    car.player_info()
                    #position = rank.index(driver_1) + 1 if driver_1 in rank else count_cars
                    #d_2 = rank.index(driver_2) + 1 if driver_2 in rank else  count_cars
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
                        chance_predjeti = max(0.1, 1.5 - difference) * 0.4  # např. až 60% šance
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

            #position = rank.index(driver_1) + 1 if driver_1 in rank else "DNF"
            print(f"\n📊 Rank {driver_1}: {position}. místo z {len(rank)}")
            #position_2 = rank.index(driver_2) + 1 if driver_2 in rank else "DNF"
            print(f"\n📊 Rank {driver_2}: {position_2}. místo z {len(rank)}")
            drivers_table()
            for car in cars:
                car.simuluj_ai(training)
            boxy_po_teamu = {}
            for a in cars:
                if not a.is_player and a.pit:  # pokud AI jezdec plánuje pit
                    team = a.team
                    if team not in boxy_po_teamu:
                        boxy_po_teamu[team] = 0
                    boxy_po_teamu[team] += 1

            for team, pocet in boxy_po_teamu.items():
                if pocet >= 2:
                    print(f"{team.nazev} jde do double stacku.")
                    for a in cars:
                        if a.team == team and a.pit:
                            position = rank.index(a) + 1 if a in rank else count_cars
                            a.time += 50
            boxy_po_teamu.clear()
            cars.sort(key=lambda x: (x.dnf, x.time))
            rank = [a for a in cars if not a.dnf]  # Move this line here
            for a in cars:
                if a in rank:  # Pokud je car v seznamu rank
                    position = rank.index(a) + 1  # position v seznamu (index + 1)
                else:
                    position = count_cars  # Pokud není car v seznamu, nastaví se na count_cars
                a.position.append(position)  # Přidání position do seznamu pozic cars

            # posun počasí
            tyre = Forecast.pop(0)
            weather_1 = Forecast[0]
            weather_2 = Forecast[1]
            weather_3 = Forecast[2]
            Forecast.append(generate_weather(weather_3))
            weather_4 = Forecast[3]
            lap += 1
        print("\n🏁 END OF THE RACE!!")
        b +=1
        time_laps.sort()
        print(f"{time_laps[0][1]} ({time_laps[0][2].nazev}) has fastest lap: {round(time_laps[0][0], 3)}")
        for a in cars:
            a.skills -= 0.01
        sector_1 = min(time_laps, key=lambda x: x[3])
        sector_2 = min(time_laps, key=lambda x: x[4])
        sector_3 = min(time_laps, key=lambda x: x[5])

        print(f"{sector_1[1]} ({sector_1[2].nazev}) has fastest sector 1 {round(sector_1[3], 3)}")
        print(f"{sector_2[1]} ({sector_2[2].nazev}) has fastest sector 2 {round(sector_2[4], 3)}")
        print(f"{sector_3[1]} ({sector_3[2].nazev}) has fastest sector 3 {round(sector_3[5], 3)}")

        time_laps[0][2].points += 2
        for d in range(len(time_laps)):
            if time_laps[d][1] == player.name:
                print(f"{time_laps[d][1]} ({time_laps[d][2].nazev}) has fastest lap {round(time_laps[d][0], 3)}, sector 1 {round(time_laps[d][3], 3)}, sector 2 {round(time_laps[d][4], 3)}, sector 3 {round(time_laps[d][5], 3)}")
                break
        for d in range(len(time_laps)):
            if time_laps[d][1] == player_2.name:
                print(f"{time_laps[d][1]} ({time_laps[d][2].nazev}) has fastest lap {round(time_laps[d][0], 3)}, sector 1 {round(time_laps[d][3], 3)}, sector 2 {round(time_laps[d][4], 3)}, sector 3 {round(time_laps[d][5], 3)}")
                break
        #time.sleep(6)
        #
        ## Uložení výsledků do CSV
        #with open("vysledky_zavodu.csv", "w", newline="", encoding="utf-8") as file:
        #    writer = csv.writer(file)
        #    writer.writerow(["Rank", "Jezdec", "Čas (min)", "Number of pit stops", "DNF", "Stinty"])
        #    for i, a in enumerate(cars, 1):
        #        time = round(a.time / 60, 2) if not a.dnf else "DNF"
        #        stint_popis = "; ".join(
        #            [f"{round(start/60, 1)}–{round((start+doba)/60, 1)}min: {typ}" for start, doba, typ in a.stinty]
        #        )
        #        writer.writerow([i, a.name, time, a.box, a.dnf, stint_popis])


        # Ujistíme se, že rank je stále list jezdců bez DNF
        rank = [a.name for a in cars if not a.dnf]
        for driver in cars:
            driver.vypocitej_points_jezdec(rank)
        for team in teams:
            team.vypocitej_points(rank)
        points = sorted(teams, key=lambda x: (x.points))
        # Bezpečný výpočet pozic
        position_1 = rank.index(driver_1) + 1 if driver_1 in rank else "DNF"
        position_2 = rank.index(driver_2) + 1 if driver_2 in rank else "DNF"
        print(f"\n🏁 Final position:")
        print(f"{driver_1}: {position_1}. place")
        print(f"{driver_2}: {position_2}. place")
        #time.sleep(4)
        # Výsledková listina
        cars.sort(key=lambda x: (x.dnf, x.time))
        for i, a in enumerate(cars, 1):
            stav = "DNF" if a.dnf else f"{round(a.time, 2)}s"
            print(f"{i}. {a.name} ({a.team.nazev}) {a.points} points")
        teams.sort(key=lambda team: team.points, reverse=True)
        #time.sleep(8)
        for i, team in enumerate(teams,1):
            print (f"{i}.{team.nazev} {team.points} points")
        #time.sleep(8)
        # 📊 Grafické znázornění výsledků race
        jmena = [a.name for a in cars]
        timey = [a.time/60 if not a.dnf else None for a in cars]
        # colours podle pneu
        colours = []
        colours_graphs()
        # Zaznamenání posledního stintu pro každé car
        for a in cars:
            if not a.dnf:
                a.stinty.append((a.last_stint_start, a.time - a.last_stint_start, a.pneu))
        # Zobrazení grafu
        plt.figure(figsize=(12, 6))
        plt.barh(jmena[::-1], [c if c is not None else 0 for c in timey][::-1], color=colours[::-1])
        plt.xlabel("Time (min)")
        plt.ylabel("drivers")
        plt.title("🏁 Results race")
        plt.tight_layout()
        plt.show()
        plt.figure(figsize=(10, 6))
        for a in cars:
            plt.plot(range(1, len(a.position) + 1), a.position, label=a.name)

        plt.gca().invert_yaxis()  # protože 1. místo je nejlepší
        plt.xlabel("Lap")
        plt.ylabel("Position")
        plt.title("Position meanwhile racing")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        plt.figure(figsize=(10, 6))
        players = [player, player_2]
        for a in players:
            plt.plot(range(len(a.position)), a.position, label=a.name)

        plt.gca().invert_yaxis()  # protože 1. místo je nejlepší
        plt.xlabel("Lap")
        plt.ylabel("Position")
        plt.title("Position meanwhile racing")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        reset_race()
    print("\n🏁 Final drivers sorting:")
    #best, worst = simulate_season_MMR2(hi)
    for d in list_drivers_mmr2:
        d.skill -= 0.05
    nahodne_name = random.choice(names_free_drivers)
    names_free_drivers.pop(names_free_drivers.index(nahodne_name))
    worst.nazev, worst.skill = nahodne_name, random.uniform(0.95,1.05)
    cars.sort(key=lambda x: x.points, reverse=True)
    for i, a in enumerate(cars, 1):
        print(f"{i}. {a.name} – {a.points} points ({a.team.nazev})")
        if i == len(cars):
            new = best.name
            skill = best.skill
            print(f"Breaking!!!\n{new} changes {a.name} ({a.team.nazev})\nBreaking!!!")
            best.name, best.skill = a.name, a.skills
            a.name, a.skills = new, skill
    print("\n🏆 Final team sorting:")
    teams.sort(key=lambda t: t.points, reverse=True)
    for i, t in enumerate(teams, 1):
        if i == 1:  
            t.skill -= 0.1
            img = mpimg.imread(f'{t.nazev}.png')
            plt.imshow(img)
            plt.axis('off')  # Optional: hides axis for image display
            plt.show()
        print(f"{i}. {t.nazev} – {t.points} points")
        if i == len(teams):
            t.skill +=0.1
