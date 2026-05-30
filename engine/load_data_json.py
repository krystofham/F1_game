import json
import os
def load_data(name: str):
    with open(f"user_input/{name}.json", "r") as input_file:
        data = json.load(input_file)
    return data
_STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")
def load_state():
    if not os.path.exists(_STATE_FILE):
        return {}
    try:
        with open(_STATE_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}