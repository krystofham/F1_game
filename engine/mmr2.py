import random
import json
from log import ilog

drivers_mmr2 = [
    "Noah Blake",
    "Felipe Sandoval",
    "Luca Moretti",
    "Brian Chen",
    "Adam Kerdöl",
    "Pierre Gauthier",
    "Viktor Orlov",
    "Daisuke Tanaka",
    "Elias Müller",
    "Jordan Evans",
    "Diego Ramirez",
    "Anton Petrov",
    "Kenji Nakamura",
    "Nicolas Dubois",
    "Thomas Fischer",
    "Miguel Lopéz",
    "Alexei Solapov",
    "Ethan Zhang",
    "Leo Harrington",
    "Marco Silva",
]


class DummyTeam:
    def __init__(self):
        self.name = "MMR2"
        self.drivers = []
        self.rating = 0
        self.points = 0


class Drivermmr2:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
        self.ratings = rating
        self.time = 0.0
        self.team = DummyTeam()
        self.is_player = False
        self.points = 0
        self.dnf = False
        self.wear = 0.0
        self.tyre = "medium"
        self.box = 0
        self.position = []
        self.stints = []
        self.drs = False
        self.pit = False
        self.destroy = False
        self.puncture = False
        self.safety_car_probability = 0
        self.last_stint_start = 0


def simulate_season_mmr2(drivers):
    ilog(
        fn="simulate_season_mmr2",
        msg="MMR2 season simulation started",
        driver_count=len(drivers),
    )
    for driver in drivers:
        driver.time = 0.0
    for lap in range(50 * 12):
        for driver in drivers:
            driver.time += driver.rating * random.uniform(0.98, 1.02)
    mmr2_sorted = sorted(drivers, key=lambda x: x.time)
    best, worst = mmr2_sorted[0], mmr2_sorted[-1]
    ilog(
        fn="simulate_season_mmr2",
        msg="MMR2 season simulation finished",
        best=best.name,
        best_time=round(best.time, 3),
        worst=worst.name,
        worst_time=round(worst.time, 3),
    )
    return best, worst

def save_mmr2_drivers(drivers, filename="mmr2_drivers.json"):
    data = []

    for driver in drivers:
        data.append({
            "name": driver.name,
            "rating": driver.rating,
            "ratings": driver.ratings,
            "points": driver.points,
        })

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    ilog(
        fn="save_mmr2_drivers",
        msg="MMR2 drivers saved",
        driver_count=len(drivers),
        filename=filename,
    )


def load_mmr2_drivers(filename="mmr2_drivers.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        drivers = []

        for driver_data in data:
            driver = Drivermmr2(
                driver_data["name"],
                driver_data["rating"],
            )

            driver.ratings = driver_data.get("ratings", driver.rating)
            driver.points = driver_data.get("points", 0)

            drivers.append(driver)

        ilog(
            fn="load_mmr2_drivers",
            msg="MMR2 drivers loaded",
            driver_count=len(drivers),
            filename=filename,
        )

        return drivers

    except FileNotFoundError:
        ilog(
            fn="load_mmr2_drivers",
            msg="MMR2 driver file not found",
            filename=filename,
        )
        return []

list_drivers_mmr2 = [Drivermmr2(name, random.uniform(5.95, 8.05)) for name in drivers_mmr2]
save_mmr2_drivers(list_drivers_mmr2)