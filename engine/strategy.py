from log import dlog


def strategy(LAPS, TIME_S1, TIME_S2, TIME_S3, pneu, speed, climax):
    count_laps = LAPS
    if count_laps < 2:
        count_laps = 3
    lap_time = (TIME_S1 + TIME_S2 + TIME_S3)/60
    if pneu == "medium":
        k_wear = [1.5,5,9,4.4,8.4]
    elif pneu == "soft":
        k_wear = [2,7,12,5,9]       
    else:
        k_wear = [1,4,7,4,8]
    if speed == "medium":
        k_speed = [1,1.04,1.08,0.6,0.65]
    elif speed == "quick":
        k_speed = [1.05,1.09,1.13,0.65,0.7]
    else:
        k_speed = [0.95,0.99,1.03,0.55,0.6]
    endurance_s = 60/k_wear[2]*k_speed[2]
    endurance_m = 60/k_wear[1]*k_speed[1]
    endurance_h =60/k_wear[0]*k_speed[0]
    endurance_i = 60/k_wear[4]*k_speed[4]
    endurance_w = 60/k_wear[3]*k_speed[3]
    wear = [endurance_h, endurance_m, endurance_s]
    name = ["hard", "medium", "soft"]
    dlog(fn="strategy", msg="tyre endurance calculated",
         laps_remaining=LAPS, pneu_type=pneu, speed_type=speed, climax=climax,
         hard_laps=round(endurance_h, 1), medium_laps=round(endurance_m, 1),
         soft_laps=round(endurance_s, 1),
         inter_laps=round(endurance_i, 1) if climax != "sunny" else None,
         wet_laps=round(endurance_w, 1) if climax != "sunny" else None)
    if climax == "sunny":
        pass
        #print(f"soft can do {round(endurance_s, 1)} laps, medium {round(endurance_m, 1)} laps, hard {round(endurance_h, 1)} laps")
    else:
        pass
        #print(f"soft can do {round(endurance_s, 1)} laps, medium {round(endurance_m, 1)} laps, hard {round(endurance_h, 1)} laps, inter {round(endurance_i, 1)}, wet {round(endurance_w, 1)}")
    box_time = (100/60)
    if count_laps == 0:
        count_laps = 1
    for i, stint in enumerate(wear, 0):
        if count_laps + 4 < wear[i] < count_laps +20:
            remain = wear[i] - count_laps
            average_speed = (wear[i] - remain)*k_speed[i]/count_laps
            time = round((lap_time*LAPS)/average_speed, 2)

            #print(f"Possible strategy - {round(stint, 0)} laps - {time} minutes - {name[i]}")



    for i in range(len(wear)):
        if count_laps + 4 < wear[i] + wear[0] < count_laps +20:
            remain = wear[i] + wear[0]- count_laps
            countlapsendurance2 = wear[0] - remain
            average_speed = (k_speed[i]*wear[i] + countlapsendurance2*k_speed[0])/count_laps
            time = round(((lap_time*LAPS)/average_speed) + box_time, 2)
            if countlapsendurance2 > 0:
                pass
                #print(f"Possible strategy - {round(wear[i] + wear[0],0)} laps - {time} minutes - {name[i]}, {name[0]}")
        if count_laps + 4 < wear[i] + wear[1]  < count_laps +20:
            remain = wear[i] + wear[1]- count_laps
            countlapsendurance2 = wear[1] - remain
            average_speed = (k_speed[i]*wear[i] + countlapsendurance2*k_speed[1])/count_laps
            time = round(((lap_time*LAPS)/average_speed) + box_time, 2)
            if countlapsendurance2 > 0:
                pass
                #print(f"Possible strategy - {round(wear[i] + wear[1],0)} laps - {time} minutes - {name[i]}, {name[1]}")
        if count_laps + 4 < wear[i] + wear[2]  < count_laps +20:
            remain = wear[i]+ wear[2] - count_laps
            countlapsendurance2 = wear[2] - remain
            average_speed = (k_speed[i]*wear[i] + countlapsendurance2*k_speed[2])/count_laps
            time = round(((lap_time*LAPS)/average_speed) + box_time, 2)
            if countlapsendurance2 > 0:
                pass
                #print(f"Possible strategy - {round(wear[i] + wear[2], 0)} laps - {time} minutes - {name[i]}, {name[2]}")
    for i in range(len(wear)):
        for j in range(len(wear)):
            if count_laps + 4 <wear[i] + wear[j] + wear[0]  < count_laps +20:
                remain = wear[i] + wear[j]  + wear[0] - count_laps
                countlapsendurance2 = wear[0] - remain
                average_speed = (k_speed[i]*wear[i] + k_speed[j]*wear[j]+ countlapsendurance2*k_speed[0])/count_laps
                time = round((lap_time*LAPS/average_speed) + box_time*2, 2)
                if countlapsendurance2 > 0:
                    pass
                    #print(f"Possible strategy - {round(wear[i] + wear[j] + wear[0], 0)} laps - {round(lap_time*(wear[i] + wear[j]+wear[0]) + box_time*2, 0)} minutes - {name[i]}, {name[j]}, {name[0]}")
            if count_laps + 4 <wear[i] + wear[j] + wear[1]  < count_laps +20:
                remain = wear[i] + wear[j]  + wear[1]- count_laps
                countlapsendurance2 = wear[1] - remain
                average_speed = (k_speed[i]*wear[i] + k_speed[j]*wear[j]+ countlapsendurance2*k_speed[1])/count_laps
                time = round(((lap_time*LAPS)/average_speed) + box_time*2, 2)
                if countlapsendurance2 > 0:
                    pass
                    #print(f"Possible strategy - {round(wear[i] + wear[j] + wear[1], 0)} laps - {round(lap_time*(wear[i] + wear[j]+wear[1]) + box_time*2, 0)} minutes - {name[i]}, {name[j]}, {name[1]}")
            if count_laps + 4 <wear[i] + wear[j] + wear[2]  < count_laps +20:
                remain = wear[i] + wear[j] + wear[2]- count_laps
                countlapsendurance2 = wear[2] - remain
                average_speed = (k_speed[i]*wear[i] + k_speed[j]*wear[j]+ countlapsendurance2*k_speed[2])/count_laps
                time =  round(((lap_time*LAPS)/average_speed) + box_time*2, 2)
                if countlapsendurance2 > 0:
                    pass
                    #print(f"Possible strategy - {round(wear[i] + wear[j] + wear[2], 0)} laps - {time} minutes - {name[i]}, {name[j]}, {name[2]}")
