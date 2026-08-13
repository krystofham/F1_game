import json
import os

from log import dlog, elog, wlog
from paths import state_file, user_input_dir

_USER_INPUT_DIR = user_input_dir()
_STATE_FILE = state_file()

_USER_INPUT_DEFAULTS = {
    "lap_user_data": {
        "driver_1": {"action": "1", "new_tyre": "medium"},
        "driver_2": {"action": "1", "new_tyre": "medium"},
        "commands": [],
    },
    "settings": {"stop_on_event": True, "show_logs": False},
}
_REQUIRED_ACTION_FILES = {"init", "transfer", "deal", "transfer_offers"}


class UserInputMissingError(Exception):
    def __init__(self, name, path, cause=None):
        self.name = name
        self.path = path
        self.cause = cause
        super().__init__(f"required user input '{name}' missing or invalid at {path}")


def load_data(name: str, default=None):
    path = os.path.join(_USER_INPUT_DIR, f"{name}.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        dlog(fn="load_data", msg="user input loaded", name=name, path=path)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        if default is not None:
            fallback = default
        elif name in _USER_INPUT_DEFAULTS:
            fallback = _USER_INPUT_DEFAULTS[name]
        elif name in _REQUIRED_ACTION_FILES:
            elog(
                fn="load_data",
                msg="required action file missing",
                name=name,
                path=path,
                error=str(e),
            )
            raise UserInputMissingError(name, path, cause=e) from e
        else:
            fallback = {}
        wlog(
            fn="load_data",
            msg="regenerating default",
            name=name,
            path=path,
            error=str(e),
        )
        os.makedirs(_USER_INPUT_DIR, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(fallback, f, indent=2, ensure_ascii=False)
        return fallback


def load_state():
    if not os.path.exists(_STATE_FILE):
        wlog(fn="load_state", msg="state.json not found")
        return {}
    try:
        with open(_STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        elog(fn="load_state", msg="state.json malformed", error=str(e))
        return {}
