import math
def reward_function(params):
    reward = 5
    speed = params['speed'] #Range: 0.0:5.0
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']   #Range: -180:+180 - Heading direction, in degrees, of the agent with respect to the x-axis of the coordinate system.
    progress = params['progress'] # Range 0-100
    steps = params['steps']
    time = steps/15
    if not params["all_wheels_on_track"] or speed < 1.5:
        reward = 1e-3
    
    reward += steps_reward(time)
    sp_reward = speed_reward(speed)
    reward = 1e-3 if sp_reward<1e-3 else reward+sp_reward
    # reward += way_points_reward(waypoints, closest_waypoints, heading)

    if reward > 1e+5:
        reward = 1e+5
    
    return float(reward)

def speed_reward(current_speed):
    reward = float(59.02346 + (-5.97844 - 59.02346)/(1 + (current_speed/2.54036)**4.020232)) # Range (0-50.0) TODO: Calculate the range and keep it below progress
    return reward

def steps_reward(time): # Range 30 to zero as steps increase
    if time < 17:
        return float( -2.424007 + (58.47831 - -2.424007)/(1 + (time/17.62056)**1.24265))
    if time >= 17:
        return float(-53.76254 + (35.20395 - -53.76254)/(1 + (time/18.64757)**26.26079))


# def way_points_reward(waypoints, closest_waypoints, heading): 
    
#     reward = 30.0
#     # Calculate the direction of the center line based on the closest waypoints
#     next_index = min(closest_waypoints[0]+4, len(waypoints)-1)
#     next_point = waypoints[next_index]
#     prev_point = waypoints[closest_waypoints[0]]

#     # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
#     track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
#     # Convert to degree
#     track_direction = math.degrees(track_direction)

#     # Calculate the difference between the track direction and the heading direction of the car
#     direction_diff = abs(track_direction - heading)
#     if direction_diff > 180:
#         direction_diff = 360 - direction_diff

#     # Penalize the reward if the difference is too large
#     DIRECTION_THRESHOLD_1 = 6.0
#     DIRECTION_THRESHOLD_2 = 15.0
#     DIRECTION_THRESHOLD_3 = 45.0

#     if direction_diff > DIRECTION_THRESHOLD_1:
#         reward *= 0.5
#     elif direction_diff > DIRECTION_THRESHOLD_2:
#         reward *= 0.25
#     elif direction_diff > DIRECTION_THRESHOLD_3:
#         reward = 1e-3
#     return float(reward) # Max - 30