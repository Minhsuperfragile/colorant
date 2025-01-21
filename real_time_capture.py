import cv2 
import numpy as np
import time

cam = cv2.VideoCapture("/home/tminh/Downloads/prx_forsaken_gameplay.mp4")

# Get video frame dimensions
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define rectangle size
rect_width = 100
rect_height = 25

# Region of interest center
roi_center_x = rect_width // 2
roi_center_y = rect_height // 2

# Calculate the center position
center_x = frame_width // 2
center_y = frame_height // 2

# Define the top-left and bottom-right corners of the rectangle
x1 = center_x - rect_width // 2
y1 = center_y - rect_height // 2
x2 = x1 + rect_width
y2 = y1 + rect_height

lower_purple = np.array([120, 50, 50])  # Lower boundary of purple
upper_purple = np.array([160, 255, 255])  # Upper boundary of purple

prev_frame_time, new_frame_time = 0,0

font = cv2.FONT_HERSHEY_SIMPLEX # font to display fps

while cam.isOpened():
    ret, image = cam.read()

    if not ret:
        break
    
    #region process frame
    roi = image[y1:y2, x1:x2] #region of interests

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    purple_mask = cv2.inRange(hsv_image, lower_purple, upper_purple)
    binary_mask = (purple_mask > 0).astype(np.uint8)

    if binary_mask[roi_center_y,roi_center_x] == 1:
        print("shoot, middle is purple")
    else:
        left_side = binary_mask[roi_center_y, :roi_center_x]
        right_side = binary_mask[roi_center_y, roi_center_x+1:]
        
        if 1 in left_side and 1 in right_side:
            print("shoot, left and right are purple")

    #endregion
    
    #region calculate fps
    new_frame_time = time.time()

    fps = 1 / (new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time

    fps = str(int(fps))

    # put fps on frame
    # cv2.putText(binary_mask, fps, (0, 20), font, 1, (100, 255, 0), 3, cv2.LINE_AA) 
    #endregion

    #region display
    if ret:
        # cv2.imshow('rtv', binary_mask*255)
        cv2.imshow('real', roi)
        cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    #endregion

cam.release()
cv2.destroyAllWindows()