try: from load_data_json import *
except: from engine.load_data_json import *
from log import dlog, elog, wlog

def get_length_of_championship() -> int:
    data = load_data("init")
    length = data["length"]
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
            wlog(fn="get_player_pneu", msg="driver key missing from lap_user_data, keeping current pneu",
                 driver_key=driver_key, current_pneu=current_pneu)
            return current_pneu
        if pneu in PNEU_types:
            dlog(fn="get_player_pneu", msg="pneu loaded from lap_user_data",
                 driver_key=driver_key, pneu=pneu)
            return pneu
        wlog(fn="get_player_pneu", msg="invalid pneu in lap_user_data, keeping current",
             driver_key=driver_key, pneu=pneu, current_pneu=current_pneu)
        return current_pneu
    except Exception as e:
        wlog(fn="get_player_pneu", msg="lap_user_data read failed, keeping current pneu",
             driver_key=driver_key, current_pneu=current_pneu, error=str(e))
        return current_pneu