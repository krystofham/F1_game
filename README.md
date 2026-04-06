# 🏎️ F1 Manager Simulator

> A terminal-based Formula 1 career management game written in Python. Manage a team, develop race strategy, handle pit stops, and fight for the championship across multiple seasons.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Game Systems](#game-systems)
  - [Training & Car Setup](#training--car-setup)
  - [Tyre Strategy](#tyre-strategy)
  - [Weather System](#weather-system)
  - [Race Simulation](#race-simulation)
  - [Safety Car](#safety-car)
  - [Pit Stops](#pit-stops)
  - [Points System](#points-system)
  - [Driver Transfers](#driver-transfers)
  - [MMR2 (Minor League)](#mmr2-minor-league)
- [Module Reference](#module-reference)
- [Configuration & Constants](#configuration--constants)
- [Known Issues & Limitations](#known-issues--limitations)
- [Planned Features (Roadmap)](#planned-features-roadmap)
- [License](#license)

---

## Overview

F1 Manager Simulator puts you in the role of a Formula 1 team principal. Each race weekend you:

1. Configure your car setup during **training**
2. Watch your drivers qualify
3. Choose **starting tyres** for both drivers
4. React to **live weather**, **safety car** periods, and tyre wear every lap
5. Make **pit stop decisions** for both cars
6. Earn **championship points** and compete across a full season

The simulation runs entirely in the terminal with matplotlib graphs displayed after each race.

---

## Features

- ✅ Full race simulation with lap-by-lap output
- ✅ Two player-controlled drivers on the same team
- ✅ Dynamic weather system (sunny → transitional → rain → heavy rain)
- ✅ Tyre wear simulation with 5 compounds (hard, medium, soft, inter, wet)
- ✅ Safety car events and crash DNFs
- ✅ DRS activation within 1 second of the car ahead
- ✅ AI pit strategy logic that reacts to weather and wear
- ✅ Driver & constructor championship standings
- ✅ Car setup system affecting cornering, grip, and speed
- ✅ Driver transfers between MMR1 and MMR2
- ✅ Multi-season career mode
- ✅ Post-race graphs: race results, position-over-laps chart

---

## Project Structure

```
f1-manager/
│
├── main.py              # Entry point — season loop, race loop, post-season logic
├── init.py              # Global constants, initial driver/team/track lists
│
├── car.py               # Car class — lap simulation, pit stops, tyre logic, AI decisions
├── team.py              # Team class — points calculation, driver registration
├── track.py             # Track definitions — sector times, laps, DNF probability
│
├── engine.py            # Qualification, race reset, safety car events, transfer logic
├── weather.py           # Weather generation and track wettiness
├── strategy.py          # Strategy advisor — prints possible 1/2/3-stop strategies
│
├── simulating_sectors.py # Car setup training — wing/brake/suspension settings + graphs
├── printing_info.py     # In-race UI — pit menus, lap info display, leaderboard
├── plot.py              # Post-race matplotlib charts
├── mmr2.py              # Minor league season simulation (promotion/relegation source)
│
├── img/                 # Team logo images (used for championship winner display)
└── README.md
```

### Module Dependency Map

```
main.py
 ├── init.py          (constants, team/track/driver lists)
 ├── engine.py        (qualification, safety_car, reset_race, transfer)
 │    └── mmr2.py     (simulate_season_mmr2)
 │    └── weather.py  (generate_weather)
 ├── car.py           (Car class)
 ├── team.py          (Team class, create_team)
 ├── track.py         (Track class, tracks[])
 ├── weather.py       (wet_track, generate_weather)
 ├── strategy.py      (strategy advisor)
 ├── simulating_sectors.py  (training, car setup)
 ├── printing_info.py (pit_player, info, drivers_table, post_race_info)
 └── plot.py          (plot_graph, colours_graphs)
```

---

## Installation

### Requirements

- Python 3.8 or higher
- pip

### Dependencies

```bash
pip install matplotlib
```

### Clone & Run

```bash
git clone https://github.com/your-username/f1-manager.git
cd f1-manager
python3 main.py
```

> **Note:** The game is fully interactive and runs in the terminal. A graphical window (matplotlib) will open after each race to show results.

---

## How to Play

### 1. Start the Game

```bash
python3 main.py
```

You will be asked:

```
What is the length of the championship:
```

Enter a number between 1 and 11 (total available circuits). The game will select that many races from the championship calendar.

---

### 2. Race Weekend Flow

Each race follows this order:

```
Training (car setup) → Qualification → Race Laps → Post-Race → Next Race
```

#### Training

You have **3 attempts** to configure:

| Setting | Range | Effect |
|---|---|---|
| Front wing | 0–11 | Higher = less understeer, more drag |
| Rear wing | 0–11 | Higher = more downforce, less top speed |
| Brakes | 50–60 | Balance affects oversteer/understeer |
| Anti-roll bars | 1 (soft) / 2 (hard) | Hard = faster, less grip |
| Springs | 1 (hard) / 2 (soft) | Hard = faster, less stable |

After each attempt, a **sector simulation graph** shows your car vs a benchmark bot across 15 corners.

A good setup can unlock a **speed bonus** that applies during the race.

#### Tyre Selection

Before the race you pick starting tyres for each driver:

```
Pick pneu for driver 1: [hard / medium / soft / wet / inter]
```

The **strategy advisor** will print suggested 1-stop, 2-stop, and 3-stop strategies based on the track and expected weather.

#### During the Race

Each lap you see:
- Current weather and forecast (4 laps ahead — occasionally inaccurate)
- Track wettiness percentage
- Top 6 leaderboard with gaps and tyre wear
- Your drivers' position, delta to the car ahead/behind, tyre wear

Then for **each of your drivers** you choose:

```
Action: [1] continue [2] box
```

If you box, you pick the new tyre compound.

**Secret commands** (undocumented in-game):
- `PNEUSTAV` — displays exact tyre wear for that driver (costs +2s)
- `PNEUSAFE` — reduces tyre wear by 1% (costs +3s)

---

### 3. Post-Race

After the race you see:
- Final classification with times and points
- Fastest lap + fastest sector holders
- Constructor standings
- Three matplotlib graphs open:
  1. Horizontal bar chart of total race times
  2. Position-over-laps for all drivers
  3. Position-over-laps for your two drivers only

---

### 4. Post-Season

At the end of the championship:
- The **last-place driver** is automatically replaced by the MMR2 champion
- AI teams may swap drivers based on team rating vs driver rating mismatch
- You are asked if you want to **sign a new driver** (optional transfer)
- All points reset for the new season

---

## Game Systems

### Training & Car Setup

File: `simulating_sectors.py`

The setup system simulates 15 corners across three types (slow, medium, fast). Each setting shifts an internal vector of 6 attributes:

```python
settings = [speed_in_training, understeer, oversteer, acceleration, grip, curb_handling]
```

The resulting `speed_bonus` flag (True/False) is passed into the race simulation. A good setup (`speed_bonus = True`) shaves approximately 0.3–0.5 seconds off each sector per lap.

Car setup also adjusts the player's `safety_car_probability` — good grip/curb handling reduces crash risk; extreme understeer/oversteer increases it.

---

### Tyre Strategy

File: `strategy.py`, `car.py`

Five compounds are available:

| Compound | Wear rate | Speed multiplier | Best in |
|---|---|---|---|
| Hard | Low | ~1.0× | Dry, long stints |
| Medium | Medium | ~1.04× | Dry, balanced |
| Soft | High | ~1.08× | Dry, qualifying |
| Inter | Medium | ~0.65× | Light rain / drying track |
| Wet | Medium | ~0.60× | Heavy rain |

**Wear rates** and **speed multipliers** scale with the track's `pneu` and `speed` classification. A "soft" track wears tyres faster; a "quick" track provides higher speed multipliers across all compounds.

Tyres degrade every lap (`PNEU_types[compound]["wear"]` + random noise). At 80% wear there is a 55% chance per lap of a puncture. At 100% wear a DNF is guaranteed.

---

### Weather System

File: `weather.py`

Weather is a Markov chain with four states:

```
sunny → transitional → rain → heavy rain
```

Transitions depend on the track's `climax` setting (either `"sunny"` or `"transitional"`). On a sunny climax the weather is locked to sunny. On a transitional climax, rain can develop over the race.

The 4-lap forecast shown in-game has a ~20% chance of being randomised (fake), forcing the player to read the situation themselves.

**Track wettiness** (`WETTINESS`) is a 0–100% value that increases in rain and dries in sun. Dry-weather tyres on a wet track (wettiness > 55%) receive a heavy time penalty.

---

### Race Simulation

File: `car.py` — `simuluj_lap()`

Each lap, sector times are calculated as:

```
sector_time = (base_sector_time × random(0.99–1.01) + driver_rating/2 + team_rating/2) / tyre_speed_multiplier
```

Modifiers applied on top:
- **Safety car active**: all sectors × 2.5
- **DRS active**: each sector − random(0.5–0.7)s
- **Training bonus**: each sector − random(0.1–0.3)s
- **Speed bonus** (from setup): each sector − random(0.3–0.5)s
- **Wrong tyre for conditions**: each sector + wettiness/2

Accumulated time (`car.time`) includes tyre wear degradation (`wear/8` per lap).

---

### Safety Car

File: `engine.py` — `safety_car()`

Each car has a `safety_car_probability` value (set from the track's `dnf_probability`). Every lap, a random check determines if that car causes an incident:

- In dry conditions: `1-in-probability` chance of DNF + safety car
- In wet conditions: `1-in-(probability/5)` — five times more likely
- Minor mistakes (no DNF) can also occur, adding random time

The safety car lasts a random 3–6 laps (`LAPS_REMAINING`).

---

### Pit Stops

File: `car.py` — `pit_stop()`, `printing_info.py` — `pit_player()`

Pit stop cost:
- Normal conditions: **+100 seconds**
- Safety car active: **+50 seconds** (undercut advantage)

After pitting:
- Tyre wear resets to 0
- The new compound is applied
- The stint is recorded: `(start_time, stint_duration, compound)`

AI pit logic (`choose_ai()`) checks:
1. Is the current tyre wrong for forecasted weather?
2. Is wear ≥ 80%?
3. Is safety car out and wear > 70%?
4. How many laps remain — pick the fastest compound that will last?

---

### Points System

File: `car.py` — `vypocitej_points_jezdec()`, `team.py` — `vypocitej_points()`

Points are awarded to finishing positions 1–23:

| Position | Points |
|---|---|
| 1st | 50 |
| 2nd | 45 |
| 3rd | 40 |
| 4th | 35 |
| 5th | 30 |
| 6th | 25 |
| 7th | 22 |
| 8–10th | 20 / 18 / 15 |
| 11–23rd | 12 down to 1 |

Fastest lap earns +2 points for the team.

---

### Driver Transfers

File: `engine.py` — `transfer()`

At the end of each season you can optionally sign a new driver. Options come from:

1. **MMR1 (current grid)** — teams whose rating significantly exceeds a driver's rating will offer them. High-rated player drivers attract more suitors.
2. **MMR2 (minor league)** — the MMR2 season champion can be recruited to replace one of your drivers.

Transfers swap names and ratings between the old and new driver objects.

---

### MMR2 (Minor League)

File: `mmr2.py`

A simplified parallel series with 20 drivers running a 12-race × 50-lap season. Each lap time is `driver.rating × random(0.98–1.02)`. The best (lowest cumulative time) and worst driver are returned to `main.py` for promotion/relegation logic.

The worst MMR2 driver is replaced each season by a name from `names_free_drivers` (a pool of 25 reserve drivers in `init.py`).

---

## Module Reference

### `car.py` — `Car`

| Method | Purpose |
|---|---|
| `__init__(name, rating, is_player)` | Create a car with given driver name and rating (5–7 scale) |
| `efectivity_pneu(weather, PNEU_types)` | Returns speed multiplier for current compound + weather |
| `simuluj_lap(...)` | Simulate one lap; returns updated `SAFETY_CAR`, `LAPS_REMAINING` |
| `pit_stop(new_pneu, SAFETY_CAR)` | Execute pit stop, record stint |
| `choose_ai(...)` | AI strategy decision; returns new tyre or None |
| `simuluj_ai(...)` | Wrapper: AI pit decision + lap simulation |
| `player_info(...)` | Print lap info for player-controlled cars |
| `drss(car_in_front)` | Activate DRS if gap < 1s |
| `vhodne_pneu(weather)` | Return list of appropriate compounds for weather |
| `vypocitej_points_jezdec(RANK)` | Add championship points based on final position |

### `team.py` — `Team`

| Method | Purpose |
|---|---|
| `__init__(name, rating)` | Create team |
| `pridej_jezdce(car)` | Register a driver to this team |
| `vypocitej_points(RANK, COUNT_CARS)` | Add constructor points from both drivers' positions |

### `engine.py`

| Function | Purpose |
|---|---|
| `qualification(simulation, cars, ...)` | Sort cars by simulated quali time; apply grid penalties |
| `reset_race(climax, cars)` | Reset all race state variables for a new race |
| `safety_car(car, weather, lap, ...)` | Roll for safety car / DNF events per car per lap |
| `transfer(cars, teams, player, ...)` | Handle end-of-season driver transfer UI |

### `weather.py`

| Function | Purpose |
|---|---|
| `generate_weather(current, climax)` | Markov transition to next weather state |
| `wet_track(weather, wettiness)` | Update track wettiness % each lap |

### `strategy.py`

| Function | Purpose |
|---|---|
| `strategy(LAPS, ...)` | Print 1/2/3-stop strategy options with estimated race times |

### `track.py` — `Track`

| Attribute | Description |
|---|---|
| `name` | Race name (matches championship calendar) |
| `pneu` | Tyre wear category: `"soft"`, `"medium"`, `"hard"` |
| `speed` | Track speed: `"slow"`, `"medium"`, `"quick"` |
| `TIME_S1/S2/S3` | Base sector times in seconds |
| `laps` | Total race laps |
| `dnf_probability` | Base denominator for crash probability roll |

---

## Configuration & Constants

Set in `init.py`:

| Constant | Default | Description |
|---|---|---|
| `DRIVER_1` | `"Max Vershaeren"` | Player driver 1 name |
| `DRIVER_2` | `"Kim Nguyen"` | Player driver 2 name |
| `TEAM_PLAYER` | `"MySql AWS Maxim racing team"` | Player team name |
| `COUNT_CARS` | 28 | Total cars on grid |
| `TIME_S1/S2/S3` | 15 / 23 / 22 | Default sector times (overridden per track) |

To add new tracks, append a `Track(...)` to the `tracks` list in `track.py`. To add new circuits to the calendar, append to the `championship` list in `init.py`.

---

## Known Issues & Limitations

- The rain pit stop logic for AI cars can sometimes leave them on dry compounds too long in heavy rain
- Negative times can theoretically occur with extreme setup values (tracked in what_i_want.txt as "záporný čas")
- Loop issue at lap ~1426 in very long races (tracked as "Zacyklení 1426")
- The transfer screen for MMR2 has a logic error — the `while` loop condition uses `or` instead of `and`, making it uncheckable
- `driver_to_trade_1.name, driver_to_trade_2.name == ...` in `main.py` is a comparison, not a swap; AI transfers do not actually execute
- Understeer display in the sector sim uses understeer values but does not visualise throttle (planned improvement)

---

## Planned Features (Roadmap)

From `what_i_want.txt` and the developer notes:

**Gameplay**
- [ ] Driver fatigue & morale system
- [ ] Team orders (allow teammate past)
- [ ] Mechanical failures (engine, gearbox, suspension)
- [ ] Overtaking probability per sector / DRS zone
- [ ] Fuel management (light vs heavy load)
- [ ] Tyre temperature simulation
- [X] Driver rating evolution over seasons
- [ ] Driving style per driver (aggressive, conservative, etc.)

**Weather**
- [ ] Sector-based rain (one sector wet, others dry)
- [X] Weather radar with limited accuracy

**Analytics**
- [ ] Web dashboard for standings and lap data

**Technical**
- [ ] JSON/YAML config files for circuits, teams, drivers
- [ ] Save / load season state
- [ ] Season history & CSV export
- [X] Modular architecture refactor
- [ ] Replay system

---

## License

MIT License — see [LICENSE](LICENSE) for details.

Copyright (c) 2025 Mightysniper22