import cv2

# Load the image (assuming it's a PNG)
image = cv2.imread('D:\\tminh\\New folder\\colorant\\around_crosshair.PNG')

# Check if the image was loaded correctly
if image is None:
    print("Error: Image not found!")
    exit()

# Convert the image from BGR (default) to HSV color space
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

height, width, channels = image.shape

# Print the size of the image
print(f"Width: {width} pixels")
print(f"Height: {height} pixels")
print(f"Channels: {channels}")

# Display the original and HSV image
cv2.imshow('Original Image', image)
cv2.imshow('HSV Image', hsv_image)

# Wait until a key is pressed, then close the image windows
cv2.waitKey(0)
cv2.destroyAllWindows()
