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


WEATHER_TRANSITIONS = {
    "sunny": {
        "choices": ["sunny", "transitional"],
        "weights": [28, 1]  
    },
    "transitional": {
        "choices": ["sunny", "transitional", "rain"],
        "weights": [1, 3, 1]  
    },
    "rain": {
        "choices": ["transitional", "rain", "heavy rain"],
        "weights": [1, 9, 1]
    },
    "heavy rain": {
        "choices": ["rain", "heavy rain"],
        "weights": [2, 8]
    }
}

def generate_weather(weather, climax):
    prev = weather
    
    if climax == "sunny":
        weather = "sunny"
        
    elif climax == "transitional":
        if weather in WEATHER_TRANSITIONS:
            state_data = WEATHER_TRANSITIONS[weather]
            weather = random.choices(state_data["choices"], weights=state_data["weights"])[0]
            
    # Logování změny stavu
    if weather != prev:
        dlog(fn="generate_weather", msg="weather advanced",
             climax=climax, from_weather=prev, to_weather=weather)
             
    return weather