import json
import os
from log import dlog, elog, wlog
from paths import state_file, user_input_dir

_USER_INPUT_DIR = user_input_dir()
_STATE_FILE = state_file()


_USER_INPUT_DEFAULTS = {
    "lap_user_data": {
        "driver_1": {"action": "1", "new_pneu": "medium"},
        "driver_2": {"action": "1", "new_pneu": "medium"},
        "commands": [],
    },
    "init": {},
    "settings": {"stop_on_event": True, "show_logs": False},
    "deal": {},
    "transfer": {},
    "transfer_offers": {},
}


def load_data(name: str, default=None):
    """Load a JSON file from user_input/. If missing or malformed, self-heal:
    write `default` (or the registered default for `name`) to disk and return it,
    instead of crashing every caller upstream.
    """
    path = os.path.join(_USER_INPUT_DIR, f"{name}.json")
    try:
        with open(path, encoding="utf-8") as input_file:
            data = json.load(input_file)
        dlog(fn="load_data", msg="user input loaded", name=name, path=path)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        fallback = default if default is not None else _USER_INPUT_DEFAULTS.get(name, {})
        wlog(fn="load_data", msg="user input missing/malformed — regenerating default",
             name=name, path=path, error=str(e), default=fallback)
        os.makedirs(_USER_INPUT_DIR, exist_ok=True)
        try:
            with open(path, "w", encoding="utf-8") as out_file:
                json.dump(fallback, out_file, indent=2, ensure_ascii=False)
        except OSError as write_err:
            elog(fn="load_data", msg="failed to write regenerated default", name=name,
                 path=path, error=str(write_err))
        return fallback


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