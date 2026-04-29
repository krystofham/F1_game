import json
def load_data(name: str):
    with open(f"user_input/{name}.json", "r") as input_file:
        data = json.load(input_file)
    return data