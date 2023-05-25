import cv2
import sim
import numpy as np

def lookInGray(clientID, sensorHadle):
    # get the image from vision sensor
    res, resolution, image = sim.simxGetVisionSensorImage(clientID, sensorHadle, 0, sim.simx_opmode_buffer)
    print("image is ok")
    if res == sim.simx_return_ok:
        img = np.array(image,dtype=np.uint8)
        img.resize([resolution[1],resolution[0],3])
        cv2.imshow('Before image',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass
        # Grayscale the photo
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        return gray

def get_gray_image_pixel_percentages(img):

    # Create a NumPy array that represents the pixel values of the image
    pixels = np.array(img)

    # Count the number of black, gray, and white pixels
    # num_black_pixels = np.count_nonzero(pixels == 0)
    num_gray_pixels = np.count_nonzero((pixels > 0) & (pixels < 255))
    # num_white_pixels = np.count_nonzero(pixels == 255)

    # Calculate the percentage of black, gray, and white pixels
    total_pixels = pixels.size
    # black_percentage = (num_black_pixels / total_pixels) * 100
    gray_percentage = (num_gray_pixels / total_pixels) * 100
    # white_percentage = (num_white_pixels / total_pixels) * 100

    # Return the grayscale image and pixel percentages
    # return black_percentage, gray_percentage, white_percentage
    return gray_percentage

def get_black_image_pixel_percentages(img):

    # Create a NumPy array that represents the pixel values of the image
    pixels = np.array(img)

    # Count the number of black, gray, and white pixels
    num_black_pixels = np.count_nonzero(pixels == 0)
    # num_gray_pixels = np.count_nonzero((pixels > 0) & (pixels < 255))
    # num_white_pixels = np.count_nonzero(pixels == 255)

    # Calculate the percentage of black, gray, and white pixels
    total_pixels = pixels.size
    black_percentage = (num_black_pixels / total_pixels) * 100
    # gray_percentage = (num_gray_pixels / total_pixels) * 100
    # white_percentage = (num_white_pixels / total_pixels) * 100

    # Return the grayscale image and pixel percentages
    # return black_percentage, gray_percentage, white_percentage
    return black_percentage