import random
from log import dlog, elog, ilog, wlog
import os, json as _json
_fuel_path = os.path.join(os.path.dirname(__file__), "user_input/lap_user_data.json")

class Car:
    def __init__(self, name, rating, is_player=False):
        self.name = name
        self.box = 0
        self.stints = []  
        self.position = []
        self.last_stint_start = 0 
        self.is_player = is_player
        self.pneu = random.choice(["medium", "hard"])
        self.wear = 0.0
        self.safety_car_probability = 0
        self.ratings = rating
        self.time = 0.0
        self.points = 0
        self.drs = False
        self.team = None
        self.dnf = False
        self.destroy = False
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


    def simuluj_lap(self, weather, training, wettiness, TIME_S1, TIME_S2, TIME_S3, speed_bonus, time_laps, PNEU_types, SAFETY_CAR, LAPS_REMAINING):
        if not SAFETY_CAR:
            LAPS_REMAINING = 0

        # Pace mode
        if self.is_player:
            try:
                with open(_fuel_path, encoding="utf-8") as _f:
                    _ud = _json.load(_f)
                pace = _ud.get(self.name, {}).get("pace", "normal")
            except Exception:
                pace = "normal"
        else:
            pace = "normal"

        PACE_MODS = {
            "slower": {"time": +1.5, "wear": 0.7},
            "normal": {"time":  0.0, "wear": 1.0},
            "faster": {"time": -1.5, "wear": 1.4},
        }
        mod = PACE_MODS.get(pace, PACE_MODS["normal"])

        if self.wear >= 100 and not self.destroy:
            self.dnf = True
            self.destroy = True
            SAFETY_CAR = True
            LAPS_REMAINING = random.randint(3, 6)
            self.puncture = True

        if self.puncture and not self.destroy:
            self.destroy = True
            SAFETY_CAR = True
            LAPS_REMAINING = random.randint(3, 6)

        if self.wear > 80 and random.random() < 0.55 and not self.destroy:
            self.puncture = True
            self.dnf = True
            self.destroy = True
            SAFETY_CAR = True
            LAPS_REMAINING = random.randint(3, 6)

        speed = self.efectivity_pneu(weather, PNEU_types)
        s1 = (TIME_S1 * random.uniform(0.99, 1.01) + self.ratings/2 + self.team.rating/2) / speed
        s2 = (TIME_S2 * random.uniform(0.99, 1.01) + self.ratings/2 + self.team.rating/2) / speed
        s3 = (TIME_S3 * random.uniform(0.99, 1.01) + self.ratings/2 + self.team.rating/2) / speed

        if SAFETY_CAR:
            s1 *= 2.5; s2 *= 2.5; s3 *= 2.5
        if self.drs:
            s1 -= random.uniform(0.5, 0.7)
            s2 -= random.uniform(0.5, 0.7)
            s3 -= random.uniform(0.5, 0.7)
        if training == "1":
            s1 -= random.uniform(0.1, 0.3)
            s2 -= random.uniform(0.1, 0.3)
            s3 -= random.uniform(0.1, 0.3)
        if speed_bonus:
            s1 -= random.uniform(0.3, 0.5)
            s2 -= random.uniform(0.3, 0.5)
            s3 -= random.uniform(0.3, 0.5)
        if wettiness < 30 and self.pneu not in ["soft", "medium", "hard"]:
            s1 += wettiness/2; s2 += wettiness/2; s3 += wettiness/2
        if wettiness > 55 and self.pneu not in ["wet", "inter"]:
            s1 += wettiness/2; s2 += wettiness/2; s3 += wettiness/2

        lap_time = s1 + s2 + s3 + mod["time"]

        if self.is_player:
            dlog(fn="simuluj_lap", msg="player lap completed", name=self.name,
                lap_time=round(lap_time, 3), pneu=self.pneu, wear=round(self.wear, 2), pace=pace)

        time_laps.append((lap_time, self.name, self.team.name, s1, s2, s3))
        self.time += self.wear/5 + lap_time
        self.wear += PNEU_types[self.pneu]["wear"] * random.uniform(0.9, 1.1) * mod["wear"]

        return SAFETY_CAR, LAPS_REMAINING





    def pit_stop(self, new_pneu, SAFETY_CAR):
        dlog(fn="pit_stop", msg="pit stop executed", name=self.name, old_pneu=self.pneu,
             new_pneu=new_pneu, safety_car=SAFETY_CAR, is_player=self.is_player)
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

    def choose_ai(self, laps, max_laps, forecast, LAPS, lap, k_wear, SAFETY_CAR):
        if self.dnf:
            return None
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
    def player_info(self, cars, COUNT_CARS, player, player_2, SAFETY_CAR):
        if self.dnf is False:
            if SAFETY_CAR is True:
                #print(random.choice(["Still safety car", "Still spinning slowly lap by lap."]))
                if self.wear > 60:
                    pass
                    #print(random.choice(["Why didn’t we pit? We’ve just thrown away the race.", "I had no grip even before the safety car!", "Come on! These weathers are dead — what are we doing?!", "Are we sure about staying out? Tyres are cooked."]))
            #print(f"\n🚗 Your car {self.name}")
                
            if self.drs:
                pass
                #print("DRS active")
            RANK = [a.name for a in cars if not a.dnf]     
            if player.name == self.name:
                position = RANK.index(player.name) + 1 if player.name in RANK else COUNT_CARS
                #print(f"Driver 1 - {player.name}")
            else:
                position = RANK.index(player_2.name) + 1 if player_2.name in RANK else  COUNT_CARS
                #print(f"Driver 2 - {player_2.name}")
            #print(f"\n📊 Position: {position}. z {len(RANK)}")
            fake_o = int((self.wear) - random.uniform(-4, 4))
            if fake_o < 0:
                fake_o = 0
            #print(f"🛞  Pneu: {self.pneu} | Wear: {fake_o}%")
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
                pred_team = car_pred.team.name if car_pred.team else "?"
                za_team = car_za.team.name if car_za.team else "?"
                #print(f"Delta in front: {round(difference, 3)}s ({pred_team})| Delta behind: {round(difference_2, 3)}s ({za_team})")
            elif index == 0:
                car_za = cars[index + 1]
                difference_2 = car_za.time - self.time
                za_team = car_za.team.name if car_za.team else "?"
                #print(f"Delta behind: {round(difference_2, 3)}s ({za_team})")
            else:
                car_pred = cars[-2]
                difference =  car_pred.time- self.time
                pred_team = car_pred.team.name if car_pred.team else "?"
                #print(f"Delta in front: {round(difference, 3)}s ({pred_team})")
            if self.wear >= 70:
                pass
                #print(random.choice(["The tyres are pretty done now.", "I don´t know what are you doing there, but I am boxing. Or at least I wish.", "The tyres are ***!", "Please, take me out from this hell." "Please box, please."]))
        return None
    def drss(self, car_in_front):
        if abs(car_in_front.time - self.time) < 1:
            dlog(fn="drss", msg="DRS activated", name=self.name,
                 delta=round(abs(car_in_front.time - self.time), 3),
                 my_time=round(self.time, 3), front_time=round(car_in_front.time, 3))
            #print("difference is:", abs(car_in_front.time - self.time), "which is lower than 1")
            #print("My time is:", self.time)
            #print("His time is", car_in_front.time)
            self.drs = True
        else:
            self.drs = False
        return self.drs

    def simuluj_ai(self, training, WETTINESS, lap, LAPS, forecast, weather, laps, max_laps, k_wear, wettiness, TIME_S1, TIME_S2, TIME_S3, speed_bonus, time_laps, PNEU_types, SAFETY_CAR, LAPS_REMAINING):
        if self.is_player is False:
            new_pneu = self.choose_ai(laps, max_laps, forecast, LAPS, lap, k_wear, SAFETY_CAR)
            if new_pneu:
                dlog(fn="simuluj_ai", msg="AI pit decision", name=self.name, new_pneu=new_pneu,
                     wear=round(self.wear, 2), lap=laps)
                self.pit_stop(new_pneu, SAFETY_CAR)
        SAFETY_CAR, LAPS_REMAINING = self.simuluj_lap(weather, training, wettiness, TIME_S1, TIME_S2, TIME_S3, speed_bonus, time_laps, PNEU_types, SAFETY_CAR, LAPS_REMAINING)
        return SAFETY_CAR, LAPS_REMAINING
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
            dict_points = {
                1: 50,
                2: 45,
                3: 40,
                4: 35,
                5: 30,
                6: 25,
                7: 22,
                8: 20,
                9: 18,
                10: 15,
                11: 12,
                12: 10,
                13: 9,
                14: 8,
                15: 7,
                16: 6,
                17: 5,
                18: 4,
                19: 3,
                20: 2,
                21: 1,
                22: 1,
                23: 1
            }
            position = RANK.index(self.name) + 1
            for x in range(1, 24):
                if position == x:
                    gained = dict_points[x]
                    self.points += gained
                    if self.is_player:
                        ilog(fn="vypocitej_points_jezdec", msg="player points awarded",
                             name=self.name, position=position, gained=gained, total=self.points)
    def to_log(self) -> dict:
        return {
            "name":      self.name,
            "team":      self.team.name if self.team else None,
            "pneu":      self.pneu,
            "wear":      round(self.wear, 3),
            "points":    self.points,
            "dnf":       self.dnf,
            "is_player": self.is_player,
        }