import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab

def convert_to_hsv(image_path):
    # Specify the path to your PNG image
    # Replace with your image file path

    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Check if the image is loaded successfully
    if image is None:
        print("Error: Could not load the image.")
        return

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Display the original image
    cv2.imshow('Original Image', image)

    # Display the HSV image
    cv2.imshow('HSV Image', hsv_image)

    # Wait for a key press and close all windows
    print("Press any key to close the windows...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def mask_purple(image_path):
    image = cv2.imread(image_path)

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define HSV range for purple
    lower_purple = np.array([120, 50, 50])  # Lower boundary of purple
    upper_purple = np.array([160, 255, 255])  # Upper boundary of purple

    # Create a mask to extract purple regions
    purple_mask = cv2.inRange(hsv_image, lower_purple, upper_purple)

    # Apply the mask to the original image
    purple_highlight = cv2.bitwise_and(image, image, mask=purple_mask)

    # Display the results
    cv2.imshow('Original Image', image)
    cv2.imshow('Purple Highlight', purple_highlight)

    # Wait for a key press and close the windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def convert_png_to_hsl(image_path):
    """
    Converts a PNG image to HSL (Hue, Saturation, Lightness) color space.

    Args:
        image_path (str): The path to the PNG image file.

    Returns:
        hsl_image: The image converted to HSL color space.
    """
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Check if the image is loaded successfully
    if image is None:
        raise ValueError("Error: Could not load the image. Check the file path.")

    # Convert the image to HSL color space
    hsl_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

    return hsl_image

def main():
    # Specify the path to your PNG image
    image_path = './sample/purple_outline.png'  # Replace with your image file path

    try:
        # Convert the image to HSL
        hsl_image = convert_png_to_hsl(image_path)

        # Display the original image
        original_image = cv2.imread(image_path)
        cv2.imshow('Original Image', original_image)

        # Display the HSL image
        cv2.imshow('HSL Image', hsl_image)

        # Take and display the screenshot of the center square
        screenshot = take_screenshot_center_square()
        screenshot.show()

        # Wait for a key press and close all windows
        print("Press any key to close the windows...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except ValueError as e:
        print(e)

def take_screenshot_center_square():
    """
    Takes a screenshot of a 100x100 pixel square in the middle of the screen.

    Returns:
        screenshot: The captured screenshot as a PIL image.
    """
    # Get the screen resolution
    screen_width, screen_height = pyautogui.size()

    # Calculate the coordinates of the 100x100 square in the center
    left = (screen_width // 2) - 50
    top = (screen_height // 2) - 50
    right = left + 100
    bottom = top + 100

    # Capture the screenshot
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

    return screenshot

if __name__ == "__main__":
    main()

# if __name__ == "__main__":
#     imgPath = './sample/purple_outline.png'
#     # convert_to_hsv(imgPath)
#     mask_purple(imgPath)

