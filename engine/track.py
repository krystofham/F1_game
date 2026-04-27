class Track:
    def __init__(self, name, pneu, speed, TIME_S1, TIME_S2, TIME_S3, laps, dnf_probability):
        self.name = name
        self.pneu = pneu
        self.speed = speed
        self.TIME_S1 = TIME_S1
        self.TIME_S2 = TIME_S2
        self.TIME_S3 = TIME_S3
        self.laps = laps
        self.dnf_probability = dnf_probability
tracks = []
tracks.append(Track("Huawei GP SPA", "hard", "quick", 22, 25, 18, 70, 4500))
tracks.append(Track("LG TV Grand Prix du France", "hard", "slow", 26, 19, 22, 74, 4500))
tracks.append(Track("Sony Varsava Grand Prix","hard", "medium", 35, 18, 24, 62, 5000))
tracks.append(Track("META China Grand Prix", "medium", "slow", 25, 34, 30, 56, 4500))
tracks.append(Track("Ostrava Apple GP", "medium", "quick", 20, 26, 18, 67, 4500))
tracks.append(Track("Python circuit Bahamas", "hard", "medium", 25, 23, 38, 72, 5000))
tracks.append(Track("HP Bulgarian GP", "medium", "medium", 23, 29, 20, 60, 5000))
tracks.append(Track("AWS Grand Prix de Espana", "medium", "quick", 26, 31, 16, 51, 6000))
tracks.append(Track("AirBNB Prague GP", "soft", "quick", 20, 33, 40, 42, 4500))
tracks.append(Track("eBay Skyline Turkey GP","medium", "slow", 27, 24, 36, 49, 4900))
tracks.append(Track("Java airlines Monza IBM Italy GP","soft", "quick", 30, 16, 18, 50, 5100))