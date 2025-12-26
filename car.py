import random
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

    def efectivity_pneu(self, weather, PNEU_types):
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


    def simuluj_lap(self, weather, training, wettiness, TIME_S1, TIME_S2, TIME_S3, speed_bonus, time_laps, PNEU_types):
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

        speed = self.efectivity_pneu(weather, PNEU_types)
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

    def choose_ai(self, laps, max_laps, forecast, LAPS, lap, k_wear):
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
    def player_info(self, cars, DRIVER_1, COUNT_CARS, player, DRIVER_2,player_2):
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
    def drss(self, car_in_front):
        if car_in_front.time - self.time < 1:
            self.drs = True
        return self.drs

    def simuluj_ai(self, training, WETTINESS, lap, LAPS, forecast, weather, laps, max_laps, k_wear, wettiness, TIME_S1, TIME_S2, TIME_S3, speed_bonus, time_laps, PNEU_types):
        if self.is_player is False:
            new_pneu = self.choose_ai(laps, max_laps, forecast, LAPS, lap, k_wear)
            if new_pneu:
                self.pit_stop(new_pneu)
        self.simuluj_lap(weather, training, wettiness, TIME_S1, TIME_S2, TIME_S3, speed_bonus, time_laps, PNEU_types)
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
