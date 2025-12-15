import matplotlib.pyplot as plt
import random

# Setup proměnné z vozu
grip = 3
acceleration = 2
oversteer_in_training = 1
understeer_in_traning = 2
speed_in_training = 3
curb_handling = 1

# Definuj 10 zatáček různých typů
corners = [
    {"type": "slow"}, {"type": "medium"}, {"type": "fast"},
    {"type": "slow"}, {"type": "fast"}, {"type": "medium"},
    {"type": "slow"}, {"type": "fast"}, {"type": "medium"}, {"type": "slow"}
]

sector_times = []
corner_speeds = []
oversteer_flags = []
understeer_flags = []

for i, corner in enumerate(corners):
    typ = corner["type"]

    # Nastav ideální time podle typu zatáčky
    if typ == "slow":
        base_time = 4.0
        grip_importance = 0.3
        accel_importance = 0.3
        speed_importance = 0.1
    elif typ == "medium":
        base_time = 3.2
        grip_importance = 0.2
        accel_importance = 0.2
        speed_importance = 0.2
    else:  # fast
        base_time = 2.6
        grip_importance = 0.1
        accel_importance = 0.1
        speed_importance = 0.4

    # Simuluj chyby
    over = max(0, oversteer_in_training + random.randint(-1, 2))
    under = max(0, understeer_in_traning + random.randint(-1, 2))
    corner_penalty = (over + under) * 0.15

    # Výpočet timeu v zatáčce podle setupu a typu
    time = base_time \
        - grip * grip_importance \
        - acceleration * accel_importance \
        - speed_in_training * speed_importance \
        + corner_penalty \
        + random.uniform(-0.1, 0.1)

    # Rychlost exitu ze zatáčky (čistě ilustrační)
    exit_speed = 150 if typ == "slow" else 200 if typ == "medium" else 270
    exit_speed += speed_in_training * 2 - (over + under) * 2 + random.randint(-5, 5)

    # Ulož hodnoty
    sector_times.append(round(time, 2))
    corner_speeds.append(exit_speed)
    oversteer_flags.append(over)
    understeer_flags.append(under)

# === 📊 GRAF 1: time v zatáčkách
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(sector_times, marker='o', color='orange', label='time v zatáčce (s)')
plt.axhline(y=3.0, color='green', linestyle='--', label='Referenční time')
plt.title("🕒 time v zatáčkách podle typu")
plt.xlabel("corner (číslo)")
plt.ylabel("time (s)")
plt.legend()
plt.grid(True)

# === 📊 GRAF 2: Rychlost + chyby
plt.subplot(2, 1, 2)
plt.plot(corner_speeds, marker='s', color='blue', label='Rychlost exitu (km/h)')
plt.bar(range(len(corners)), oversteer_flags, color='red', alpha=0.5, label='oversteer')
plt.bar(range(len(corners)), understeer_flags, bottom=oversteer_flags, color='purple', alpha=0.5, label='understeer')

# Popisky zatáček (typy)
corner_labels = [f"{i+1} ({c['type']})" for i, c in enumerate(corners)]
plt.xticks(ticks=range(len(corners)), labels=corner_labels, rotation=45)

plt.title("📈 Rychlost a chyby v zatáčkách")
plt.xlabel("corner")
plt.ylabel("Rychlost / chyby")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
