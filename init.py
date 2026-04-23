import random
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from printing_info import *
from simulating_sectors import *
from strategy import *
from mmr2 import *
from track import *
from team import *
from car import *
from weather import *
from engine import *
from plot import *
from get_data import *
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
SAFETY_CAR = False
WEATHER_TYPES = ["sunny", "transitional", "rain", "heavy rain"]
pneu_colours = {
    "hard": "gray",
    "medium": "yellow",
    "soft": "red",
    "inter": "green",
    "wet": "deepskyblue"
}


drivers = ["Alex Storme","Matteo Blaze","Hiro Tanaka","Lukas Rennhardt","Diego Ventura","Aiden Falk","Pierre Lucien","Nilapsai Vetrovski","Riku Yamashita","Carlos Navarro","Johan Reißer","Theo Hartman","Enzo DaCosta","Sebastian Krell","Marco Falcone","Ivan Vasiliev","Tyler Quinn","Jae-Min Han","Felipe Marquez","Elias Northgate","Arjun Desai","Tomás Moreira","Leo Krüger","Mikhail Antonov","Julian Stroud","Renzo Morandi"]
championship = ["AWS Grand Prix de Espana", "AirBNB Prague GP", "eBay Skyline Turkey GP","Java airlines Monza IBM Italy GP","HP Bulgarian GP","Python circuit Bahamas", "Ostrava Apple GP", "META China Grand Prix", "Sony Varsava Grand Prix", "LG TV Grand Prix du France", "Huawei GP SPA"]
cars = []
for driver in drivers:
    cars.append(Car(driver,random.uniform(5, 6)))
player = Car(DRIVER_1, random.uniform(5, 6), is_player=True)
cars.append(player)
player_2 = Car(DRIVER_2, random.uniform(5, 6), is_player=True)
cars.append(player_2)

create_team(TEAM_PLAYER,                                player, player_2, teams,    random.uniform(5,   6))
create_team("Scuderia Python",                          cars[0], cars[1], teams,    random.uniform(4,   6.9))
create_team("Racing 404",                               cars[2],cars[3], teams,     random.uniform(4.5, 6))
create_team("Formula 1.0 racing team",                  cars[4],cars[5], teams,     random.uniform(4,   6))
create_team("Microsoft PitStop Protocol racing team",   cars[6],cars[7], teams,     random.uniform(4,   6))
create_team("Intel QWERTY GP",                          cars[8],cars[9], teams,     random.uniform(4.5, 6))
create_team("Underbyte Nvidia GP",                      cars[10],cars[11], teams,   random.uniform(4,   6.85))
create_team("JavaScript Racing team",                   cars[12],cars[13], teams,   random.uniform(4,   6.85))
create_team("Java motors",                              cars[14],cars[15], teams,   random.uniform(4,   6))
create_team("Jawa Surenate Linux racing team",          cars[16],cars[17], teams,   random.uniform(4,   6))
create_team("AMD Assemblyte GP",                        cars[18],cars[19], teams,   random.uniform(4,   6))
create_team("VS racing 22",                             cars[20],cars[21], teams,   random.uniform(4,   6))
create_team("PyCharm motors",                           cars[22],cars[23], teams,   random.uniform(4,   6))
create_team("Pixel motors",                             cars[24],cars[25], teams,   random.uniform(4,   6))
lenght = 0
