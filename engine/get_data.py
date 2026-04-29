from load_data_json import *
def get_lenght_of_championship() -> int:
    if load_data("init")["lenght"] < 0 or  load_data("init")["lenght"] > 12:
        raise ValueError("invalid lenght") 
    return load_data("init")["lenght"]

def get_player_pneu(PNEU_types:dict, player_pneu:str, driver) -> str:
    pneu = load_data("lap_user_data")[driver]["new_pneu"]
    if pneu == "":
        return player_pneu
    return pneu