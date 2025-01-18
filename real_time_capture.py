import cv2 
import numpy as np
import time

cam = cv2.VideoCapture("/home/tminh/Downloads/jmdva.mp4")

lower_purple = np.array([120, 50, 50])  # Lower boundary of purple
upper_purple = np.array([160, 255, 255])  # Upper boundary of purple

prev_frame_time, new_frame_time = 0,0

font = cv2.FONT_HERSHEY_SIMPLEX # font to display fps

while cam.isOpened():
    ret, image = cam.read()

    if not ret:
        break
    
    #region process frame
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    purple_mask = cv2.inRange(hsv_image, lower_purple, upper_purple)
    binary_mask = (purple_mask > 0).astype(np.uint8)
    # Apply the mask to the original image
    # purple_highlight = cv2.bitwise_and(image, image, mask=purple_mask)
    #endregion
    
    #region calculate fps
    new_frame_time = time.time()

    fps = 1 / (new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time

    fps = str(int(fps))
    # put fps on frame
    cv2.putText(binary_mask, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA) 
    #endregion

    #region display
    if ret:
        cv2.imshow('rtv', binary_mask*255)
        cv2.waitKey(1)

    if cv2.waitKey(1) == 27: 
        break
    #endregion

cam.release()
cv2.destroyAllWindows()