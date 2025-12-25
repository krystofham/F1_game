import random
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

def colours_graphs(cars, colours):
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


def reset_race(climax, cars):
    global lap, time_laps, SAFETY_CAR, LAPS_REMAINING, forecast, weather
    lap = 0
    time_laps = []
    SAFETY_CAR = False
    LAPS_REMAINING = 0
    weather = "sunny"
    forecast = [generate_weather(weather, climax)]
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

drivers = ["Alex Storme","Matteo Blaze","Hiro Tanaka","Lukas Rennhardt","Diego Ventura","Aiden Falk","Pierre Lucien","Nilapsai Vetrovski","Riku Yamashita","Carlos Navarro","Johan Reißer","Theo Hartman","Enzo DaCosta","Sebastian Krell","Marco Falcone","Ivan Vasiliev","Tyler Quinn","Jae-Min Han","Felipe Marquez","Elias Northgate","Arjun Desai","Tomás Moreira","Leo Krüger","Mikhail Antonov","Julian Stroud","Renzo Morandi"]
championship = ["AWS Grand Prix de Espana", "AirBNB Prague GP", "eBay Skyline Turkey GP","Java airlines Monza IBM Italy GP","HP Bulgarian GP","Python circuit Bahamas", "Ostrava Apple GP", "META China Grand Prix", "Sony Varsava Grand Prix", "LG TV Grand Prix du France", "Huawei GP SPA"]
