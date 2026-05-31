import random

drivers_mmr2 = [
    "Noah Blake", "Felipe Sandoval", "Luca Moretti", "Brian Chen", "Adam Kerdöl", "Pierre Gauthier",
    "Viktor Orlov", "Daisuke Tanaka", "Elias Müller", "Jordan Evans", "Diego Ramirez", "Anton Petrov",
    "Kenji Nakamura", "Nicolas Dubois", "Thomas Fischer", "Miguel Lopéz", "Alexei Solapov", "Ethan Zhang",
    "Leo Harrington", "Marco Silva"
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
        self.pneu = "medium"
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
    for driver in drivers:
        driver.time = 0.0
    for lap in range(50 * 12):
        for driver in drivers:          # ← chybělo "for driver in drivers"
            driver.time += driver.rating * random.uniform(0.98, 1.02)
    mmr2_sorted = sorted(drivers, key=lambda x: x.time)
    return mmr2_sorted[0], mmr2_sorted[-1]

list_drivers_mmr2 = [Drivermmr2(name, random.uniform(5.95, 8.05)) for name in drivers_mmr2]
