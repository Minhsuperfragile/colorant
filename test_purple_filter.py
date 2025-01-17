import cv2
import numpy as np

def filter_purple_to_2d_array(image_path):
    """
    Filter out all colors except purple from the input image and return a 2D array.
    """
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found!")
        return None

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range for purple color in HSV
    lower_purple = np.array([130, 50, 50])  # Adjust as needed
    upper_purple = np.array([160, 255, 255])  # Adjust as needed

    # Create a mask that isolates purple
    mask = cv2.inRange(hsv, lower_purple, upper_purple)

    # Convert the binary mask to a 2D array of 0s and 1s
    binary_mask = (mask > 0).astype(np.uint8)
 
    return binary_mask

def display_and_save_2d_array(binary_mask, output_path):
    """
    Display and save the binary 2D array as an image.
    """
    # Display the result (scaled up for better visibility)
    cv2.imshow("Purple Filtered Mask", binary_mask * 255)  # Multiply by 255 to make it visible
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()

    # Save the binary mask as an image
    cv2.imwrite(output_path, binary_mask * 255)  # Multiply by 255 to save as a visible image
    print(f"Filtered image saved as {output_path}")
    
def check_center_pixel(binary_mask):
    """
    Check if the center pixel of the binary mask has a value of 1.
    """
    # Get the dimensions of the binary mask
    height, width = binary_mask.shape

    # Find the center coordinates
    center_y = height // 2
    center_x = width // 2

    # Get the value of the center pixel
    center_value = binary_mask[center_y, center_x]

    return center_value == 1


def search_purple_from_center(binary_mask):
    """
    Search for purple pixels (value 1) from the center of the image to the edges in all directions.
    Prints the direction and distance of the first purple pixel found.
    """
    # Get the dimensions of the binary mask
    height, width = binary_mask.shape

    # Find the center coordinates
    center_y = height // 2
    center_x = width // 2

    # Define directions as deltas (dy, dx)
    directions = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1),
    }

    # Search in each direction
    for direction, (dy, dx) in directions.items():
        y, x = center_y, center_x
        distance = 0

        while 0 <= y < height and 0 <= x < width:
            if binary_mask[y, x] == 1:
                print(f"Purple pixel found {direction} at distance {distance}.")
                break

            # Move in the direction
            y += dy
            x += dx
            distance += 1
        else:
            print(f"No purple pixel found {direction}.")

if __name__ == "__main__":
    # Input and output file paths
    input_image_path = "full_cypher.PNG"  # Replace with your input image path
    output_image_path = "output.png"  # Replace with your desired output path

    # Process the image to get a 2D array
    purple_mask = filter_purple_to_2d_array(input_image_path)
    # print(check_center_pixel(purple_mask))
    search_purple_from_center(purple_mask)

    # if purple_mask is not None:
    #     # Display and save the result
    #     display_and_save_2d_array(purple_mask, output_image_path)
