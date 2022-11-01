from turtle import distance


def reward_function(params):
    reward = 5
    speed = params['speed'] #Range: 0.0:5.0
    steps = params['steps']
    time = steps/15
    progress = params['progress']
    next_point = params['closest_waypoints'][1]
    is_left = params['is_left_of_center']
    steering_angle = abs(params['steering_angle'])
    steer = params['steering_angle']
    distance_from_center = params['distance_from_center']
    if speed < 1.5 or time>11.9:
        return float(1e-3)
    
    reward += steps_reward(steps)
    sp_reward = speed_reward(speed)
    reward = 1e-3 if sp_reward<1e-3 else reward+sp_reward

    if 6 < next_point < 36:
        if speed < 2.5:
            reward -= 40
        if steering_angle > 5:
            reward -= 40
        if 20 < next_point < 28:
            if not is_left:
                reward +=20
        if speed > 2.5 and steering_angle < 5:
            reward += (2*speed)**3
    
    if 40 < next_point < 70:
        if speed < 2.5:
            reward -= 40
        if steering_angle > 5:
            reward -= 40
        if speed > 2.5 and steering_angle < 5:
            reward += (2*speed)**3
    
    # long turn start
    if 65 < next_point < 102:
        if is_left:
            reward += 15
            if 77 < next_point < 86:
                reward += increase_distance(distance_from_center)
            if 86 < next_point < 102:
                reward += reduce_distance(distance_from_center)
    if 65 < next_point < 78:
        if not is_left:
            reward += 15
        
            if next_point < 73:
                reward += increase_distance(distance_from_center)
            
            if next_point == 73 and steer < 0:
                reward += 20

            if next_point > 74:
                reward += reduce_distance(distance_from_center)
    
    if 80 < next_point < 114:
        if is_left:
            reward += 15
            if 80 < next_point < 87 or 100 < next_point <= 110:
                reward += increase_distance(distance_from_center)
            if 88 < next_point < 100 or 110 < next_point <= 114:
                reward += reduce_distance(distance_from_center)
    # long turn end

    if 112 < next_point < 150:
        if speed < 2.5:
            reward -= 40
        if steering_angle > 5:
            reward -=40
        if 116 < next_point < 134:
            if not is_left:
                reward += 20
        if speed > 2.5 and steering_angle < 5:
            reward += (2*speed)**3

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

def increase_distance(distance_from_center): #dfc -> 0 and 0.53
    return float(30*distance_from_center)

def reduce_distance(distance_from_center):
    return float(-30*(distance_from_center-0.535))

def longturn_a(next_point, is_left, distance_from_center, steering_angle):
    reward = 0
    
    return reward


# def waypoints_reward(next_point, is_left):
#     right_lane = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130]
#     if next_point in right_lane and is_left != True:
#         return 40
    
#     elif next_point not in right_lane and is_left == True:
#         return 40

#     return 0

# def speed_angle_reward(speed, steering_angle):
#     reward = 0
#     if 10 < steering_angle < 15 and 1.5 < speed < 2:
#         reward = speed_reward(speed)
#     if steering_angle < 5 and speed > 2.5:
#         reward = speed_reward(speed)

#     return reward

# def curve_cut(next_point, distance_from_center):
#     if 85 < next_point < 91 or 146 < next_point < 148 or 9 < next_point < 14:
#         return float(80*distance_from_center)
#     return 0