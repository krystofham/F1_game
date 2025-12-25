import random
import matplotlib.pyplot as plt
def technical_sector_sim(settings):
    speed_in_training = settings[0]/10
    understeer_in_traning = settings[1]/5
    oversteer_in_training = settings[2]/5
    acceleration = settings[3]/10
    grip = settings[4]/5
    curb_handling = settings[5]/5
    my_time = 30
    my_time -= (grip + acceleration + oversteer_in_training + understeer_in_traning + speed_in_training + curb_handling)
            
    corner_slow = [1, 3, 5, 9, 11, 15]
    corner_medium =  [2, 6, 7, 12, 13]
    corner_fast = [4, 8, 10, 14]
    speeds_on_exit_player = []
    oversteers_player = []
    understeers_player = []
    time_sim_player = []
    for x in range(1, 16):
        chance_mistake = (settings[1] + settings[2]) * -1
        if chance_mistake < 1:
            chance_mistake = 1
        if random.randint(0, 100) < chance_mistake:
            mistake = True
        else:
            mistake = False
        for y in corner_fast:
            if x == y:
                corner = "fast"
        for y in corner_medium:
            if x ==y:
                corner = "medium"
        for y in corner_slow:
            if x==y:
                corner = "slow"
        under = settings[1]*random.uniform(0.98,1.02)
        over = settings[2]*random.uniform(0.98,1.02)
        bonus_time = 0
        if corner == "slow":
            corner_speed = 100+ random.uniform(-5, 5)
            if under > 2:
                corner_speed -= 10*under
                bonus_time += 2
            if over > 2:
                corner_speed -= 10*over
                bonus_time += 2
            if grip < -1:
                under += settings[1]*grip*2
                if under <0:
                    under *= -1
                over += settings[2]*grip
                if over <0:
                    over *= -1
            if curb_handling <-5:
                under += settings[1]*grip
                if under <0:
                    under *= -1
                over += settings[2]*grip*2
                if over <0:
                    over *= -1
            time_sim_player.append(15 + under + over+ bonus_time)
        elif corner == "medium":
            corner_speed = 150+ random.uniform(-5, 5)
            if under > 2:
                corner_speed -= 30*under
                bonus_time += 2
            if over > 2:
                corner_speed -= 30*over
                bonus_time += 2
            if grip < -4:
                under += settings[1]*grip*2
                if under <0:
                    under *= -1
                over += settings[2]*grip
                if over <0:
                    over *= -1
            if curb_handling <-4:
                under += settings[1]*grip
                if under <0:
                    under *= -1
                over += settings[2]*grip*2
                if over <0:
                    over *= -1
            time_sim_player.append(10 + under + over+ bonus_time)
        elif corner == "fast":
            corner_speed = 200+ random.uniform(-5, 5)
            if under > 2:
                corner_speed -= 30*under
                bonus_time += 2
            if over > 2:
                corner_speed -= 30*over
                bonus_time += 2
            if grip < -5:
                under += settings[1]*grip*2
                if under <0:
                    under *= -1
                over += settings[2]*grip
                if over <0:
                    over *= -1
            if curb_handling <-2:
                under += settings[1]*grip
                if under <0:
                    under *= -1
                over += settings[2]*grip*2
                if over <0:
                    over *= -1
            time_sim_player.append(7 + under + over + bonus_time)
        if corner_speed < 0:
            corner_speed = 0
        speed_on_exit = corner_speed +speed_in_training*10+10* acceleration

        if mistake:
            speed_on_exit = 30
            under = 10
            over = 10
        if speed_on_exit <0:
            speed_on_exit *=-1
        speeds_on_exit_player.append(speed_on_exit)
        understeers_player.append(under)
        oversteers_player.append(over)



    speeds_on_exit_bot = []
    time_sim = []
    for x in range(1, 16):
        for y in corner_fast:
            if x == y:
                corner = "fast"
        for y in corner_medium:
            if x ==y:
                corner = "medium"
        for y in corner_slow:
            if x==y:
                corner = "slow"
        under = 0
        over = 0
        if corner == "slow":
            corner_speed = 100+ random.uniform(-25, 25)
            time_sim.append(15 + random.uniform(-1.5, 1.5))
        elif corner == "medium":
            corner_speed = 150+ random.uniform(-25, 25)
            time_sim.append(10 + random.uniform(-1.5, 1.5))
        elif corner == "fast":
            corner_speed = 200+ random.uniform(-25, 25)
            time_sim.append(7+ random.uniform(-1.5, 1.5))
        speeds_on_exit_bot.append(corner_speed)



    turns = list(range(1, 16))
    fig, axs = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
# Time comparison
    axs[0].plot(turns, time_sim_player, label="player – time", marker='o', color='orange')
    axs[0].plot(turns, time_sim, label="Bot – time", marker='o', color='blue')
    axs[0].set_ylabel("time [s]")
    axs[0].legend()
    axs[0].grid(True)
# Speed comparison
    axs[1].plot(turns, speeds_on_exit_player, label="exit player [km/h]", marker='o', color='green')
    axs[1].plot(turns, speeds_on_exit_bot, label="exit bot [km/h]", marker='o', color='gray')
    axs[1].set_ylabel("Speed [km/h]")
    axs[1].legend()
    axs[1].grid(True)

# Understeer / Oversteer
    axs[2].bar(turns, understeers_player, label="understeer", color='blue', alpha=0.6)
    axs[2].bar(turns, oversteers_player, label="oversteer", color='green', alpha=0.6)
    axs[2].set_ylabel("mistakes")
    axs[2].set_xlabel("corner")
    axs[2].legend()
    axs[2].grid(True)

    plt.tight_layout()
    plt.show()
