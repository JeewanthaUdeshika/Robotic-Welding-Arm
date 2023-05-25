'''
This is the test Program to detect colour presentage. This can be used to get the colour presentage units to end of the welding seam of specific object by move the tip by mouse corresponding seam

Author: Jeewantha Ariyawansha
Last Modified: 04-04-2023
'''

import sim as vrep
import time
import cv2
import numpy as np
import moveRobot
import time
import vision

vrep.simxFinish(-1)

clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)


if clientID!=-1:
    print ('Connected to remote API server')
    print ('Vision Sensor object handling')
    res, v1 = vrep.simxGetObjectHandle(clientID, 'vs1', vrep.simx_opmode_oneshot_wait)
    _, target = vrep.simxGetObjectHandle(clientID, 'Target',vrep.simx_opmode_blocking)
    print ('Getting first image')
    # moveRobot.move1(clientID, target, (1.5250, -1, 0.852, 0, 0, 0), 1)
    err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_streaming)
    while (vrep.simxGetConnectionId(clientID) != -1):
        time.sleep(2)
        err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_buffer)

        print(resolution)
        if err == vrep.simx_return_ok:
            print ("image OK!!!")
            img = np.array(image,dtype=np.uint8)
            img.resize([resolution[1],resolution[0],3])
            cv2.imshow('Before image',img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            """ gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            canny_edges = cv2.Canny(gray_image, 120, 150) """

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            cv2.imshow("Grayed", gray)

            #########################
            print(vision.get_black_image_pixel_percentages(gray))
            #print(vision.get_white_image_pixel_percentages(gray))
            #print(vision.get_gray_image_pixel_percentages(gray))
            #########################

else:
  print ("Failed to connect to remote API Server")
  vrep.simxFinish(clientID)

cv2.destroyAllWindows()