#!/usr/bin/env python3
"""Verify Pydantic models used by FastAPI endpoints."""
from pydantic import ValidationError

from models import (
    InitConfigPayload,
    LapUserDataPayload,
    PatchStatePayload,
    SettingsPayload,
    SimUntilPayload,
    TransferPayload,
)


def ok(name: str) -> None:
    print(f"  OK  {name}")


def fail(name: str, err: Exception) -> None:
    print(f"  FAIL {name}: {err}")
    raise SystemExit(1)


def main() -> None:
    print("Pydantic model validation")

    # Valid payloads
    InitConfigPayload(pneu_driver_1="hard", pneu_driver_2="soft", training_mode=2)
    ok("InitConfigPayload valid")

    LapUserDataPayload(commands=[], **{"Max Vershaeren": {"pace": "normal"}})
    ok("LapUserDataPayload valid with extra driver keys")

    TransferPayload(pilot_to_change="A", chosen_pilot="B", rating=5.5)
    ok("TransferPayload valid")

    SimUntilPayload(lap=10)
    ok("SimUntilPayload valid")

    SettingsPayload(stop_on_event=True, show_logs=False)
    ok("SettingsPayload valid")

    PatchStatePayload(teams=[{"name": "Team X"}], drivers=[{"name": "Driver Y", "rating": 5.0}])
    ok("PatchStatePayload valid")

    # Invalid payloads should raise
    for bad, model, label in [
        ({"pneu_driver_1": "hard"}, InitConfigPayload, "InitConfigPayload missing fields"),
        ({"lap": "not-int"}, SimUntilPayload, "SimUntilPayload bad lap type"),
        ({}, TransferPayload, "TransferPayload missing required"),
    ]:
        try:
            model(**bad)
            fail(label, ValidationError("expected ValidationError"))
        except ValidationError:
            ok(f"{label} rejected")

    # FastAPI app imports models without error
    import app  # noqa: F401
    ok("app.py imports models and loads")

    print("\nAll Pydantic checks passed.")


if __name__ == "__main__":
    main()
