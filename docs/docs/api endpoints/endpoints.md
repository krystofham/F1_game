---
sidebar_position: 1
---
# POST

## /api/init_race
init race before it can begin 
### Possible code
- `{"status":"ok","race":"AWS Grand Prix de Espana","lap":0,"total_laps":null}`

## /api/sim_lap
Sim one lap
## /api/post_race
after race call this
## /api/post_championship
after chapipionship
### Possible code
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
## /api/get_teams/{team_name}
return json with team based on team name -need to be an exact string of team name
# Other
## Helpers
### load_game_objects
Returns game object from init
### load json
Return loaded json from path
### state
returns state.json