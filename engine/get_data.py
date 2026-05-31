try: from load_data_json import *
except: from engine.load_data_json import *
def get_length_of_championship() -> int:
    if load_data("init")["length"] < 0 or  load_data("init")["length"] > 12:
        raise ValueError("invalid length") 
    return load_data("init")["length"]

def get_player_pneu(PNEU_types, current_pneu, driver_key):
    try:
        data = load_data("lap_user_data")
        # Zkus driver_1/driver_2 i přímý klíč
        if driver_key in data:
            pneu = data[driver_key]["new_pneu"]
        else:
            # fallback na current_pneu pokud klíč neexistuje
            return current_pneu
        if pneu in PNEU_types:
            return pneu
        return current_pneu
    except:
        return current_pneu