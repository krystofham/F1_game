try: from load_data_json import *
except: from engine.load_data_json import *
def get_length_of_championship() -> int:
    if load_data("init")["length"] < 0 or  load_data("init")["length"] > 12:
        raise ValueError("invalid length") 
    return load_data("init")["length"]

def get_player_pneu(PNEU_types:dict, player_pneu:str, driver) -> str:
    pneu = load_data("lap_user_data")[driver]["new_pneu"]
    if pneu == "":
        return player_pneu
    return pneu