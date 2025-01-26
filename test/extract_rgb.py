import cv2

# Load the image
image = cv2.imread('around_crosshair.PNG')

# Define the coordinates of the pixel (row, column)
x = 4  # x-coordinate (column)
y = 7  # y-coordinate (row)

# Access the pixel's BGR value
bgr_value = image[y, x]

# Print the BGR value (OpenCV uses BGR format by default)
print(f"BGR value at pixel ({x}, {y}): {bgr_value}")

# Convert BGR to RGB
rgb_value = (bgr_value[2], bgr_value[1], bgr_value[0])  # RGB format
print(f"RGB value at pixel ({x}, {y}): {rgb_value}")
