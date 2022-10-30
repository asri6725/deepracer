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
    if speed < 1.5 or time>8.5:
        reward = 1e-3
    
    reward += steps_reward(steps)
    sp_reward = speed_reward(speed)
    reward = 1e-3 if sp_reward<1e-3 else reward+sp_reward

    reward+= waypoints_reward(next_point, is_left)
    if 45 < next_point < 77:
        if speed < 2:
            reward -= 20
        if steering_angle > 12:
            reward -=40
    if 117 < next_point < 144:
        if speed < 2:
            reward -= 20
        if steering_angle > 8:
            reward -=40
    if 10 < next_point < 32:
        if speed < 2:
            reward -= 20
        if steering_angle > 8:
            reward -= 40
    
    if progress == 100:
        reward+= max(1e+5, float(2*(44.54183 + (219.2892 - 44.54183)/(1 + (time/7.362352)^41.34854))))

    if reward > 1e+5:
        reward = 1e+5

    return float(reward)

def speed_reward(current_speed):
    reward = float(59.02346 + (-5.97844 - 59.02346)/(1 + (current_speed/2.54036)**4.020232)) # Range (0-50.0) TODO: Calculate the range and keep it below progress
    return reward

def steps_reward(steps): # Range 30 to zero as steps increase
    if steps < 105:
        return float(-910528.8 + (49.99999 - -910528.8)/(1 + (steps/6828481)**1.00001))
    if steps >= 105:
        return max(1e-3, float(-0.4248772 + (36.47548 - -0.4248772)/(1 + (steps/121.3058)**30.0557)))

def waypoints_reward(next_point, is_left):
    right_lane = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134]
    if next_point in right_lane and is_left != True:
        return 40
    
    elif next_point not in right_lane and is_left == True:
        return 40

    return 0

