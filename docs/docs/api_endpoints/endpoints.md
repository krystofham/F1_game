---
sidebar_position: 1
---
# POST

## /api/init_race
init race before it can begin 
Config file: init.json
### Structure
Currently not working training_mode, front_wing, rear_wing, brakes, stabilizators, springs.
length is for season len.
```json
{
    "length": 2,
    "pneu_driver_1": "hard",
    "pneu_driver_2": "hard",
    "training_mode": 1,
    "front_wing": 5,
    "rear_wing": 5,
    "brakes": 55,
    "stabilizators": 1,
    "springs":1   
}
```
### Possible code
- `{"status":"ok","race":"AWS Grand Prix de Espana","lap":0,"total_laps":null}`

## /api/sim_lap
- `{"detail":"Race not initialized. Call /api/init_race first."}`
- `{"status":"ok","lap":2,"total_laps":51,"finished":false}`
Sim one lap
## /api/post_race
after race call this
## /api/post_championship
after chapipionship

# GET
## /get/state
return state witch loaded state func
## /api/get_drivers
returns json with structure
## /api/get_teams
return json with teams
structure:
```json
  "teams": [
    {
      "position": 1,
      "name": "MySql AWS Maxim racing team",
      "points": 0,
      "rating": 5.1439,
      "drivers": [
        "Max Vershaeren",
        "Kim Nguyen"
      ]
    }
    ...
  ]
```
## /api/get_teams/team_name
return json with team based on team name -need to be an exact string of team name
# Other
## Helpers
### load_game_objects
Returns game object from init
### load json
Return loaded json from path
### state
returns state.json
### init first
Inserts into init.json data
1) Lenght
### init
Inserts into init.json data
1) training_mode
2) pneu_driver_1
3) pneu_driver_2
