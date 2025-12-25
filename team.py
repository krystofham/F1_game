class Team:
    def __init__(self, name, skill):
        self.name = name
        self.skill = skill
        self.drivers = [] 
        self.points = 0   

    def pridej_jezdce(self, car):
        self.drivers.append(car)
        car.team = self

    def vypocitej_points(self, RANK, COUNT_CARS):
        for jezdec in self.drivers:
            if jezdec.name in RANK:
                position = RANK.index(jezdec.name) + 1
            else:
                position = COUNT_CARS
            if position == 1:
                self.points += 50
            elif position == 2:
                self.points += 45
            elif position == 3:
                self.points += 40
            elif position == 4:
                self.points += 35
            elif position == 5:
                self.points += 30
            elif position == 6:
                self.points += 25
            elif position == 7:
                self.points += 22
            elif position == 8:
                self.points += 20
            elif position == 9:
                self.points += 18
            elif position == 10:
                self.points += 15
            elif position == 11:
                self.points += 12
            elif position == 12:
                self.points += 10
            elif position == 13:
                self.points += 9
            elif position == 14:
                self.points += 8
            elif position == 15:
                self.points += 7
            elif position == 16:
                self.points += 6
            elif position == 17:
                self.points += 5
            elif position == 18:
                self.points += 4
            elif position == 19:
                self.points += 3
            elif position == 20:
                self.points += 2
            elif position == 21:
                self.points += 1
            elif position == 22:
                self.points += 1
            elif position == 23:
                self.points += 1

teams = []
def create_team(TEAM_PLAYER, player_1, player_2, teams, skill):
    tym = Team(TEAM_PLAYER, skill)
    tym.pridej_jezdce(player_1)
    tym.pridej_jezdce(player_2)
    teams.append(tym)
    return tym
