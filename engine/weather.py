import random
from log import dlog


def wet_track(weather, wettiness):
    before = wettiness
    if weather == "heavy rain":
        wettiness += 30
    if weather == "rain":
        wettiness += 20
    if weather == "transitional":
        if wettiness < 60:
            wettiness += 10
        elif wettiness >40:  
            wettiness -= 10
    if weather == "sunny":
        wettiness -= 20
    if wettiness > 100:
        wettiness = 100
    if wettiness < 0:
        wettiness = 0
    if wettiness != before:
        dlog(fn="wet_track", msg="track wettiness updated",
             weather=weather, before=before, after=wettiness)
    return wettiness


def generate_weather(weather, climax):
    prev = weather
    if climax == "transitional":
        if weather == "sunny":
            weather = random.choice(["sunny", "sunny","sunny","sunny", "sunny", "sunny","sunny","sunny","sunny", "sunny","sunny","sunny", "sunny", "sunny","sunny","sunny","sunny", "sunny","sunny","sunny", "sunny", "sunny","sunny","sunny", "sunny", "sunny","sunny","sunny", "transitional"])
        elif weather == "transitional":
            weather = random.choice(["sunny", "transitional", "transitional","transitional","rain"])
        elif weather == "rain":
            weather = random.choice(["transitional", "rain", "rain", "rain", "rain", "rain", "rain", "rain", "rain", "rain", "heavy rain"])
        elif weather == "heavy rain":
            weather = random.choice(["rain", "rain", "heavy rain", "heavy rain", "heavy rain", "heavy rain", "heavy rain", "heavy rain", "heavy rain", "heavy rain"])
    if climax == "sunny":
        weather = "sunny"
    if weather != prev:
        dlog(fn="generate_weather", msg="weather advanced",
             climax=climax, from_weather=prev, to_weather=weather)
    return weather
