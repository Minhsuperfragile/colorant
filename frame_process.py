import cv2
import numpy as np

def convert_to_hsv(image):

    # Check if the image is loaded successfully
    if image is None:
        raise TypeError("Could not load image")

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    return hsv_image

def purple_mask(image, hsv_image):
    # Define HSV range for purple
    lower_purple = np.array([120, 50, 50])  # Lower boundary of purple
    upper_purple = np.array([160, 255, 255])  # Upper boundary of purple

    # Create a mask to extract purple regions
    purple_mask = cv2.inRange(hsv_image, lower_purple, upper_purple)

    # Apply the mask to the original image
    purple_highlight = cv2.bitwise_and(image, image, mask=purple_mask)

    return purple_highlight
