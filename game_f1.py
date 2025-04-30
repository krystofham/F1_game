import random
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json
#import csv
poradi = 0
nazvy_jezdcu = [    "Maximilian Becker", "Santiago Cruz",   "Oliver Wright", "Hiroshi Takeda",     "Sebastian Fontaine", "Mateo Silva",     "Jonas Lindberg", "Ivan Kuznetsov",     "Lorenzo Bianchi", "Connor Mitchell",    "Rafael Ortega", "Tobias Schmidt",     "Yuto Nakamura", "Charles Lambert",     "Gabriel Costa", "Andrei Petrescu",    "Lucas Meyer", "Zhang Wei",     "Finn Gallagher", "Ricardo Santos"]
CAS_S1 = 15
CAS_S2 = 23
CAS_S3 = 22
casy_kol = []
KOL = 0
laps_rem = 0
driver_1 = "Max"
driver_2 = "Kim"
#while driver_1 == "":
#    driver_1 = input("Chybný vstup. Jak se jmenuje jezdec 1: ")
#while driver_1 == driver_2 or driver_2 == "":
#    driver_2 = input("Chybný vstup. Jak se jmenuje jezdec 2: ")
team_player = "MySql AWS Maxim racing team"
POCET_AUT = 28

POCASI_TYPY = ["slunečno", "přechodné", "déšť", "silný déšť"]
pneu_barvy = {
    "tvrdé": "gray",
    "střední": "yellow",
    "měkké": "red",
    "inter": "green",
    "mokré": "deepskyblue"
}
def zkontroluj_pneu(nova):
    if nova == "tvrde" or nova == "hard":
        nova = "tvrdé"
    if nova == "med" or nova == "medium" or nova == "stredni":
        nova = "střední"
    if nova == "soft" or nova == "mekke":
        nova = "měkké"
    if nova == "mokre" or nova == "wet":
        nova = "mokré"
    if nova == "intermedial":
        nova = "inter"
    return nova
def barvy_grafy():
    for a in auta:
        if a.dnf:
            barvy.append("red")
        elif a.pneu.lower() == "tvrdé":
            barvy.append("gray")
        elif a.pneu.lower() == "střední":
            barvy.append("yellow")
        elif a.pneu.lower() == "měkké":
            barvy.append("red")
        elif a.pneu.lower() == "mokré":
            barvy.append("blue")
        elif a.pneu.lower() == "inter":
            barvy.append("green")
        else:
            barvy.append("green")  # fallback
    return barvy
def info():
    predpoved = [pocasi_1, pocasi_2, pocasi_3, pocasi_4]
    if kolo == 0:
        print(f"Kvalifikace | Aktuální počasí: {pocasi}")
    else:
        print(f"\n🌤️  Kolo {kolo}/{KOL} | Aktuální počasí: {pocasi}")
    if random.randint(1, 10) < 8:
        print(f"🔮 Předpověď: {', '.join(predpoved)}")
        if pocasi_1 == "slunečno" and pocasi_4 in ["déšť", "silný déšť"]:
            print(random.choice(["We’re monitoring the weather, expect rain in 3 laps.", "Rain is coming in now, you should start thinking about wet tires soon.", "Rain intensity increasing, we expect full wet conditions in the next 3 laps."]))
            print(random.choice(["Copy that, adjusting my pace.", "Understood, I’m keeping an eye on it.","OK"]))
    else:
        fake = [vygeneruj_pocasi(pocasi) for _ in range(4)]
        print(f"🔮 Předpověď: {', '.join(fake)}")
        if fake[0] == "slunečno" and fake[3] in ["déšť", "silný déšť"]:
            print(random.choice(["We’re monitoring the weather, expect rain in 3 laps.", "Rain is coming in now, you should start thinking about wet tires soon.", "Rain intensity increasing, we expect full wet conditions in the next 3 laps."]))
            print(random.choice(["Copy that, adjusting my pace.", "Understood, I’m keeping an eye on it.","OK"]))
    return predpoved
def vygeneruj_pocasi(pocasi):
    if pocasi == "slunečno":
        pocasi = random.choice(["slunečno", "slunečno","slunečno","slunečno", "slunečno", "slunečno","slunečno","slunečno","slunečno", "slunečno","slunečno","slunečno", "slunečno", "slunečno","slunečno","slunečno","slunečno", "slunečno","slunečno","slunečno", "slunečno", "slunečno","slunečno","slunečno", "slunečno", "slunečno","slunečno","slunečno", "přechodné"])
    elif pocasi == "přechodné":
        pocasi = random.choice(["slunečno", "přechodné", "přechodné","přechodné","déšť"])
    elif pocasi == "déšť":
        pocasi = random.choice(["přechodné", "déšť", "déšť", "déšť", "déšť", "déšť", "déšť", "déšť", "déšť", "déšť", "silný déšť"])
    elif pocasi == "silný déšť":
        pocasi = random.choice(["déšť", "déšť", "silný déšť", "silný déšť", "silný déšť", "silný déšť", "silný déšť", "silný déšť", "silný déšť", "silný déšť"])
    pravdepodobnosti = {
        "slunečno": ["slunečno", "slunečno","slunečno","slunečno", "přechodné"],
        "přechodné": ["slunečno", "přechodné", "přechodné","přechodné","déšť"],
        "déšť": ["přechodné", "déšť", "déšť", "déšť","silný déšť"],
        "silný déšť": ["déšť", "déšť", "silný déšť", "silný déšť", "silný déšť"]
    }
    return pocasi
safety_car = False
def tabulka_jezdcu():
    for i, a in enumerate(auta[:6], 1):
        if a.dnf:
            status = POCET_AUT
        
        status = round(a.cas, 3)
        if i == 1:
            status_1 = round(status/60, 3)
            print(f"{i}. {a.jmeno} – {status} min")
            heloo = round(a.opotrebeni) * random.uniform(0.9, 1.1)
            heloo = round(heloo, 1)
            print(f"Počet boxů: {a.box} Únava: {heloo}%")
            status_1 = round(status, 3)
        else:
            distance = round(status - status_1, 3)
            print(f"{i}. {a.jmeno} + {distance} s")
            heloo = round(a.opotrebeni) * random.uniform(0.9, 1.1)
            heloo = round(heloo, 1)
            print(f"Počet boxů: {a.box} Únava: {heloo}%")
            status_1 = status
def reset_zavod():
    global kolo, casy_kol, safety_car, laps_rem, predpoved, pocasi
    kolo = 0
    casy_kol = []
    safety_car = False
    laps_rem = 0
    pocasi = "slunečno"
    predpoved = [vygeneruj_pocasi(pocasi)]
    for _ in range(3):
        predpoved.append(vygeneruj_pocasi(predpoved[-1]))
    for a in auta:
        a.cas = 0
        a.dnf = False
        a.opotrebeni = 0
        a.pozice = []
        a.defekt = False
        a.box = 0
        a.stinty = []
        a.last_stint_start = 0
    return kolo, casy_kol, safety_car, laps_rem, pocasi, predpoved, auta
def pit_hrac(training):
    volba = 1
    volba_2 = 1
    if hrac.dnf is False:
        print("Akce: [1] Pokračovat [2] Pit stop řidiče 1")
        volba = input("> ").strip()
        if volba == "2":
            print("Zvol pneu pro řidiče 1: [tvrdé / střední / měkké / mokré / inter]")
            strategie(KOL-kolo, CAS_S1, CAS_S2, CAS_S3, pneu, rychlost)                
            nova = input("> ").strip().lower()
            while nova not in PNEU_TYPY:
                nova = input("Neplatná volba. Zvol pneu: [tvrdé / střední / měkké / mokré / inter]\n> ")
                zkontroluj_pneu(nova)
            if nova in PNEU_TYPY:
                hrac.pit_stop(nova)
            else:
                print("Neplatná volba – pokračuješ.")
    if hrac_2.dnf is False:
        print("Akce: [1] Pokračovat [2] Pit stop řidiče 2")
        volba_2 = input("> ").strip()
        if volba_2 == "2":
            print("Zvol pneu pro řidiče 2: [tvrdé / střední / měkké / mokré / inter]")
            strategie(KOL-kolo, CAS_S1, CAS_S2, CAS_S3, pneu, rychlost)  
            nova = input("> ").strip().lower()
            while nova not in PNEU_TYPY:
                nova = input("Neplatná volba. Zvol pneu: [tvrdé / střední / měkké / mokré / inter]\n> ")
                zkontroluj_pneu(nova)
            if nova in PNEU_TYPY:
                hrac_2.pit_stop(nova)
            else:
                print("Neplatná volba – pokračuješ.")
    if hrac.dnf == True or hrac_2.dnf==True:
        if volba == "2" and volba_2 == "2":
            print(random.choice(["Box now, double stack. Maintain gap, all planned.",  "Box, box, double stack! Close gap, no mistakes!",  "Box this lap, we’re double stacking. Maintain delta, we’ve got margin.",  "Plan B, box now. You’ll be second in the stack, minimal delay expected.",  "Box this lap for double stack. First car in now, stand by for release.",  "Box this lap, we are double stacking. Pit crew is prepped for both."]))
            print( "Copy. Keeping gap, I’m right behind.",  "Understood. Staying tight.",  "Copy. I’m ready.",  "Confirmed. I’ll hit my marks.")
            hrac.cas += 3
            hrac_2.cas += 3
        elif volba_2 == "2" and volba != "2" or volba == "2" and volba_2 != "2":
            print(random.choice(["Box, box. Box this lap. Tyres ready, confirm entry.",  "Pit window is open. Box this lap for new tyres.",  "Box now. Hitting your marks is critical.",  "Box, box. Tyre temps look good — execute clean entry.",  "Pit this lap. We’re switching compound."]))
            print(random.choice([ "Copy. In this lap.",  "Understood. Coming in.",  "On my way in.", "Copy. Box, box",  "Copy, box this lap.", "Copy, confirmed."]))
def strategie(KOL, CAS_S1, CAS_S2, CAS_S3, pneu, rychlost):
    pocet_kol = KOL
    lap_time = (CAS_S1 + CAS_S2 + CAS_S3)/60
    if pneu == "střední":
        k_opotrebeni = [1.5,5,9,4.4,8.4]
    elif pneu == "měkké":
        k_opotrebeni = [2,7,12,5,9]       
    else:
        k_opotrebeni = [1,4,7,4,8]
    if rychlost == "střední":
        k_rychlost = [1,1.05,1.12,0.6,0.65]
    elif rychlost == "rychlé":
        k_rychlost = [1.05,1.12,1.15,0.65,0.7]
    else:
        k_rychlost = [0.95,1,1.05,0.55,0.6]
    vydrz_s = 65/k_opotrebeni[2]*k_rychlost[2]
    vydrz_m = 65/k_opotrebeni[1]*k_rychlost[1]
    vydrz_h =65/k_opotrebeni[0]*k_rychlost[0]
    vydrze = [vydrz_h, vydrz_m, vydrz_s]
    nazev = ["Hard", "Medium", "Soft"]
    box_time = (100/60)
#    cas = round((lap_time*KOL)/60*prych, 0)
    for i, stint in enumerate(vydrze, 0):
        if pocet_kol + 4 < vydrze[i] < pocet_kol +20:
            #zbytek = pocet_kol - vydrze[i]
            zbytek = vydrze[i] - pocet_kol
            prych = (vydrze[i] - zbytek)*k_rychlost[i]/pocet_kol
            #prych = (k_rychlost[i]*vydrze[i])/pocet_kol
            cas = round((lap_time*KOL)/prych, 2)

            print(f"Možná strategie - {round(stint, 0)} kol - {cas} minut - {nazev[i]}")

#    zbytek = vydrz1 + vydrz2 - kol
#    pocetkolvydrz2 = vydrz2 - zbytek 
#    prych = (k_rychlost[i]*vydrz1 + pocet_kolvydrz2*k_rychlost[0])/pocet_kol

    for i in range(len(vydrze)):
        if pocet_kol + 4 < vydrze[i] + vydrze[0] < pocet_kol +20:
            zbytek = vydrze[i] + vydrze[0]- pocet_kol
            pocetkolvydrz2 = vydrze[0] - zbytek
            prych = (k_rychlost[i]*vydrze[i] + pocetkolvydrz2*k_rychlost[0])/pocet_kol
            cas = round(((lap_time*KOL)/prych) + box_time, 2)
            if pocetkolvydrz2 > 0:
                print(f"Možná strategie - {round(vydrze[i] + vydrze[0],0)} kol - {cas} minut - {nazev[i]}, {nazev[0]}")
        if pocet_kol + 4 < vydrze[i] + vydrze[1]  < pocet_kol +20:
            zbytek = vydrze[i] + vydrze[1]- pocet_kol
            pocetkolvydrz2 = vydrze[1] - zbytek
            prych = (k_rychlost[i]*vydrze[i] + pocetkolvydrz2*k_rychlost[1])/pocet_kol
            cas = round(((lap_time*KOL)/prych) + box_time, 2)
            if pocetkolvydrz2 > 0:
                print(f"Možná strategie - {round(vydrze[i] + vydrze[1],0)} kol - {cas} minut - {nazev[i]}, {nazev[1]}")
        if pocet_kol + 4 < vydrze[i] + vydrze[2]  < pocet_kol +20:
            zbytek = vydrze[i]+ vydrze[2] - pocet_kol
            pocetkolvydrz2 = vydrze[2] - zbytek
            prych = (k_rychlost[i]*vydrze[i] + pocetkolvydrz2*k_rychlost[2])/pocet_kol
            cas = round(((lap_time*KOL)/prych) + box_time, 2)
            if pocetkolvydrz2 > 0:
                print(f"Možná strategie - {round(vydrze[i] + vydrze[2], 0)} kol - {cas} minut - {nazev[i]}, {nazev[2]}")
    for i in range(len(vydrze)):
        for j in range(len(vydrze)):
            if pocet_kol + 4 <vydrze[i] + vydrze[j] + vydrze[0]  < pocet_kol +20:
                zbytek = vydrze[i] + vydrze[j]  + vydrze[0] - pocet_kol
                pocetkolvydrz2 = vydrze[0] - zbytek
                prych = (k_rychlost[i]*vydrze[i] + k_rychlost[j]*vydrze[j]+ pocetkolvydrz2*k_rychlost[0])/pocet_kol
                cas = round((lap_time*KOL/prych) + box_time*2, 2)
                if pocetkolvydrz2 > 0:
                    print(f"Možná strategie - {round(vydrze[i] + vydrze[j] + vydrze[0], 0)} kol - {round(lap_time*(vydrze[i] + vydrze[j]+vydrze[0]) + box_time*2, 0)} minut - {nazev[i]}, {nazev[j]}, {nazev[0]}")
            if pocet_kol + 4 <vydrze[i] + vydrze[j] + vydrze[1]  < pocet_kol +20:
                zbytek = vydrze[i] + vydrze[j]  + vydrze[1]- pocet_kol
                pocetkolvydrz2 = vydrze[1] - zbytek
                prych = (k_rychlost[i]*vydrze[i] + k_rychlost[j]*vydrze[j]+ pocetkolvydrz2*k_rychlost[1])/pocet_kol
                cas = round(((lap_time*KOL)/prych) + box_time*2, 2)
                if pocetkolvydrz2 > 0:
                    print(f"Možná strategie - {round(vydrze[i] + vydrze[j] + vydrze[1], 0)} kol - {round(lap_time*(vydrze[i] + vydrze[j]+vydrze[1]) + box_time*2, 0)} minut - {nazev[i]}, {nazev[j]}, {nazev[1]}")
            if pocet_kol + 4 <vydrze[i] + vydrze[j] + vydrze[2]  < pocet_kol +20:
                zbytek = vydrze[i] + vydrze[j] + vydrze[2]- pocet_kol
                pocetkolvydrz2 = vydrze[2] - zbytek
                prych = (k_rychlost[i]*vydrze[i] + k_rychlost[j]*vydrze[j]+ pocetkolvydrz2*k_rychlost[2])/pocet_kol
                cas =  round(((lap_time*KOL)/prych) + box_time*2, 2)
                if pocetkolvydrz2 > 0:
                    print(f"Možná strategie - {round(vydrze[i] + vydrze[j] + vydrze[2], 0)} kol - {cas} minut - {nazev[i]}, {nazev[j]}, {nazev[2]}")
ridici_mmr2 = [
    "Noah Blake", "Felipe Sandoval", "Luca Moretti", "Brian Chen", "Adam Novak", "Pierre Gauthier",
    "Viktor Orlov", "Daisuke Tanaka", "Elias Müller", "Jordan Evans", "Diego Ramirez", "Anton Petrov",
    "Kenji Nakamura", "Nicolas Dubois", "Thomas Fischer", "Miguel Lopez", "Alexei Sokolov", "Ethan Zhang",
    "Leo Harrington", "Marco Silva"
]

# Class to represent each driver
class ridicmmr2:
    def __init__(self, jmeno, zkusenost):
        self.jmeno = jmeno
        self.zkusenost = zkusenost
        self.cas = 0.0

# Function to simulate the season
def simuluj_sezonu_MMR2(jezdci):
    for driver in jezdci:
        for zavod in range(12):  # For 12 races
            for lap in range(50):  # For 50 laps per race
                driver.cas += driver.zkusenost * random.uniform(0.97, 1.02)  # Add time based on experience
    
    # Sort drivers by their time (lower is better)
    mmr2_serazene = sorted(jezdci, key=lambda x: x.cas)
    
    # Best driver is the one with the lowest time
    best = mmr2_serazene[0]
    # Worst driver is the one with the highest time
    worst = mmr2_serazene[-1]  
    
    return best, worst

# Create a list of drivers with random experience
seznam_ridicu_mmr2 = [ridicmmr2(jmeno, random.uniform(0.95, 1.05)) for jmeno in ridici_mmr2]

# Run the simulation
best, worst = simuluj_sezonu_MMR2(seznam_ridicu_mmr2)
#for driver in ridici_mmr2:
#    ridicmmr2(driver,random.uniform(0.95, 1))
class Auto:
    def __init__(self, jmeno, zkusenost, je_hrac=False):
        self.jmeno = jmeno
        self.box = 0
        self.stinty = []  # seznam úseků závodu (start_time, délka, pneu)
        self.pozice = []
        self.last_stint_start = 0  # čas začátku aktuálního stintu
        self.je_hrac = je_hrac
        self.pneu = random.choice(["střední", "tvrdé"])
        self.opotrebeni = 0.0
        self.zkusenosti = zkusenost
        self.cas = 0.0
        self.body = 0
        self.drs = False
        self.team = None
        self.dnf = False
        self.defekt = False

    def efektivita_pneu(self, pocasi):
        # Zajisti, že pneumatika je string
        if isinstance(self.pneu, list):
            self.pneu = self.pneu[0]

        base = PNEU_TYPY[self.pneu]["rychlost"]

        if pocasi in ["déšť", "silný déšť"] and self.pneu not in ["mokré", "inter"]:
            base *= 0.3
        if pocasi == "silný déšť" and self.pneu not in ["mokré", "inter"]:
            base *= 0.2
        if pocasi == "slunečno" and self.pneu in ["mokré", "inter"]:
            base *= 0.5

        return base


    def simuluj_kolo(self, pocasi, training):
        global safety_car
        if self.dnf:
            return
        
        if self.opotrebeni >= 100:
            print(f"{self.jmeno} – extrémní opotřebení! ❌")
            self.dnf = True
            return

        if self.defekt:
            print(f"{self.jmeno} – defekt! ❌")
            safety_car = True
            return safety_car
        if self.opotrebeni > 80 and random.random() < 0.55:
            print(f"{self.jmeno} – defekt! ❌")
            self.defekt = True
            self.dnf = True
            safety_car = True
            return safety_car

        rychlost = self.efektivita_pneu(pocasi)
        s1 = CAS_S1*random.uniform(0.98, 1.02)*self.zkusenosti*self.team.zkusenost/ rychlost
        s2 = CAS_S2*random.uniform(0.98, 1.02)*self.zkusenosti*self.team.zkusenost/ rychlost
        s3 = CAS_S3*random.uniform(0.98, 1.03)*self.zkusenosti*self.team.zkusenost/ rychlost
        if safety_car:
            s1 = s1*2.5
            s2 = s2*2.5
            s3 = s3*2.5
        if self.drs:
            s1 = s1 - random.uniform(0.2, 0.3)
            s2 = s2 - random.uniform(0.2, 0.3)
            s3 = s3 - random.uniform(0.2, 0.3)
        if training == "2":
            s1 = s1 - random.uniform(0.1, 0.3)
            s2 = s2 - random.uniform(0.1, 0.3)
            s3 = s3 - random.uniform(0.1, 0.3)
        if pocasi in ["slunečno"] and self.pneu not in ["měkké", "střední", "tvrdé"]:
            s1 = s1*3
            s2 = s2*3
            s3 = s3*3
        if pocasi in ["déšť", "silný déšť"] and self.pneu not in ["mokré" , "inter"]:
            s1 = s1*3
            s2 = s2*3
            s3 = s3*3
        lap_time = s1 + s2 + s3
        casy_kol.append((lap_time, self.jmeno, self.team, s1, s2, s3))
        self.cas = self.cas + self.opotrebeni/10 + lap_time

            
        #global auta  # použijeme globální seznam aut
        #auta.sort(key=lambda x: (x.dnf, x.cas))  # seřadíme auta podle času
        index = auta.index(self)

        if index > 0:
            auto_pred = auta[index - 1]
            if not auto_pred.dnf:
                rozdil = self.cas - auto_pred.cas  # o kolik je pomalejší
                if rozdil < 1.5:  # je blízk
                    obrana = random.uniform(0.65, 0.95)  # obranná dovednost soupeře
                    sance = max(0.1, 1.5 - rozdil) * 0.4
                    if random.random() > obrana or random.random() < sance:
                        # ✅ Předjetí úspěšné – není třeba nic dělat
                        pass
                    else:
                        #❌Předjetí nevyšlo → "zůstaneš za ním"
                            # DOSTANEŠ JEHO ČAS + malý rozdíl, abys byl těsně za ním
                        self.cas = auto_pred.cas + random.uniform(0.05, 0.25)
        self.opotrebeni += PNEU_TYPY[self.pneu]["opotřebení"]
        prirustek = PNEU_TYPY[self.pneu]["opotřebení"] * random.uniform(0, 0.4)
        self.opotrebeni += prirustek
    def pit_stop(self, nova_pneu):
    # Ulož předchozí stint
        if not self.dnf:
            self.stinty.append((self.last_stint_start, self.cas - self.last_stint_start, self.pneu))
        if safety_car == True:
            self.cas += 50
        else: 
            self.cas += 100
        self.box += 1
        self.predchozi_pneu = self.pneu
        self.pneu = nova_pneu
        self.opotrebeni = 0
        self.last_stint_start = self.cas  # nový stint začíná od nového času

    def rozhodni_ai(self, pocasi, kol, max_kol, predpoved):
        if self.dnf:
            return None, False
        pozice = sorted(auta, key=lambda x: (x.dnf, x.cas)).index(self) + 1
        unava = self.opotrebeni
        zustava = max_kol - kol
        idealni = self.vhodne_pneu(predpoved[0])
        ideal_2 = self.vhodne_pneu(predpoved[2])

        self.pit = False
        if self.pneu not in idealni and self.pneu not in ideal_2 and zustava > 5:
            self.pit = True
        elif unava >= 80 and random.random() < 0.95:
            self.pit = True
        elif unava > 90 or (self.pneu not in idealni and random.random() > 0.9):
            self.pit = True
        elif safety_car and self.opotrebeni > 70 and zustava > 5:
            self.pit = True
        if predpoved[3] == "přechodné":
            idealni = "měkké"
        elif predpoved[0] in ["déšť", "silný déšť"] and KOL - kolo < 70/k_opotrebeni[3] and predpoved[2] == predpoved[0]:
            idealni = "mokré"
        elif predpoved[0] in ["déšť", "silný déšť"] and KOL - kolo < 70/k_opotrebeni[4] and predpoved[2] == predpoved[0]:
            idealni = "inter"
        elif predpoved[0] == "slunečno" and KOL - kolo < 70/k_opotrebeni[0] and predpoved[2] == predpoved[0]:
            idealni = "tvrdé"
        elif predpoved[0] == "slunečno" and KOL- kolo < 70/k_opotrebeni[1] and predpoved[2] == predpoved[0]:
            idealni = "střední"
        elif predpoved[0] == "slunečno" and KOL - kolo < 70/k_opotrebeni[2] and predpoved[2] == predpoved[0]:
            idealni = "měkké"
        elif predpoved[0] in ["přechodné", "slunečno", "déšť"] and predpoved[3] in ["déšť", "silný déšť"] or predpoved[0] in ["déšť", "silný déšť"] and predpoved[2] == predpoved[0] or predpoved[2] in ["déšť", "silný déšť"]:
            idealni = random.choice(["mokré" ,"mokré" , "inter"])
        elif predpoved[0] == "slunečno" and predpoved[2] == predpoved[0]:
            idealni = random.choice(["měkké" , "střední", "tvrdé", "střední", "tvrdé"])
        elif predpoved[0] in ["přechodné", "slunečno", "déšť"] and predpoved[3] in ["slunečno"]:
            idealni = random.choice(["měkké" , "střední", "tvrdé", "střední", "tvrdé"])
        return idealni if self.pit else None
    def hrac_info(self):
        if self.dnf == False:
            if safety_car == True:
                print(random.choice(["Still safety car", "Still spinning slowly lap by lap."]))
                if self.opotrebeni > 60:
                    print(random.choice(["Why didn’t we pit? We’ve just thrown away the race.", "I had no grip even before the safety car!", "Come on! These tyres are dead — what are we doing?!", "Are we sure about staying out? Tyres are cooked."]))
            print(f"\n🚗 Tvé auto {self.jmeno}")
            poradi = [a.jmeno for a in auta if not a.dnf]  # Move this line here            
            if driver_1 == self.jmeno:
                pozice = poradi.index(driver_1) + 1 if driver_1 in poradi else POCET_AUT
                print(f"Řidič 1 - {hrac.jmeno}")
            else:
                pozice = poradi.index(driver_2) + 1 if driver_2 in poradi else  POCET_AUT
                print(f"Řidič 2 - {hrac_2.jmeno}")
            print(f"\n📊 Pořadí: {pozice}. místo z {len(poradi)}")
            fake_o = int(self.opotrebeni) - random.uniform(-4, 4)
            fake_o = int(fake_o)
            if fake_o < 0:
                fake_o = 0
            print(f"🛞  Pneumatiky: {self.pneu} | Opotřebení: {fake_o}%")
            index = auta.index(self)
            rozdil = 0
            rozdil_2 = 0
            if 0 < index < len(auta):
                auto_pred = auta[index - 1]
                if index + 1 < len(auta):
                    auto_za = auta[index + 1]
                else:
                    auto_za = auta[index]
                rozdil = self.cas - auto_pred.cas    
                rozdil_2 = auto_za.cas - self.cas
                print(f"Delta před: {round(rozdil, 3)}s ({auto_pred.team.nazev})| Delta za: {round(rozdil_2, 3)}s ({auto_za.team.nazev})")
            elif index == 0:
                auto_za = auta[index + 1]
                rozdil_2 = auto_za.cas - self.cas
                print(f"Delta za: {round(rozdil_2, 3)}s ({auto_za.team.nazev})")
            else:
                auto_pred = auta[index - 1]
                rozdil = self.cas - auto_pred.cas
                print(f"Delta před: {round(rozdil, 3)}s ({auto_pred.team.nazev})")
            if self.opotrebeni >= 70:
                print(random.choice(["The tyres are pretty done now.", "I don´t know what are you doing there, but I am boxing. Or at least I wish.", "The tyres are ***!", "Please, take me out from this hell." "Please box, please."]))
        return 
    def drss(self):
        for i in range(1, len(auta)):  # Začínáme od 1, abychom měli i-1 pro předchozí auto
    # Čas aktuálního a předchozího auta
            current_time = self.cas  # Čas aktuálního auta
            previous_time = auta[i-1].cas  # Předpokládám, že auta mají atribut 'cas'

    # Vypočítáme rozdíl mezi časy
            time_difference = current_time - previous_time

    # Pokud je rozdíl menší než 1 sekunda, aktivujeme DRS
            if time_difference < 1:
                self.drs = True
        return self.cas, self.drs

    def simuluj_ai(self, training):
        if self.je_hrac == False:
            nova_pneu = self.rozhodni_ai(pocasi, kolo, KOL, predpoved)
            if nova_pneu:
                self.pit_stop(nova_pneu)

        self.simuluj_kolo(pocasi, training)
    def vhodne_pneu(self, pocasi):
        if pocasi in ["silný déšť", "déšť"]:
                return ["mokré", "inter"]
        elif pocasi == "přechodné":
            return ["mokré", "inter", "měkké", "střední", "tvrdé"]
        else:
            return ["měkké", "střední", "tvrdé"]
    def vypocitej_body_jezdec(self, poradi):
        if self.dnf == False:
            pozice = poradi.index(self.jmeno) + 1
            if pozice == 1:
                self.body += 50
            elif pozice == 2:
                self.body += 42
            elif pozice == 3:
                self.body += 36
            elif pozice == 4:
                self.body += 32
            elif pozice == 5:
                self.body += 28
            elif pozice == 6:
                self.body += 25
            elif pozice == 7:
                self.body += 22
            elif pozice == 8:
                self.body += 19
            elif pozice == 9:
                self.body += 16
            elif pozice == 10:
                self.body += 14
            elif pozice == 11:
                self.body += 12
            elif pozice == 12:
                self.body += 10
            elif pozice == 13:
                self.body += 8
            elif pozice == 14:
                self.body += 6
            elif pozice == 15:
                self.body += 5
            elif pozice == 16:
                self.body += 4
            elif pozice == 17:
                self.body += 3
            elif pozice == 18:
                self.body += 2
            elif pozice == 19:
                self.body += 1
class Team:
    def __init__(self, nazev, zkusenost):
        self.nazev = nazev
        self.zkusenost = zkusenost
        self.jezdci = []  # seznam instancí třídy Auto
        self.body = 0     # body celého týmu

    def pridej_jezdce(self, auto):
        self.jezdci.append(auto)
        auto.team = self

    def vypocitej_body(self, poradi):
        """
        Po závodě zavolej na každý tým a předej aktuální pořadí jezdců.
        Např. poradi = [jmeno1, jmeno2, ...]
        """
        for jezdec in self.jezdci:
            if jezdec.jmeno in poradi:
                pozice = poradi.index(jezdec.jmeno) + 1
                if pozice == 1:
                    self.body += 50
                elif pozice == 2:
                    self.body += 42
                elif pozice == 3:
                    self.body += 36
                elif pozice == 4:
                    self.body += 32
                elif pozice == 5:
                    self.body += 	28
                elif pozice == 6:
                    self.body += 25
                elif pozice == 7:
                    self.body += 22
                elif pozice == 8:
                    self.body += 19
                elif pozice == 9:
                    self.body += 16
                elif pozice == 10:
                    self.body += 14
                elif pozice == 11:
                    self.body += 12
                elif pozice == 12:
                    self.body += 10
                elif pozice == 13:
                    self.body += 8
                elif pozice == 14:
                    self.body += 6
                elif pozice == 15:
                    self.body += 5
                elif pozice == 16:
                    self.body += 4
                elif pozice == 17:
                    self.body += 3
                elif pozice == 18:
                    self.body += 2
                elif pozice == 19:
                    self.body += 1
drivers = ["Lightning McQueen","Francesco Bernoulli","Ghost rider","Lando Norris", "Alain Prost", "Niki Lauda", "James Hunt",  "Robert Kubica","Jiří Král","Števo Eisele","Oscar Piastri", "Charles Leclerc", "Lewis Hamilton", "George Russel", "Andrea Kimi Antoneli", "Lance Stroll", "Fernando Alonso", "Mick Schumacher", "Michael Schumacher", "Sergio Perez", "Ayrton Senna", "Jaquez Villenueve", "Valterri Bottas", "Guan Zhou", "Yuki Tsunoda", "Kimi Raikonen"]
x = 0
auta = []
for driver in drivers:
    auta.append(Auto(driver,random.uniform(0.9, 1)))
hrac = Auto(driver_1, random.uniform(0.9, 1), je_hrac=True)
auta.append(hrac)

hrac_2 = Auto(driver_2, random.uniform(0.95, 1), je_hrac=True)
auta.append(hrac_2)
teams = []
# Vytvoření týmů a přiřazení jezdců
def vytvor_team(team_player, hrac_1, hrac_2, teams, zkusenost):
    tym = Team(team_player, zkusenost)
    tym.pridej_jezdce(hrac_1)
    tym.pridej_jezdce(hrac_2)
    teams.append(tym)
    return tym
vytvor_team(team_player, hrac, hrac_2, teams, random.uniform(0.85, 1))
vytvor_team("Scuderia Python", auta[0], auta[1], teams, random.uniform(0.8, 0.9))
vytvor_team("Racing 404",auta[2],auta[3], teams, random.uniform(0.95, 1))
vytvor_team("Formula 1.0 racing team",auta[4],auta[5], teams, random.uniform(0.9, 1))
vytvor_team("Microsoft PitStop Protocol racing team",auta[6],auta[7], teams, random.uniform(0.8, 1))
vytvor_team("Intel QWERTY GP",auta[8],auta[9], teams, random.uniform(0.95, 1))
vytvor_team("Underbyte Nvidia GP",auta[10],auta[11], teams, random.uniform(0.8, 0.85))
vytvor_team("JavaScript Racing team",auta[12],auta[13], teams, random.uniform(0.8, 0.85))
vytvor_team("Java motors",auta[14],auta[15], teams, random.uniform(0.8, 1))
vytvor_team("Jawa Surenate Linux racing team",auta[16],auta[17], teams, random.uniform(0.8, 1))
vytvor_team("AMD Assemblyte GP",auta[18],auta[19], teams, random.uniform(0.8, 1))
vytvor_team("VS racing 22",auta[20],auta[21], teams, random.uniform(0.8, 1))
vytvor_team("PyCharm motors",auta[22],auta[23], teams, random.uniform(0.8, 1))
vytvor_team("Pixel motors",auta[24],auta[25], teams, random.uniform(0.8, 1))
sampionat = ["AWS Grand Prix de Espana", "AirBNB Prague GP", "eBay Skyline Turkey GP","Java airlines Monza IBM Italy GP","HP Bulgarian GP","Python circuit Bahamas", "Ostrava Apple GP", "META China Grand Prix", "Sony Varsava Grand Prix", "LG TV Grand Prix du France", "Huawei GP SPA"]
b = 1
lenght = int(input("Jaká je délka šampionátu: "))
hi = len(sampionat) - lenght
if hi > 0:
    for _ in range(hi):
        sampionat.pop(random.randint(0, len(sampionat)-1))
while len(nazvy_jezdcu) > 1:
    b = 0
    for zavod in sampionat:
        kolo = 0
        if zavod == "Huawei GP SPA":
            pneu = "měkké"
            rychlost = "rychlé"
            CAS_S1 = 22
            CAS_S2 = 25
            CAS_S3 = 18
            KOL = 70
        if zavod == "LG TV Grand Prix du France":
            pneu = "měkké"
            rychlost = "rychlé"
            CAS_S1 = 26
            CAS_S2 = 19
            CAS_S3 = 22
            KOL = 74
        if zavod == "Sony Varsava Grand Prix":
            pneu = "tvrdé"
            rychlost = "střední"
            CAS_S1 = 35
            CAS_S2 = 18
            CAS_S3 = 24
            KOL = 62
        if zavod == "META China Grand Prix":
            pneu = "střední"
            rychlost = "pomalé"
            CAS_S1 = 25
            CAS_S2 = 34
            CAS_S3 = 30
            KOL = 56
        if zavod == "Ostrava Apple GP":
            pneu = "měkké"
            rychlost = "rychlé"
            CAS_S1 = 20
            CAS_S2 = 26
            CAS_S3 = 18
            KOL = 67
        if zavod == "Python circuit Bahamas":
            pneu = "tvrdé"
            rychlost = "střední"
            CAS_S1 = 25
            CAS_S2 = 23
            CAS_S3 = 38
            KOL = 72  
        if zavod == "HP Bulgarian GP":
            pneu = "střední"
            rychlost = "střední"
            CAS_S1 = 23
            CAS_S2 = 29
            CAS_S3 = 20
            KOL = 60
        if zavod == "AWS Grand Prix de Espana":
            pneu = "střední"
            rychlost = "rychlé"
            CAS_S1 = 26
            CAS_S2 = 31
            CAS_S3 = 12
            KOL = 51
        if zavod == "AirBNB Prague GP":
            pneu = "měkké"
            rychlost = "rychlé"
            CAS_S1 = 20
            CAS_S2 = 33
            CAS_S3 = 40
            KOL = 42
        if zavod == "eBay Skyline Turkey GP":
            pneu = "tvrdé"
            rychlost = "pomalé"
            CAS_S1 = 27
            CAS_S2 = 24
            CAS_S3 = 36
            KOL = 49
        if zavod == "Java airlines Monza IBM Italy GP":
            pneu = "měkké"
            rychlost = "rychlé"
            CAS_S1 = 30
            CAS_S2 = 16
            CAS_S3 = 18
            KOL = 70
        print(f"Jede se závod {zavod} {b}/{len(sampionat)}")
        print(f"Tato ať je charakteristická tím, že má {pneu} pneu a {rychlost} tempo. Má {KOL} kol")
        strategie(KOL, CAS_S1, CAS_S2, CAS_S3, pneu, rychlost)

        if pneu == "střední":
            k_opotrebeni = [1.5,5,9,4.4,8.4]
        elif pneu == "měkké":
            k_opotrebeni = [2,7,12,5,9]       
        else:
            k_opotrebeni = [1,4,7,4,8]
        if rychlost == "střední":
            k_rychlost = [1,1.05,1.12,0.6,0.65]
        elif rychlost == "rychlé":
            k_rychlost = [1.05,1.12,1.15,0.65,0.7]
        else:
            k_rychlost = [0.95,1,1.05,0.55,0.6]
        PNEU_TYPY = {
        "tvrdé": {"opotřebení": k_opotrebeni[0], "rychlost": k_rychlost[0]},
        "střední": {"opotřebení": k_opotrebeni[1], "rychlost": k_rychlost[1]},
        "měkké": {"opotřebení": k_opotrebeni[2], "rychlost": k_rychlost[2]},
        "mokré": {"opotřebení": k_opotrebeni[3], "rychlost": k_rychlost[3]},
        "inter": {"opotřebení": k_opotrebeni[4], "rychlost": k_rychlost[4]},
        }
        pocasi = "slunečno"
        pocasi_1 = vygeneruj_pocasi(pocasi)
        pocasi_2 = vygeneruj_pocasi(pocasi_1)
        pocasi_3 = vygeneruj_pocasi(pocasi_2)
        pocasi_4 = vygeneruj_pocasi(pocasi_3)
        predpoved = [pocasi_1, pocasi_2, pocasi_3, pocasi_4]
        for x in predpoved:
            print (f"Počasí: 🌤️ ☁️  {x}")
        for auto in auta:
            auto.pneu = random.choice(["tvrdé", "střední"])
        hrac.pneu = input("Zvol pneu pro jezdce 1: [tvrdé / střední / měkké / mokré / inter]\n> ")
        while hrac.pneu not in PNEU_TYPY:
            hrac.pneu = input("Neplatná volba. Zvol pneu: [tvrdé / střední / měkké / mokré / inter ]\n> ")
            zkontroluj_pneu(hrac.pneu)
            if hrac.pneu == "exit":
                continue
        hrac_2.pneu = input("Zvol pneu pro jezdce 2: [tvrdé / střední / měkké / mokré / inter]\n> ")
        while hrac_2.pneu not in PNEU_TYPY:
            hrac_2.pneu = input("Neplatná volba. Zvol pneu: [tvrdé / střední / měkké / mokré / inter]\n> ")
            zkontroluj_pneu(hrac.pneu)
            if hrac.pneu == "exit":
                continue
        simulace = []
        #Tréninky
        training = input("Akce: Chceš trénink na výdrž pneu [1], rychlost [2] nebo kvalikaci [3]: ")
        #Kvalifikace
        for auto in auta:
            sim_cas = CAS_S1 * random.uniform(0.9, 1.1) + CAS_S2 * random.uniform(0.9, 1.1) + CAS_S3 * random.uniform(0.9, 1.1)
            if auto.je_hrac and training == "3":
                sim_cas = sim_cas/1.5 
            simulace.append((auto, sim_cas))
        simulace.sort(key=lambda x: x[1])
        for i, (auto, sim_cas) in enumerate(simulace):
            penalizovany_cas =  1 * i
            auto.cas += penalizovany_cas
        ######################################################################################################################################################################
        while kolo <= KOL:
            if kolo == KOL:
                print("Last lap. Push push.")
            info()
            for auto in auta:
            # sem patří tvůj kód

                if pocasi == "slunečno":
                    if random.randint(1, 5000) == 1:
                        if kolo >= 3:
                            auto.dnf = True
                            safety_car = True
                            laps_rem = random.randint(3,6)
                            print(f"{auto.jmeno} obdrželo DNF")
                            print(random.choice([
                        "Radio: Crash ahead, safety car is out!",
                        "Radio: We’ve got yellow flags – full course yellow!",
                        "Radio: Big crash, bring the delta in check.",
                        "Radio: Watch the debris – SC deployed!"
                    ]))
                else:
                    if random.randint(1, 1000) == 1:
                        if kolo >= 3:
                            auto.dnf = True
                            safety_car = True
                            laps_rem = random.randint(3,6)
                            print(f"{auto.jmeno} obdrželo DNF")
                            print(random.choice([
                        "Radio: Crash ahead, safety car is out!",
                        "Radio: We’ve got yellow flags – full course yellow!",
                        "Radio: Big crash, bring the delta in check.",
                        "Radio: Watch the debris – SC deployed!"
                    ]))
            if safety_car == True:
                laps_rem -=1
            if laps_rem == 0:
                safety_car = False
            auta.sort(key=lambda x: (x.dnf, x.cas))
            for auto in auta:
            # sem patří tvůj kód

                if auto.je_hrac:
                    auto.hrac_info()
                    #pozice = poradi.index(driver_1) + 1 if driver_1 in poradi else POCET_AUT
                    #d_2 = poradi.index(driver_2) + 1 if driver_2 in poradi else  POCET_AUT
            auta.sort(key=lambda x: (x.dnf, x.cas))
            auta = [a for a in auta] 

            auto.drss()

            for i, auto in enumerate(auta):
                auta = [a for a in auta] 

                if i > 0:
                    auto_pred = auta[i - 1]
                    rozdil = auto.cas - auto_pred.cas
                    if rozdil < 1.5 and rozdil > 0:
                        obrana = random.uniform(0.6, 0.95)
                        sance_predjeti = max(0.1, 1.5 - rozdil) * 0.4  # např. až 60% šance
                        if auto.drs == True:
                            sance_predjeti += 0.3
                        if obrana  < sance_predjeti:
                            auto.opotrebeni += 3
                            auta[i], auta[i - 1] = auta[i - 1], auta[i]
            auta.sort(key=lambda x: (x.dnf, x.cas))

            pit_hrac(training)
            auta.sort(key=lambda x: (x.dnf, x.cas))
            timecar = 0
            poradi = [a.jmeno for a in auta if not a.dnf]  # Move this line here
            pozice = poradi.index(driver_1) + 1 if driver_1 in poradi else POCET_AUT
            pozice_2 = poradi.index(driver_2) + 1 if driver_2 in poradi else POCET_AUT


            #poradi = [a.jmeno for a in auta if not a.dnf]

            #pozice = poradi.index(driver_1) + 1 if driver_1 in poradi else "DNF"
            print(f"\n📊 Pořadí {driver_1}: {pozice}. místo z {len(poradi)}")
            #pozice_2 = poradi.index(driver_2) + 1 if driver_2 in poradi else "DNF"
            print(f"\n📊 Pořadí {driver_2}: {pozice_2}. místo z {len(poradi)}")
            tabulka_jezdcu()
            for auto in auta:
                auto.simuluj_ai(training)
            boxy_po_teamu = {}
            for a in auta:
                if not a.je_hrac and a.pit:  # pokud AI jezdec plánuje pit
                    team = a.team
                    if team not in boxy_po_teamu:
                        boxy_po_teamu[team] = 0
                    boxy_po_teamu[team] += 1

            for team, pocet in boxy_po_teamu.items():
                if pocet >= 2:
                    print(f"{team.nazev} jde do double stacku.")
                    for a in auta:
                        if a.team == team and a.pit:
                            pozice = poradi.index(a) + 1 if a in poradi else POCET_AUT
                            a.cas += 50
            boxy_po_teamu.clear()
            auta.sort(key=lambda x: (x.dnf, x.cas))
            poradi = [a for a in auta if not a.dnf]  # Move this line here
            for a in auta:
                if a in poradi:  # Pokud je auto v seznamu poradi
                    pozice = poradi.index(a) + 1  # Pozice v seznamu (index + 1)
                else:
                    pozice = POCET_AUT  # Pokud není auto v seznamu, nastaví se na POCET_AUT
                a.pozice.append(pozice)  # Přidání pozice do seznamu pozic auta

            # posun počasí
            pocasi = predpoved.pop(0)
            pocasi_1 = predpoved[0]
            pocasi_2 = predpoved[1]
            pocasi_3 = predpoved[2]
            predpoved.append(vygeneruj_pocasi(pocasi_3))
            pocasi_4 = predpoved[3]
            kolo += 1
        print("\n🏁 KONEC ZÁVODU!")
        b +=1
        casy_kol.sort()
        print(f"{casy_kol[0][1]} ({casy_kol[0][2].nazev}) zajel nejrychlejší čas {round(casy_kol[0][0], 3)}")
        for a in auta:
            a.zkusenosti -= 0.01
        sektor1 = min(casy_kol, key=lambda x: x[3])
        sektor2 = min(casy_kol, key=lambda x: x[4])
        sektor3 = min(casy_kol, key=lambda x: x[5])

        print(f"{sektor1[1]} ({sektor1[2].nazev}) zajel nejrychlejší sektor 1 {round(sektor1[3], 3)}")
        print(f"{sektor2[1]} ({sektor2[2].nazev}) zajel nejrychlejší sektor 2 {round(sektor2[4], 3)}")
        print(f"{sektor3[1]} ({sektor3[2].nazev}) zajel nejrychlejší sektor 3 {round(sektor3[5], 3)}")

        casy_kol[0][2].body += 2
        for d in range(len(casy_kol)):
            if casy_kol[d][1] == hrac.jmeno:
                print(f"{casy_kol[d][1]} ({casy_kol[d][2].nazev}) zajel svůj nejrychlejší čas {round(casy_kol[d][0], 3)}, sektor 1 {round(casy_kol[d][3], 3)}, sektor 2 {round(casy_kol[d][4], 3)}, sektor 3 {round(casy_kol[d][5], 3)}")
                break
        for d in range(len(casy_kol)):
            if casy_kol[d][1] == hrac_2.jmeno:
                print(f"{casy_kol[d][1]} ({casy_kol[d][2].nazev}) zajel svůj nejrychlejší čas {round(casy_kol[d][0], 3)}, sektor 1 {round(casy_kol[d][3], 3)}, sektor 2 {round(casy_kol[d][4], 3)}, sektor 3 {round(casy_kol[d][5], 3)}")
                break
        #time.sleep(6)
        #
        ## Uložení výsledků do CSV
        #with open("vysledky_zavodu.csv", "w", newline="", encoding="utf-8") as file:
        #    writer = csv.writer(file)
        #    writer.writerow(["Pořadí", "Jezdec", "Čas (min)", "Počet boxů", "DNF", "Stinty"])
        #    for i, a in enumerate(auta, 1):
        #        cas = round(a.cas / 60, 2) if not a.dnf else "DNF"
        #        stint_popis = "; ".join(
        #            [f"{round(start/60, 1)}–{round((start+doba)/60, 1)}min: {typ}" for start, doba, typ in a.stinty]
        #        )
        #        writer.writerow([i, a.jmeno, cas, a.box, a.dnf, stint_popis])


        # Ujistíme se, že poradi je stále list jezdců bez DNF
        poradi = [a.jmeno for a in auta if not a.dnf]
        for driver in auta:
            driver.vypocitej_body_jezdec(poradi)
        for team in teams:
            team.vypocitej_body(poradi)
        body = sorted(teams, key=lambda x: (x.body))
        # Bezpečný výpočet pozic
        pozice_1 = poradi.index(driver_1) + 1 if driver_1 in poradi else "DNF"
        pozice_2 = poradi.index(driver_2) + 1 if driver_2 in poradi else "DNF"
        print(f"\n🏁 Finální pozice:")
        print(f"{driver_1}: {pozice_1}. místo")
        print(f"{driver_2}: {pozice_2}. místo")
        #time.sleep(4)
        # Výsledková listina
        auta.sort(key=lambda x: (x.dnf, x.cas))
        for i, a in enumerate(auta, 1):
            stav = "DNF" if a.dnf else f"{round(a.cas, 2)}s"
            print(f"{i}. {a.jmeno} ({a.team.nazev}) {a.body} bodů")
        teams.sort(key=lambda team: team.body, reverse=True)
        #time.sleep(8)
        for i, team in enumerate(teams,1):
            print (f"{i}.{team.nazev} {team.body} bodů")
        #time.sleep(8)
        # 📊 Grafické znázornění výsledků závodu
        jmena = [a.jmeno for a in auta]
        casy = [a.cas/60 if not a.dnf else None for a in auta]
        # Barvy podle pneu
        barvy = []
        barvy_grafy()
        # Zaznamenání posledního stintu pro každé auto
        for a in auta:
            if not a.dnf:
                a.stinty.append((a.last_stint_start, a.cas - a.last_stint_start, a.pneu))
        # Zobrazení grafu
        plt.figure(figsize=(12, 6))
        plt.barh(jmena[::-1], [c if c is not None else 0 for c in casy][::-1], color=barvy[::-1])
        plt.xlabel("Čas (min)")
        plt.ylabel("Jezdci")
        plt.title("🏁 Výsledky závodu – nižší čas = lepší")
        plt.tight_layout()
        plt.show()
        plt.figure(figsize=(10, 6))
        for a in auta:
            plt.plot(range(1, len(a.pozice) + 1), a.pozice, label=a.jmeno)

        plt.gca().invert_yaxis()  # protože 1. místo je nejlepší
        plt.xlabel("Kolo")
        plt.ylabel("Pozice")
        plt.title("Vývoj pozic během závodu")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        plt.figure(figsize=(10, 6))
        players = [hrac, hrac_2]
        for a in players:
            plt.plot(range(len(a.pozice)), a.pozice, label=a.jmeno)

        plt.gca().invert_yaxis()  # protože 1. místo je nejlepší
        plt.xlabel("Kolo")
        plt.ylabel("Pozice")
        plt.title("Vývoj pozic během závodu")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        reset_zavod()
    print("\n🏁 Finální pořadí šampionátu jezdců:")
    #best, worst = simuluj_sezonu_MMR2(hi)
    for d in seznam_ridicu_mmr2:
        d.zkusenost -= 0.05
    nahodne_jmeno = random.choice(nazvy_jezdcu)
    nazvy_jezdcu.pop(nazvy_jezdcu.index(nahodne_jmeno))
    worst.nazev, worst.zkusenost = nahodne_jmeno, random.uniform(0.95,1.05)
    auta.sort(key=lambda x: x.body, reverse=True)
    for i, a in enumerate(auta, 1):
        print(f"{i}. {a.jmeno} – {a.body} bodů ({a.team.nazev})")
        if i == len(auta):
            new = best.jmeno
            skill = best.zkusenost
            print(f"{new} nahrazuje {a.jmeno} ({a.team.nazev})")
            best.jmeno, best.zkusenost = a.jmeno, a.zkusenosti
            a.jmeno, a.zkusenosti = new, skill
    print("\n🏆 Finální pořadí týmů (konstruktérů):")
    teams.sort(key=lambda t: t.body, reverse=True)
    for i, t in enumerate(teams, 1):
        if i == 1:
            t.zkusenost -= 0.1
            img = mpimg.imread(f'tymy/{t.nazev}.png')
            plt.imshow(img)
            plt.axis('off')  # Optional: hides axis for image display
            plt.show()
        print(f"{i}. {t.nazev} – {t.body} bodů")
        if i == len(teams):
            t.zkusenost +=0.1