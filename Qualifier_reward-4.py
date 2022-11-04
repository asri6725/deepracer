

def reward_function(params):
    reward = 5
    speed = params['speed'] #Range: 0.0:4.0
    steps = params['steps']
    time = steps/15
    progress = params['progress']
    closest_waypoints = params['closest_waypoints']
    x, y = params['x'], params['y']
    # is_left = params['is_left_of_center']
    steering_angle = abs(params['steering_angle'])
    # steer = params['steering_angle']
    # distance_from_center = params['distance_from_center']
    if speed < 1.5 or time>11.5:
        return float(1e-3)
    
    reward += steps_reward(steps)
    sp_reward = speed_reward(speed)
    reward = 1e-3 if sp_reward<1e-3 else reward+sp_reward
    d_reward = distance_reward(closest_waypoints, x, y)
    reward = 1e-3 if d_reward < 1e-3 else reward+sp_reward

    next_point = closest_waypoints[1]
    if 6 < next_point < 36:
        if speed < 2.5:
            reward -= 40
        if steering_angle > 5:
            reward -= 40
        if speed > 2.5 and steering_angle < 5:
            reward += (2*speed)**3
    
    if 40 < next_point < 70:
        if speed < 2.5:
            reward -= 40
        if steering_angle > 5:
            reward -= 40
        if speed > 2.5 and steering_angle < 5:
            reward += (2*speed)**3

    if 112 < next_point < 150:
        if speed < 2.5:
            reward -= 40
        if steering_angle > 5:
            reward -=40
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

def distance_reward(closest_waypoints, x, y):
    distance_from_ideal = min ( 
        distance([x,y], ideal_waypoints(closest_waypoints[0])),
        distance([x,y], ideal_waypoints(closest_waypoints[1]))
    )

    return float(-2.16061 + (28.59262 - -2.16061)/(1 + (distance_from_ideal/0.1349032)**2.258325))

def distance(point1, point2):
    return float(( abs(point2[0]-point1[0]) + abs(point2[1] - point1[1]) )**0.5 )

def ideal_waypoints(loc):
    return [[0.63069109, 2.80611932],
       [0.63367125, 2.69079621],
       [0.6467188 , 2.57569291],
       [0.66972231, 2.46183988],
       [0.70251506, 2.35022569],
       [0.74487589, 2.24177514],
       [0.79652923, 2.1373277 ],
       [0.85714459, 2.03761659],
       [0.92633571, 1.94324872],
       [1.00365975, 1.85468625],
       [1.08861721, 1.77223051],
       [1.1806537 , 1.69600972],
       [1.27916562, 1.6259728 ],
       [1.38351227, 1.56189156],
       [1.4930358 , 1.50337335],
       [1.60708637, 1.44988322],
       [1.72504192, 1.40077175],
       [1.84630443, 1.35530161],
       [1.97025603, 1.31266612],
       [2.09617545, 1.2719922 ],
       [2.2231517 , 1.23232374],
       [2.35576976, 1.190681  ],
       [2.48814156, 1.14836059],
       [2.62010372, 1.1049143 ],
       [2.75155515, 1.06006668],
       [2.88245693, 1.01371411],
       [3.01283929, 0.96594252],
       [3.14278403, 0.91697795],
       [3.27239538, 0.86710616],
       [3.40178871, 0.81664194],
       [3.52534292, 0.76798582],
       [3.64882806, 0.72098717],
       [3.77225054, 0.67657779],
       [3.89565744, 0.63576533],
       [4.01912628, 0.59935302],
       [4.14273194, 0.56802807],
       [4.26652265, 0.54240254],
       [4.390508  , 0.52303129],
       [4.5146562 , 0.51041311],
       [4.63889641, 0.50498126],
       [4.76312271, 0.50708933],
       [4.88719857, 0.51699788],
       [5.01096146, 0.53486531],
       [5.13422789, 0.56074489],
       [5.25679889, 0.59458804],
       [5.3784661 , 0.63625275],
       [5.49901791, 0.68551547],
       [5.61824556, 0.74208505],
       [5.73594876, 0.8056172 ],
       [5.85194051, 0.87572882],
       [5.96605088, 0.95201138],
       [6.0781297 , 1.03404317],
       [6.18804798, 1.12140005],
       [6.29569809, 1.21366463],
       [6.40099292, 1.31043383],
       [6.50386394, 1.41132475],
       [6.60425847, 1.51597899],
       [6.70213638, 1.62406543],
       [6.79746619, 1.73528168],
       [6.89022097, 1.84935431],
       [6.980374  , 1.96603801],
       [7.06789434, 2.08511385],
       [7.15274241, 2.20638682],
       [7.23486553, 2.32968268],
       [7.31419351, 2.4548443 ],
       [7.39063436, 2.58172754],
       [7.46407004, 2.71019664],
       [7.5343525 , 2.84011927],
       [7.60129994, 2.9713612 ],
       [7.6646937 , 3.10378064],
       [7.72427579, 3.2372224 ],
       [7.77974745, 3.37151184],
       [7.83076905, 3.50644891],
       [7.87696157, 3.64180249],
       [7.91791   , 3.77730515],
       [7.9531689 , 3.91264892],
       [7.98227014, 4.0474821 ],
       [8.00473301, 4.18140776],
       [8.02007634, 4.31398396],
       [8.02783246, 4.44472614],
       [8.02756242, 4.57311169],
       [8.01887186, 4.69858671],
       [8.00142678, 4.82057488],
       [7.97496831, 4.93848799],
       [7.9393258 , 5.05173771],
       [7.89442733, 5.15974804],
       [7.84030706, 5.26196766],
       [7.77710908, 5.35788145],
       [7.7050874 , 5.44702069],
       [7.62460227, 5.52897101],
       [7.536113  , 5.60337802],
       [7.44016781, 5.66995014],
       [7.33739134, 5.72845868],
       [7.22847048, 5.77873548],
       [7.11413941, 5.82066844],
       [6.99516423, 5.85419554],
       [6.87232807, 5.8792982 ],
       [6.74641682, 5.89599457],
       [6.61820582, 5.90433369],
       [6.48844757, 5.90439106],
       [6.35786039, 5.89626615],
       [6.22711782, 5.88008231],
       [6.09683868, 5.85598899],
       [5.96757762, 5.82416624],
       [5.83981608, 5.78483111],
       [5.71395379, 5.73824529],
       [5.59030113, 5.68472331],
       [5.46907261, 5.62464036],
       [5.35038212, 5.55843893],
       [5.23424046, 5.48663315],
       [5.12055594, 5.40981015],
       [5.00913994, 5.32862503],
       [4.89972666, 5.24377382],
       [4.79201344, 5.15593375],
       [4.6857631 , 5.06560545],
       [4.5807927 , 4.97315917],
       [4.48081878, 4.88243357],
       [4.37959748, 4.79420328],
       [4.27684354, 4.70906838],
       [4.17224941, 4.62769566],
       [4.06553767, 4.55071821],
       [3.95644174, 4.47877854],
       [3.84474817, 4.41244104],
       [3.73031118, 4.35215634],
       [3.61306059, 4.29823493],
       [3.49300409, 4.25082828],
       [3.37022468, 4.20991786],
       [3.24487511, 4.17530971],
       [3.1171707 , 4.14663361],
       [2.98738247, 4.12334422],
       [2.85585139, 4.10466958],
       [2.72282052, 4.09005797],
       [2.58852158, 4.07896026],
       [2.45315288, 4.07089104],
       [2.31675601, 4.06579649],
       [2.18425079, 4.05787239],
       [2.05356546, 4.04652377],
       [1.9251617 , 4.03105575],
       [1.79950825, 4.01084184],
       [1.67721911, 3.98511327],
       [1.55873527, 3.9534865 ],
       [1.44466638, 3.91541352],
       [1.33564671, 3.8704324 ],
       [1.23222981, 3.81830074],
       [1.13519251, 3.7586213 ],
       [1.04519953, 3.69128277],
       [0.96285535, 3.61637202],
       [0.88870748, 3.5341512 ],
       [0.82324005, 3.44504611],
       [0.76686864, 3.34963169],
       [0.71993756, 3.24861421],
       [0.68271928, 3.1428114 ],
       [0.65541543, 3.03313123],
       [0.63815905, 2.92055024],
       [0.63069109, 2.80611932]][loc]