from big_functions import * 

lenght = get_lenght_of_championship()
championshionship_race_count = len(championship) - lenght
if championshionship_race_count > 0:
    for _ in range(championshionship_race_count):
        championship.pop(random.randint(0, len(championship)-1))
season_count = 1
b = 1


print(f"Season {season_count}")

time_laps = [] 
for race in championship:
    speed_bonus, season_count, time_laps, k_speed, k_wear, training_type, WETTINESS, lap, forecast, weather, climax, pneu, speed, PNEU_types, weather_1, weather_2, weather_3, weather_4, weather = init_race(tracks, race, cars, teams, championship, player, player_2, b, season_count)
    while lap <= LAPS:
        lap, cars, teams = sim_the_lap(
            cars, teams, player, player_2, lap, SAFETY_CAR, LAPS_REMAINING,
            WETTINESS, forecast, weather, LAPS, climax, DRIVER_1, DRIVER_2,
            pneu, speed, PNEU_types, weather_1, weather_2, weather_3, weather_4,
            training_type, k_wear, speed_bonus, season_count, race, time_laps
        )
    #post race
    RANK = [a for a in cars if not a.dnf]
    save_state_end_of_race(cars, teams, season_count, race)
    teams, cars, time_laps = post_race_info(time_laps, player, player_2, cars, teams, COUNT_CARS)
    points, cars, teams, players = plot_graph(RANK, DRIVER_1, DRIVER_2, teams, cars, player, player_2, climax)
    lap, time_laps, SAFETY_CAR, LAPS_REMAINING, weather, forecast, cars, WETTINESS = reset_race(climax, cars)
    b+=1
#post chamiponship
save_state_end_of_season(cars, teams, season_count)
print("\n🏁 Drivers at the end of championship:")
best, worst = simulate_season_mmr2(list_drivers_mmr2)
season_count +=1
for mmr2_driver in list_drivers_mmr2:
    mmr2_driver.rating -= 1/(season_count*2)
random_name = random.choice(names_free_drivers)
# names_free_drivers.pop(names_free_drivers.index(random_name))
worst.name, worst.rating = random_name, random.uniform(0.95,1.05)
cars.sort(key=lambda x: x.points, reverse=True)
for i, a in enumerate(cars, 1):
    print(f"{i}. {a.name} – {a.points} points ({a.team.name})")
    if i == len(cars):
        new = best.name
        rating = best.rating
        print(f"Breaking!!!\n{new} changes {a.name} ({a.team.name})\nBreaking!!!")
        if a.is_player:
            if DRIVER_1 == a.name:
                DRIVER_1 = new
                player.name, player.ratings = new, rating
            if DRIVER_2 == a.name:
                DRIVER_2 = new
                player_2.name, player_2.ratings = new, rating
        best.name, best.rating = a.name, a.ratings
        a.name, a.ratings = new, rating
print_teams_end_championship(teams)
teams, player, player_2, DRIVER_1, DRIVER_2, cars = trading_at_the_of_season(teams, player, player_2, DRIVER_1, DRIVER_2, cars)
WETTINESS, cars, teams =  reset_championship(cars, teams)
