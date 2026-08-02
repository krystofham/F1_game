try: from load_data_json import *
except: from engine.load_data_json import *
from log import dlog, elog, wlog

def get_length_of_championship() -> int:
    try:
        data = load_data("init")
        length = data["length"]
    except UserInputMissingError as e:
        elog(fn="get_length_of_championship", msg="init.json missing")
        raise ValueError("Championship not configured yet") from e
    except KeyError:
        elog(fn="get_length_of_championship", msg="init.json missing key 'length'")
        raise ValueError("init.json missing required key 'length'")
    if length < 0 or length > 12:
        elog(fn="get_length_of_championship", msg="invalid championship length", length=length)
        raise ValueError("invalid length")
    dlog(fn="get_length_of_championship", msg="championship length loaded", length=length)
    return length

def get_player_pneu(PNEU_types, current_pneu, driver_key):
    try:
        data = load_data("lap_user_data")
        if driver_key in data:
            pneu = data[driver_key]["new_pneu"]
        else:
            wlog(fn="get_player_pneu", msg="driver key missing", driver_key=driver_key)
            return current_pneu
        if pneu in PNEU_types:
            dlog(fn="get_player_pneu", msg="pneu loaded", driver_key=driver_key, pneu=pneu)
            return pneu
        wlog(fn="get_player_pneu", msg="invalid pneu", driver_key=driver_key, pneu=pneu)
        return current_pneu
    except Exception as e:
        wlog(fn="get_player_pneu", msg="read failed", driver_key=driver_key, error=str(e))
        return current_pneu