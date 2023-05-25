'''
This program models the welder. You can add code to weld module code in this file

Author: Jeewantha Ariyawansha
Last Modified: 04-04-2023
'''

import sim
import moveRobot
import time

def weld(clientID, Handle):
    # get initial target position
    for i in range(100):
        ini_posi = sim.simxGetObjectPosition(clientID, Handle, -1, sim.simx_opmode_streaming)[1]

    moveRobot.move(clientID, Handle, (ini_posi[0], ini_posi[1]-0.03, ini_posi[2], 0, 0, 0), 1)
    time.sleep(2)
    moveRobot.move(clientID, Handle, (ini_posi[0], ini_posi[1]+0.03, ini_posi[2], 0, 0, 0), 1)
