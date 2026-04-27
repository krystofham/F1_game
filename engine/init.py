import random
import json
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from printing_info import *
from simulating_sectors import *
from strategy import *
from mmr2 import *
from track import *
from team import *
from saving import *
from car import *
from weather import *
from engine import *
from plot import *
from get_data import *

_BASE_DIR = os.path.dirname(__file__)
_CONFIG_DIR = os.path.abspath(os.path.join(_BASE_DIR, "..", "config"))
with open(os.path.join(_CONFIG_DIR, "drivers.json"), encoding="utf-8") as f:
    _drivers_cfg = json.load(f)

with open(os.path.join(_CONFIG_DIR, "teams.json"), encoding="utf-8") as f:
    _teams_cfg = json.load(f)

RANK            = 0
WETTINESS       = 0
TIME_S1         = 15
TIME_S2         = 23
TIME_S3         = 22
time_laps       = []
LAPS            = 0
LAPS_REMAINING  = 0
SAFETY_CAR      = False
length          = 0

DRIVER_1        = _drivers_cfg["player_drivers"]["driver_1"]
DRIVER_2        = _drivers_cfg["player_drivers"]["driver_2"]
TEAM_PLAYER     = _teams_cfg["player_team"]["name"]
COUNT_CARS      = 28

WEATHER_TYPES   = ["sunny", "transitional", "rain", "heavy rain"]

pneu_colours = {
    "hard":   "gray",
    "medium": "yellow",
    "soft":   "red",
    "inter":  "green",
    "wet":    "deepskyblue",
}

drivers             = _drivers_cfg["drivers"]
names_free_drivers  = _drivers_cfg["free_drivers"]

championship = [
    "AWS Grand Prix de Espana",
    "AirBNB Prague GP",
    "eBay Skyline Turkey GP",
    "Java airlines Monza IBM Italy GP",
    "HP Bulgarian GP",
    "Python circuit Bahamas",
    "Ostrava Apple GP",
    "META China Grand Prix",
    "Sony Varsava Grand Prix",
    "LG TV Grand Prix du France",
    "Huawei GP SPA",
]

cars = [Car(driver, random.uniform(5, 6)) for driver in drivers]

player   = Car(DRIVER_1, random.uniform(5, 6), is_player=True)
player_2 = Car(DRIVER_2, random.uniform(5, 6), is_player=True)
cars.append(player)
cars.append(player_2)

_pt = _teams_cfg["player_team"]
create_team(
    _pt["name"],
    player,
    player_2,
    teams,
    random.uniform(_pt["performance_min"], _pt["performance_max"]),
)

for _t in _teams_cfg["teams"]:
    i1, i2 = _t["car_indices"]
    create_team(
        _t["name"],
        cars[i1],
        cars[i2],
        teams,
        random.uniform(_t["performance_min"], _t["performance_max"]),
    )