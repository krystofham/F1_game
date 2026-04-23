def get_lenght_of_championship() -> int:
    try:
        lenght = int(input("What is the lenght of the championship: "))
    except:
        lenght = 0
    while lenght <= 0:
        lenght = input("What is the lenght of the championship: ")
        try:
            lenght =  int(lenght)
        except:
            lenght = 0
    return lenght
def get_player_pneu(PNEU_types:dict, player_pneu:str) -> str:
    pneu = input("Pick pneu for driver 1: [hard / medium / soft / wet / inter]\n[> ")
    while pneu not in PNEU_types:
        pneu = input("Invalid choice. Pick pneu for driver 1: [hard / medium / soft / wet / inter]\n[> ")
        if pneu == "exit":
            return player_pneu
    return pneu