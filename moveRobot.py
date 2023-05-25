'''
This program is the move function of robo arm of the welder

Author: Jeewantha Ariyawansha
Last Modified: 04-04-2023
'''

import sim as vrep
import time
import numpy as np

# Creating a connection to V-REP
vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
if clientID == -1:
    print('Failed to connect to V-REP remote API server')
    vrep.simxFinish(clientID)

def move(clientID, target, destination, speed):

    # Getting target position and orientation
    _, ini_pos = vrep.simxGetObjectPosition(clientID, target, -1, vrep.simx_opmode_streaming)
    _, ini_ori = vrep.simxGetObjectOrientation(clientID, target, -1, vrep.simx_opmode_streaming)
    
    # deciding shortest orientation

    for i in range(3):
        if ((abs(destination[i+3]-ini_ori[0]) > np.pi) and (ini_ori[i]<0)):
            ini_ori[i] = ini_ori[i] + 2*np.pi
        elif ((abs(destination[i+3]-ini_ori[i]) > np.pi) and (ini_ori[i]>0)):
            ini_ori[i] = ini_ori[i] - 2*np.pi


    # Making initial vector
    ini_vector = np.concatenate((ini_pos, ini_ori))
    dis_vector = destination - ini_vector

    # Getting magnitude of the distance
    distance = np.linalg.norm(dis_vector)
    samples = round(distance * 50)

    for i in range(samples):
        cur_vector = ini_vector + (dis_vector / samples)

        # Stop
        start_time = time.time()
        while (time.time() - start_time) < (distance / (speed * samples)):
            time.sleep(0.001)  # pause for 1 millisecond

        # set positions to go
        vrep.simxSetObjectPosition(clientID, target, -1, cur_vector[:3], vrep.simx_opmode_oneshot)
        vrep.simxSetObjectOrientation(clientID, target, -1, cur_vector[3:], vrep.simx_opmode_oneshot)

        ini_vector = cur_vector

_, target = vrep.simxGetObjectHandle(clientID, 'Target',vrep.simx_opmode_blocking)
_, shape = vrep.simxGetObjectHandle(clientID, 'Shape',vrep.simx_opmode_blocking)

# move1(clientID, target, (1.158, 0.483, 0.1905, 0, 0, 0), 1)



