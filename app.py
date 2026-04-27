from fastapi import FastAPI
import os
import json
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Povolí přístup z tvého React vývojového serveru
    allow_methods=["*"],
    allow_headers=["*"],
)



"""
data in
    driver.json
    teams.json
    state.json
"""
_CONFIG = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_CONFIG, "config/drivers.json"), encoding="utf-8") as f:
    drivers = json.load(f)

with open(os.path.join(_CONFIG, "config/teams.json"), encoding="utf-8") as f:
    teams = json.load(f)

with open(os.path.join(_CONFIG, "engine/state.json"), encoding="utf-8") as f:
    state = json.load(f)

class Player_team(BaseModel):
    name: str
    driver_1: str
    driver_2: str
    performance_min: float
    performance_max: float

class Team(BaseModel):
    name: str
    performance_max: float
    performance_min: float
    car_indices: list[int]

class Teams(BaseModel):
    player_team: Player_team
    teams: list[Team]




@app.get("/api/get_teams")
async def read_teams():
    return teams

@app.get("/api/get_team/{team_id}")
async def get_team(team_id:str):
    try:
        if int(team_id) > 12:
            raise HTTPException(status_code=404, detail="Team index out of range")        
        else:
            return teams["teams"][int(team_id)]
    except ValueError:
        raise HTTPException(status_code=400, detail="Attribut should be a number")

@app.get("/api/get_drivers")
async def get_players():
    return drivers

@app.get("/api/get_driver/{driver_id}")
async def get_player(driver_id:str):
    return drivers[driver_id]

@app.get("/api/get_state")
async def get_state():
    return state