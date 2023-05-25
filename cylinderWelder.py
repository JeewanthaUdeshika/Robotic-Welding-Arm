'''
This is the main program of welder robot and this should be run in order to activate robot

Author: Jeewantha Ariyawansha
Last Modified: 02-04-2023
'''

# importing Libraries
import sim
import time
import numpy as np
import moveRobot
import vision
import weldingTorch

# connect with coppeliasim
sim.simxFinish(-1)
clientID = sim.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

if clientID == -1:
    print('Failed to connect to CoppeliaSim remote API server')
    sim.simxFinish(clientID)

else:
    # Getting object handles
    _, visionSence = sim.simxGetObjectHandle(clientID, 'vs1', sim.simx_opmode_oneshot_wait)              # For vision sensor
    _, target = sim.simxGetObjectHandle(clientID, 'Target', sim.simx_opmode_blocking)               # For Target of roboarm
    _, proximity = sim.simxGetObjectHandle(clientID, 'Proximity_sensor', sim.simx_opmode_blocking)  # For proximity sensor
    _, welding = sim.simxGetObjectHandle(clientID, "WeldingTorchActiveTip", sim.simx_opmode_blocking)

    # Move robot to initial position
    firstPoint = (1.0822, -0.32135, 1.6631, 0, 0, 0)    # You can change this according to the object position
    ini_posi = firstPoint
    moveRobot.move(clientID, target, ini_posi, 1)


    # Getting the first image
    err, resolution, image = sim.simxGetVisionSensorImage(clientID, visionSence, 0, sim.simx_opmode_streaming)


    if (sim.simxGetConnectionId(clientID) != -1):
            time.sleep(2)

            target_y = 0
            # Move the target down until the proximity sensor detects an object
            while True: # @Todo: This may be changed to flag
                # Move the target to object
                target_y += 0.01
                moveRobot.move(clientID, target, (ini_posi[0], ini_posi[1]+target_y, ini_posi[2], 0, 0, 0), 1)
                
                # Check if the proximity sensor detects an object
                _, detection_state, _, _, _ = sim.simxReadProximitySensor(clientID, proximity, sim.simx_opmode_blocking)

                if detection_state:
                    print("Object detected!, 1st stage")
                    break
            
                
            # Update the initial position
            for i in range(100):
                ini_posi = sim.simxGetObjectPosition(clientID, target, -1, sim.simx_opmode_streaming)[1]
            print(ini_posi)

            firstWeldPoint = []

            #### IF WELDINGSEAM IS VERTICAL ####
            target_z = 0    
            while True:
                # Move the target through z axis till the welding seam found
                target_z += 0.01
                moveRobot.move(clientID, target, (ini_posi[0], ini_posi[1], ini_posi[2]+target_z, 0, 0, 0), 1)

                # checking the welding seam
                gray = vision.lookInGray(clientID, visionSence)
                grayPresentageVal = vision.get_gray_image_pixel_percentages(gray)

                if grayPresentageVal > 40.16:
                    firstWeldPoint = [ini_posi[0], ini_posi[1], ini_posi[2], 0, 0, 0]
                    break
            
            # Weld the point
            weldingTorch.weld(clientID, target)

            # Update the initial position
            for i in range(100):
                ini_posi = sim.simxGetObjectPosition(clientID, target, -1, sim.simx_opmode_streaming)[1]

            target_x = 0
            target_y = 0
            while True:
                target_x += 0.05
                posi = [ini_posi[0] - target_x, ini_posi[1] - 0.6, ini_posi[2], 0, 0, 0]
                # Move back and go left parrallal to the welding seam
                moveRobot.move(clientID, target, posi, 1)

                # If the end of the welding seam detected, stop the move
                # checking the welding seam
                gray = vision.lookInGray(clientID, visionSence)
                blackPresentageVal = vision.get_black_image_pixel_percentages(gray)

                if blackPresentageVal > 15.25:
                    print("Left end of the object")
                    # Move to the first welded position
                    moveRobot.move(clientID, target, firstPoint, 1)
                    print("Move into first Point")

                    moveRobot.move(clientID, target, (firstWeldPoint[0], firstWeldPoint[1], firstWeldPoint[2], 0,0,0), 1)
                    print("Moved to first weld object")
                    break

                # Move the target down until the proximity sensor detects an object
                while True: # @Todo: This may be changed to flag
                    # Move the for the target
                    target_y += 0.01 
                    
                    # Check if the proximity sensor detects an object
                    _, detection_state, _, _, _ = sim.simxReadProximitySensor(clientID, proximity, sim.simx_opmode_blocking)

                    if detection_state:
                        print("Object detected! when going left")
                        # Weld the point
                        weldingTorch.weld(clientID, target)
                        break

                    moveRobot.move(clientID, target, (posi[0], posi[1]+target_y, posi[2], 0, 0, 0), 1)

                    

            target_x = 0
            target_y = 0
            while True:
                target_x += 0.05
                posi = [ini_posi[0] + target_x, ini_posi[1] - 0.6, ini_posi[2], 0, 0, 0]
                # Move back and go left parrallal to the welding seam
                moveRobot.move(clientID, target, posi, 1)

                # If the end of the welding seam detected, stop the move
                # checking the welding seam
                gray = vision.lookInGray(clientID, visionSence)
                blackPresentageVal = vision.get_black_image_pixel_percentages(gray)

                if blackPresentageVal > 15.25:
                    print("Left end of the object")
                    # Move to the first welded position
                    moveRobot.move(clientID, target, firstPoint, 1)
                    print("Move into first Point")

                    moveRobot.move(clientID, target, (firstWeldPoint[0], firstWeldPoint[1], firstWeldPoint[2], 0,0,0), 1)
                    print("Moved to first weld object")
                    break

                # Move the target down until the proximity sensor detects an object
                while True: # @Todo: This may be changed to flag
                    # Move the for the target
                    target_y += 0.01 

                    # Check if the proximity sensor detects an object
                    _, detection_state, _, _, _ = sim.simxReadProximitySensor(clientID, proximity, sim.simx_opmode_blocking)

                    if detection_state:
                        print("Object detected! when going left")
                        # Weld the point
                        weldingTorch.weld(clientID, target)
                        break

                    moveRobot.move(clientID, target, (posi[0], posi[1]+target_y, posi[2], 0, 0, 0), 1)


            # move to the initial position
            moveRobot.move(clientID, target, firstPoint, 1)

            


        

        


