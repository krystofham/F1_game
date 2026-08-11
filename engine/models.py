from typing import Any

from pydantic import BaseModel, ConfigDict


class LapUserDataPayload(BaseModel):
    # dynamic driver keys (e.g. "Max Vershaeren") + "commands" list
    model_config = ConfigDict(extra="allow")
    commands: list[Any] = []


class InitConfigPayload(BaseModel):
    pneu_driver_1: str
    pneu_driver_2: str
    training_mode: int


class TransferPayload(BaseModel):
    pilot_to_change: str
    chosen_pilot: str
    rating: float | None = None


class SimUntilPayload(BaseModel):
    lap: int


class SettingsPayload(BaseModel):
    stop_on_event: bool
    show_logs: bool


class TeamPatch(BaseModel):
    name: str | None = None


class DriverPatch(BaseModel):
    name: str | None = None
    rating: float | None = None


class PatchStatePayload(BaseModel):
    teams: list[TeamPatch] | None = None
    drivers: list[DriverPatch] | None = None
