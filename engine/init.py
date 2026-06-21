import random
import json
import os
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
#from plot import *
from get_data import *
from log import clear_log, ilog, dlog, elog, wlog
# clear_log()
ilog(fn="init", msg="init.py run started")
_BASE_DIR = os.path.dirname(__file__)
_CONFIG_DIR = os.path.abspath(os.path.join(_BASE_DIR, "..", "config"))
ilog(fn="init", msg="directories resolved", base_dir=_BASE_DIR, config_dir=_CONFIG_DIR)

try:
    with open(os.path.join(_CONFIG_DIR, "drivers.json"), encoding="utf-8") as f:
        _drivers_cfg = json.load(f)
    with open(os.path.join(_CONFIG_DIR, "teams.json"), encoding="utf-8") as f:
        _teams_cfg = json.load(f)
except OSError as e:
    elog(fn="init", msg="config json read failed", error=str(e), config_dir=_CONFIG_DIR)
    raise
except json.JSONDecodeError as e:
    elog(fn="init", msg="config json malformed", error=str(e), config_dir=_CONFIG_DIR)
    raise

dlog(fn="init", msg="config loaded",
     driver_count=len(_drivers_cfg.get("drivers", [])),
     team_count=len(_teams_cfg.get("teams", [])))

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

playersname = _drivers_cfg["player_drivers"]

player   = Car(playersname[0], random.uniform(5, 6), is_player=True)
player_2 = Car(playersname[1], random.uniform(5, 6), is_player=True)
cars.append(player)
cars.append(player_2)
dlog(fn="init", msg="cars created", cars=[c.to_log() for c in cars])
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
ilog(fn="init", msg="init.py run finished", teams=[t.to_log() for t in teams], car_count=len(cars))
