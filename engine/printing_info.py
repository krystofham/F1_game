import json

# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
import os
import random

from load_data_json import *
from log import dlog, elog, ilog, wlog
from paths import img_dir, user_input_dir
from strategy import strategy
from weather import generate_weather


def pit_player(
    player,
    player_2,
    LAPS,
    lap,
    TIME_S1,
    TIME_S2,
    TIME_S3,
    tyre,
    speed,
    PNEU_types,
    SAFETY_CAR,
    climax,
):
    data = load_data("lap_user_data")
    default_action = {"action": "1", "new_tyre": "medium"}
    d1_data = {
        **default_action,
        **(data.get(player.name) or data.get("driver_1") or {}),
    }
    d2_data = {
        **default_action,
        **(data.get(player_2.name) or data.get("driver_2") or {}),
    }
    pick = d1_data["action"].strip().lower()
    pick_2 = d2_data["action"].strip().lower()

    dlog(
        fn="pit_player",
        msg="lap user data loaded",
        player_1=player.name,
        action_1=pick,
        tyre_1=d1_data.get("new_tyre"),
        player_2=player_2.name,
        action_2=pick_2,
        tyre_2=d2_data.get("new_tyre"),
    )

    if not player.dnf:
        if pick == "tyrestav":
            player.time += 2
        elif pick == "tyresafe":
            player.wear -= 1
            player.time += 3
        elif pick == "2":
            new = d1_data["new_tyre"].strip().lower()
            if new not in PNEU_types:
                elog(
                    fn="pit_player",
                    msg="invalid tyre for driver 1",
                    driver=player.name,
                    tyre=new,
                )
                raise ValueError(f"Driver 1: invalid tyre '{new}'")
            strategy(LAPS - lap, TIME_S1, TIME_S2, TIME_S3, tyre, speed, climax)
            ilog(
                fn="pit_player",
                msg="driver 1 pit stop",
                driver=player.name,
                new_tyre=new,
                lap=lap,
            )
            player.pit_stop(new, SAFETY_CAR)

    if not player_2.dnf:
        if pick_2 == "tyrestav":
            player_2.time += 2
        elif pick_2 == "tyresafe":
            player_2.wear -= 1
            player_2.time += 3
        elif pick_2 == "2":
            new = d2_data["new_tyre"].strip().lower()
            if new not in PNEU_types:
                elog(
                    fn="pit_player",
                    msg="invalid tyre for driver 2",
                    driver=player_2.name,
                    tyre=new,
                )
                raise ValueError(f"Driver 2: invalid tyre '{new}'")
            strategy(LAPS - lap, TIME_S1, TIME_S2, TIME_S3, tyre, speed, climax)
            ilog(
                fn="pit_player",
                msg="driver 2 pit stop",
                driver=player_2.name,
                new_tyre=new,
                lap=lap,
            )
            player_2.pit_stop(new, SAFETY_CAR)

    if not (player.dnf or player_2.dnf):
        if pick == "2" and pick_2 == "2":
            player.time += 3
            player_2.time += 3
    # Reset po přečtení — aby se pitstop neopakoval
    try:
        reset_path = os.path.join(user_input_dir(), "lap_user_data.json")
        with open(reset_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    player.name: {"action": "1", "new_tyre": "medium"},
                    player_2.name: {"action": "1", "new_tyre": "medium"},
                    "commands": [],
                },
                f,
                indent=2,
            )
    except Exception as e:
        wlog(fn="pit_player", msg="lap_user_data reset failed", error=str(e))
    else:
        dlog(
            fn="pit_player",
            msg="lap_user_data reset to defaults",
            player_1=player.name,
            player_2=player_2.name,
        )

    return player, player_2


def post_race_info(time_laps, player, player_2, cars, teams, COUNT_CARS):
    if not time_laps:
        elog(fn="post_race_info", msg="no lap times recorded — results incomplete")
    else:
        ilog(
            fn="post_race_info",
            msg="post race processing started",
            time_laps_count=len(time_laps),
            fastest_lap_driver=time_laps[0][1] if time_laps else None,
        )
        time_laps.sort()

        sector_1 = min(time_laps, key=lambda x: x[3])
        sector_2 = min(time_laps, key=lambda x: x[4])
        sector_3 = min(time_laps, key=lambda x: x[5])
        for x in teams:
            if x.name == sector_1[2]:
                x.points += 2

    RANK = [a.name for a in cars if not a.dnf]
    for driver in cars:
        driver.vypocitej_points_jezdec(RANK)
        driver.ratings -= 0.01
    for team in teams:
        team.vypocitej_points(RANK, COUNT_CARS)

    return teams, cars, time_laps