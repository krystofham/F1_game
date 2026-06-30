from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any

class LapUserDataPayload(BaseModel):
    # dynamic driver keys (e.g. "Max Vershaeren") + "commands" list
    model_config = ConfigDict(extra="allow")
    commands: List[Any] = []

class InitConfigPayload(BaseModel):
    pneu_driver_1: str
    pneu_driver_2: str
    training_mode: int

class TransferPayload(BaseModel):
    pilot_to_change: str
    chosen_pilot: str
    rating: Optional[float] = None

class SimUntilPayload(BaseModel):
    lap: int

class SettingsPayload(BaseModel):
    stop_on_event: bool
    show_logs: bool

class TeamPatch(BaseModel):
    name: Optional[str] = None

class DriverPatch(BaseModel):
    name: Optional[str] = None
    rating: Optional[float] = None

class PatchStatePayload(BaseModel):
    teams: Optional[List[TeamPatch]] = None
    drivers: Optional[List[DriverPatch]] = None
