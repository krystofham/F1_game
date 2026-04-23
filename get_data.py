def get_lenght_of_championship() -> int:
    while lenght <= 0:
        lenght = input("What is the lenght of the championship: ")
        try:
            return int(lenght)
        except:
            lenght = 0
def get_player_pneu(PNEU_types:dict, player_pneu:str) -> str:
    pneu = input("Pick pneu for driver 1: [hard / medium / soft / wet / inter]\n[> ")
    while player.pneu not in PNEU_types:
        pneu = input("Invalid choice. Pick pneu for driver 1: [hard / medium / soft / wet / inter]\n[> ")
        if pneu == "exit":
            return player_pneu
    return pneu