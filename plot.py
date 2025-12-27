import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random
from engine import reset_race
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

def plot_graph(RANK, DRIVER_1, DRIVER_2, teams, cars, player, player_2, climax):
    points = sorted(teams, key=lambda x: (x.points))
    # Rank count
    position_1 = None
    position_2 =None
    for x in RANK:
        if x.name == DRIVER_1:
            position_1 = RANK.index(x) + 1
        if x.name == DRIVER_2:
            position_2 = RANK.index(x) + 1
    if position_1 == None: 
        position_1 = 'DNF'    
    if position_2 == None: 
        position_2 = 'DNF'
    print("\n🏁 Final Position:")
    print(f"{DRIVER_1}: {position_1}. position")
    print(f"{DRIVER_2}: {position_2}. position")
    #time.sleep(4)
    # Results
    cars.sort(key=lambda x: (x.dnf, x.time))
    for i, a in enumerate(cars, 1):
        stav = "DNF" if a.dnf else f"{round(a.time, 2)}s"
        print(f"{i}. {a.name} ({a.team.name}) {a.points} points ({a.ratings+ random.uniform(0,4) - random.uniform(0,4)} rating)")
    teams.sort(key=lambda team: team.points, reverse=True)
    #time.sleep(8)
    for i, team in enumerate(teams,1):
        print (f"{i}.{team.name} {team.points} points")
    #time.sleep(8)
    jmena = [a.name for a in cars]
    timey = [a.time/60 if not a.dnf else None for a in cars]
    # colours podle pneu
    colours = []
    colours_graphs(cars, colours)
    # Last stint for every car
    for a in cars:
        if not a.dnf:
            a.stints.append((a.last_stint_start, a.time - a.last_stint_start, a.pneu))
    # Print graph
    plt.figure(figsize=(12, 6))
    plt.barh(jmena[::-1], [c if c is not None else 0 for c in timey][::-1], color=colours[::-1])
    plt.xlabel("time (min)")
    plt.ylabel("Drivers")
    plt.title("🏁 Results of race")
    plt.tight_layout()
    plt.show()
    plt.figure(figsize=(10, 6))
    for a in cars:
        plt.plot(range(1, len(a.position) + 1), a.position, label=a.name)

    plt.gca().invert_yaxis()  # cause first place is the best
    plt.xlabel("lap")
    plt.ylabel("Position")
    plt.title("Position during race")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.figure(figsize=(10, 6))
    players = [player, player_2]
    for a in players:
        plt.plot(range(len(a.position)), a.position, label=a.name)

    plt.gca().invert_yaxis()  # cause first place is the best
    plt.xlabel("lap")
    plt.ylabel("Position")
    plt.title("Position during race")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    return points, cars, teams, players