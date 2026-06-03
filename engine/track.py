from log import log
import os
import random
import json

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
    @staticmethod
    def load_all_from_json():
        """
        Načte konfiguraci ze souboru /config/tracks.json přesně podle poskytnuté struktury.
        """
        # Cesta o úroveň výš (z /engine do /config)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, '..', 'config', 'tracks.json')

        tracks_list = []
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    track = Track(
                        name=item["name"],
                        pneu=item["pneu_wear"],
                        speed=item["speed_type"],
                        TIME_S1=item["temp_1"],
                        TIME_S2=item["temp_2"],
                        TIME_S3=item["temp_3"],
                        laps=item["laps"],
                        dnf_probability=item["dnf_probability"] 
                    )
                    tracks_list.append(track)
        except FileNotFoundError:
            log(f"[ERROR] Soubor s tratěmi nebyl nalezen na adrese: {json_path}")
            return []
        except json.JSONDecodeError:
            log(f"[ERROR] Chyba při čtení JSONu v: {json_path}")
            return []
        random.shuffle(tracks_list)
        return tracks_list

# Automatické načtení při importu modulu
tracks = Track.load_all_from_json()