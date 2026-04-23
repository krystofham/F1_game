import random
from engine import transef_mmr1, transfer
drivers_mmr2 = [
    "Noah Blake", "Felipe Sandoval", "Luca Moretti", "Brian Chen", "Adam Kerdöl", "Pierre Gauthier",
    "Viktor Orlov", "Daisuke Tanaka", "Elias Müller", "Jordan Evans", "Diego Ramirez", "Anton Petrov",
    "Kenji Nakamura", "Nicolas Dubois", "Thomas Fischer", "Miguel Lopéz", "Alexei Solapov", "Ethan Zhang",
    "Leo Harrington", "Marco Silva"
]
class Drivermmr2:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
        self.time = 0.0

# Function to simulate the season
def simulate_season_mmr2(drivers):
    for driver in drivers:
        for lap in range(50*12):  # For 50 laps per race For 12 races
            driver.time += driver.rating * random.uniform(0.98, 1.02)  # Add time based on experience
    
    # Sort drivers by their time (lower is better)
    print("TOP 5 MMR2 drivers:")
    mmr2_sorted = sorted(drivers, key=lambda x: x.time)
    for i, x in enumerate(mmr2_sorted, 1):
        random_n = random.uniform(0,4)
        print(f"{i}. {x.name} (rating: {round(x.rating + random_n - 2, 1)})")
        if i == 5:
            break
    # Best driver is the one with the lowest time
    best = mmr2_sorted[0]
    # Worst driver is the one with the highest time
    worst = mmr2_sorted[-1]  
    
    return best, worst


# Create a list of drivers with random experience
list_drivers_mmr2 = [Drivermmr2(name, random.uniform(5.95, 8.05)) for name in drivers_mmr2]

def trading_at_the_of_season(teams, player, player_2, DRIVER_1, DRIVER_2, cars):
    answear = input("Important question")
    while answear == "":
        answear = input("Important question")
    new_pilot = input("Do you want new pilot? YES/NO\n").lower()   
    while new_pilot not in ("yes", "no"):
        new_pilot = input("Do you want new pilot? YES/NO\n").lower()   
    if new_pilot == "yes":
        player, player_2, DRIVER_1, DRIVER_2, cars = transfer(cars, teams, player, player_2, DRIVER_1, DRIVER_2)        
    class Want:
        def __init__(self, name):
            self.name = name
            self.transfer_did = False
    want_trade = []
    for x in teams:
        for y in x.drivers:
            if x.rating - y.ratings > 0.8 and y.is_player == False:
                want_trade.append(Want(y))
    while len(want_trade) >= 2:
        driver_to_trade_1, driver_to_trade_2 = random.sample(want_trade, 2)
        print(f"Breaking!!!\n {driver_to_trade_1.name.name} ({driver_to_trade_1.name.team.name}, {driver_to_trade_1.name.points} points) changes {driver_to_trade_2.name.name} ({driver_to_trade_2.name.team.name}, {driver_to_trade_2.name.points} points)\nBreaking!!!")
        driver_to_trade_1.name, driver_to_trade_2.name = driver_to_trade_2.name, driver_to_trade_1.name
        want_trade.remove(driver_to_trade_1)
        want_trade.remove(driver_to_trade_2)
