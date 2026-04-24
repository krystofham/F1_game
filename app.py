from fastapi import FastAPI

app = FastAPI()

"""
data in
    driver.json
    teams.json
    state.json
"""
with open(os.path.join(_CONFIG, "drivers.json"), encoding="utf-8") as f:
    drivers = json.load(f)

with open(os.path.join(_CONFIG, "teams.json"), encoding="utf-8") as f:
    teams = json.load(f)

with open(os.path.join(_CONFIG, "state.json"), encoding="utf-8") as f:
    state = json.load(f)


@app.get("/api/get_teams")
def read_teams():
    return {}

@app.get("/api/get_team/{team_id}")
def get_team(team_id):
    if team_id < 12:
        return 403
    else:
        return {}
@app.get("/api/get_players")
def get_players():
    return {}

@app.get("/api/get_player/{player_id}")
def get_player():
    return {}

@app.get("/api/get_state")
def get_state():
    return {}