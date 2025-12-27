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
        under = settings[1]*random.uniform(0.8,1.2)
        over = settings[2]*random.uniform(0.8,1.2)
        bonus_time = 0
        if corner == "slow":
            corner_speed = 100+ random.uniform(-50, 50)
            if under > 2:
                corner_speed -= 10*under
                bonus_time += 2
            if over > 2:
                corner_speed -= 10*over
                bonus_time += 2
            if grip < -1:
                under += settings[1]*grip*2
                over += settings[2]*grip
            if curb_handling <-5:
                under += settings[1]*grip
                over += settings[2]*grip*2
            if over < 0: over*=-1
            if under < 0: under*=-1
            if corner_speed < 10:corner_speed=10
            time_sim_player.append(15 + under + over+ bonus_time)
        elif corner == "medium":
            corner_speed = 150+ random.uniform(-50, 50)
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
            if over < 0: over*=-1
            if under < 0: under*=-1
            if corner_speed < 10:corner_speed=10
            time_sim_player.append(10 + under + over+ bonus_time)
        elif corner == "fast":
            corner_speed = 200+ random.uniform(-50, 50)
            if under > 2:
                corner_speed -= 30*under
                bonus_time += 2
            if over > 2:
                corner_speed -= 30*over
                bonus_time += 2
            if grip < -5:
                under += settings[1]*grip*2
                over += settings[2]*grip
            if curb_handling <-2:
                under += settings[1]*grip
                over += settings[2]*grip*2
            if over < 0: over*=-1
            if under < 0: under*=-1
            if corner_speed < 10:corner_speed=10
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
            corner_speed = 100+ random.uniform(-50, 50)
            time_sim.append(15 + random.uniform(-3.5, 3.5))
        elif corner == "medium":
            corner_speed = 150+ random.uniform(-50, 50)
            time_sim.append(10 + random.uniform(-3.5, 3.5))
        elif corner == "fast":
            corner_speed = 200+ random.uniform(-50, 50)
            time_sim.append(7+ random.uniform(-3.5, 3.5))
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
def training(speed, climax, cars):
    speed_in_training = 0
    understeer_in_traning = 0
    oversteer_in_training = 0
    acceleration = 0
    grip = 0
    curb_handling = 0
    front_wing = None
    rear_wing = None
    brakes = None
    stabilizators = None
    suspension = None
    training = input("Do you want training for speed [1] or qualification [2]: ")
    for x in range(3):
        print("Settings of the car. You have three attemps")
        print("We are setting front wing. Value 0-11. In lower speed higher number. Lowers understeer. During rain bigger number.")
        front_wing = int(input(f"How do you want to set the front wing? Last value: {front_wing}\n"))
        if speed == "quick":
            front_wing_ideal = random.randint(0, 4)
        elif speed == "medium":
            front_wing_ideal = random.randint(4, 7) 
        else:
            front_wing_ideal = random.randint(6, 11)
        if climax == "transitional":
            front_wing_ideal += random.randint(3,5)
        if front_wing_ideal > 11:
            front_wing_ideal = 11
        diff = front_wing_ideal - front_wing
        speed_in_training += diff
        if diff > 2 or diff < -2:
            oversteer_in_training -= diff
        else:
            oversteer_in_training += diff
        understeer_in_traning -= diff
        acceleration += diff
        grip += diff


        print("We are setting rear wing.")
        rear_wing = int(input(f"How do you want to set the rear wing? Last value: {rear_wing}\n"))
        if speed == "quick":
            rear_wing_ideal = random.randint(0, 4)
        elif speed == "medium":
            rear_wing_ideal = random.randint(4, 7) 
        else:
            rear_wing_ideal = random.randint(6, 11)
        if climax == "transitional":
            rear_wing_ideal += random.randint(3,5)
        if rear_wing_ideal > 11:
            rear_wing_ideal = 11
        diff = rear_wing_ideal - rear_wing
        speed_in_training += diff
        if diff > 2 or diff < -2:
            oversteer_in_training -= diff
        else:
            oversteer_in_training += diff
        understeer_in_traning -= diff
        acceleration += diff
        grip += diff


        print("We are setting brakes.")
        brakes = int(input(f"How do you want to set the brakes? 50 - 60. Lower number means bigger oversteer, bigger understeer Last value: {brakes} \n"))
        brakes__ideal = random.randint (50, 60)
        if brakes < 40 or brakes > 70:
            brakes = 55
        diff = brakes__ideal - brakes
        understeer_in_traning += diff * 2
        oversteer_in_training += diff *-2

        print(f"We are setting anti-roll bars. 1 = softer, 2 = harder. If you have harder, the car is faster, but has lower grip. Last value: {stabilizators}")
        stabilizators = int(input("What anti-roll bars do you want\n"))
        if stabilizators == 1:
            grip -= 2
            curb_handling -=2
            speed_in_training +=2
            acceleration +=2
        else:
            grip += 2
            curb_handling +=2
            speed_in_training -=2
            acceleration -=2


        print("We are setting springs.")
        suspension = int(input(f"What springs do you want? 1-hard 2-soft. Hards have better acceleration, lower grip, unstable car, bigger understeer a oversteer. Last value: {suspension}\n"))
        if suspension == 1:
            acceleration += 2
            grip -=1
            curb_handling -=2
            oversteer_in_training -=1
            understeer_in_traning -=1
            speed_in_training +=3
        else:
            acceleration -= 2
            grip +=1
            curb_handling +=2
            oversteer_in_training +=1
            understeer_in_traning +=1
            speed_in_training -=3

        settings = [speed_in_training,understeer_in_traning,oversteer_in_training,acceleration,grip,curb_handling]
        technical_sector_sim(settings)
        if understeer_in_traning > 3 :
            for car in cars:
                if car.is_player:
                    car.safety_car_probability -= understeer_in_traning*250
        if oversteer_in_training > 3 :
            for car in cars:
                if car.is_player:
                    car.safety_car_probability -= oversteer_in_training*250
        if grip > 3 :
            for car in cars:
                if car.is_player:
                    car.safety_car_probability -= 250*grip
        if curb_handling >3:
            for car in cars:
                if car.is_player:
                    car.safety_car_probability -= curb_handling*250     
        if oversteer_in_training < -2 :
            for car in cars:
                if car.is_player:
                    car.safety_car_probability += oversteer_in_training*250
        if oversteer_in_training < -2 :
            for car in cars:
                if car.is_player:
                    car.safety_car_probability += oversteer_in_training*250
        if grip < -2:
            for car in cars:
                if car.is_player:
                    car.safety_car_probability += 250*grip
        if curb_handling <-2:
            for car in cars:
                if car.is_player:
                    car.safety_car_probability += curb_handling*250     
        if oversteer_in_training + understeer_in_traning > 5:
            for car in cars:
                if car.is_player:
                    car.safety_car_probability -= (oversteer_in_training + understeer_in_traning)*150
    if speed_in_training + acceleration > 5:
        speed_bonus = True
    else:
        speed_bonus = False
    return speed_bonus, training