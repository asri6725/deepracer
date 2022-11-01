import math

def reward_function(params):
    reward = 5
    speed = params['speed'] #Range: 0.0:5.0
    steps = params['steps']
    time = steps/15
    progress = params['progress']
    next_point = params['closest_waypoints'][1]
    is_left = params['is_left_of_center']
    steering_angle = abs(params['steering_angle'])
    distance_from_center = params['distance_from_center']
    if time>11.9:
        return float(1e-3)
    
    reward += steps_reward(steps)

    left = [8,9,10,11,12,13,14,15,
           34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,
           57,58,59,60,61,62,63,64,65,66,67,68,69,
           85,86,87,88,89,90,91,92,
           139,140,141,142,143,144,145,146,147,148,149,150,151]
    centerleft = [1,2,3,4,5,6,7,
                 16,17,18,
                 31,32,33,
                 70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,
                 93,94,95,96,97,98,99,100,101,102,103,104,105,
                 106,107,108,109,110,111,112,113,114,115,116,
                 137,138,
                 152,153,154]
    centerright = [19,20,21,22,23,
                  26,27,28,29,30,
                  117,118,119,
                  133,134,135,136]
    right = [24,25,
            120,121,122,123,124,125,126,127,128,129,130,131,132]
    
    if params['all_wheels_on_track'] == True:
        if (next_point in centerleft):
            if (params['distance_from_center']/params['track_width'])<=0.25 and (params['is_left_of_center']):
                reward += 40
            elif (params['distance_from_center']/params['track_width'])<=0.25 and (not params['is_left_of_center']):
                reward += 0
            else:
                reward += -20
                
        elif (next_point in centerright):
            if (params['distance_from_center']/params['track_width'])<=0.25 and (not params['is_left_of_center']):
                reward += 40
            elif (params['distance_from_center']/params['track_width'])<=0.25 and  (params['is_left_of_center']):
                reward += 0
            else:
                reward += -20

        elif (next_point in left):
            if (params['is_left_of_center']) and (params['distance_from_center']/params['track_width'])>0.25 and(params['distance_from_center']/params['track_width'])<0.48:
                reward += 40
            else:
                reward += -20
        elif (next_point in right):
            if (not params['is_left_of_center']) and (params['distance_from_center']/params['track_width'])>0.25 and (params['distance_from_center']/params['track_width'])<0.48:
                reward += 40
            else:
                reward += -20

    fast = [2,3,4,
             14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,
             47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,
             68,69,70,71,72,73,74,75,76,77,78,79,80,
             96,97,98,99,100,101,102,103,104,105,106,107,
             110,111,112,113,114,115,116,117,118,
             123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,
             152,153,154]
    medium = [1,5,6,7,8,9,10,11,12,13,
              34,35,36,37,38,39,40,41,42,43,44,45,46,
              81,82,83,
              86,87,88,89,90,91,92,93,94,95,
              108,109,
              119,120,121,122,
              141,142,143,144,145,146,147,148,149,150,151]
    slow = [84,85,139,140]

    if next_point in fast:
        if speed >= 3:
            reward += speed_reward(speed)
        else:
            reward -= 20
    elif next_point in medium:
        if speed >= 2:
            reward += speed_reward(speed)
        else:
            reward -= 20
    elif next_point in slow:
        if speed >= 1.2 and speed<1.5:
            reward += speed_reward(2*speed)
        else:
            reward -= 20
    
    # reward = 1e-3 if sp_reward<1e-3 else reward+sp_reward

    if progress == 100:
        reward+= float(2*(44.54183 + (219.2892 - 44.54183)/(1 + (time/7.362352)**41.34854)))
    
    if reward > 1e+5:
        reward = 1e+5
    
    if reward < 1e-3:
        reward = 1e-3

    return float(reward)

def speed_reward(current_speed):
    reward = float(59.02346 + (-5.97844 - 59.02346)/(1 + (current_speed/2.54036)**4.020232)) # Range (0-50.0) TODO: Calculate the range and keep it below progress
    return reward

def steps_reward(steps): # Range 30 to zero as steps increase
    if steps < 105:
        return float(-910528.8 + (49.99999 - -910528.8)/(1 + (steps/6828481)**1.00001))
    if steps >= 105:
        return max(1e-3, float(-0.4248772 + (36.47548 - -0.4248772)/(1 + (steps/121.3058)**30.0557)))

# def waypoints_reward(next_point, is_left, speed):
    