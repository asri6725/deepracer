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
    
    reward += speed_reward(speed)
    # reward += progress_reward(progress)
    reward += way_points_reward(waypoints, closest_waypoints, heading)

    TOTAL_NUM_STEPS = 250

    if progress == 100:
        reward += 1500 * (progress/steps)
        if abs(time)-10 <= 0:
            reward += 200000*(-0.2307168 + (113139200 - -0.2307168)/(1 + (time/2.181144)**11.95197))
    

    if not params["all_wheels_on_track"]:
        reward = 1e-3
    
    return float(reward)

def speed_reward(current_speed):
    max_speed = 4
    return float(current_speed**2*max_speed*5) # Range (0-80) TODO: Calculate the range and keep it below progress

def progress_reward(progress): 
    return float(progress/2) # Range 0-200

def way_points_reward(waypoints, closest_waypoints, heading): 
    
    reward = 300.0
    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[0]+4]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD_1 = 15.0
    DIRECTION_THRESHOLD_2 = 45.0
    DIRECTION_THRESHOLD_3 = 90.0

    if direction_diff > DIRECTION_THRESHOLD_1:
        reward *= 0.5
    elif direction_diff > DIRECTION_THRESHOLD_2:
        reward *= 0.25
    elif direction_diff > DIRECTION_THRESHOLD_3:
        reward = 1e-3
    return float(reward) # Max - 30