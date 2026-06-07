import json
import os
from log import dlog, elog, wlog

_USER_INPUT_DIR = os.path.join(os.path.dirname(__file__), "user_input")
_STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")


def load_data(name: str):
    path = os.path.join(_USER_INPUT_DIR, f"{name}.json")
    try:
        with open(path, encoding="utf-8") as input_file:
            data = json.load(input_file)
        dlog(fn="load_data", msg="user input loaded", name=name, path=path)
        return data
    except FileNotFoundError:
        elog(fn="load_data", msg="user input file not found", name=name, path=path)
        raise
    except json.JSONDecodeError as e:
        elog(fn="load_data", msg="user input malformed JSON", name=name, path=path, error=str(e))
        raise


def load_state():
    if not os.path.exists(_STATE_FILE):
        wlog(fn="load_state", msg="state.json not found, returning empty dict")
        return {}
    try:
        with open(_STATE_FILE, encoding="utf-8") as f:
            state = json.load(f)
        dlog(fn="load_state", msg="state.json loaded",
             type=state.get("type"), lap=state.get("lap"), race=state.get("race"))
        return state
    except json.JSONDecodeError as e:
        elog(fn="load_state", msg="state.json malformed JSON", error=str(e))
        return {}