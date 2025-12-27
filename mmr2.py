import random
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