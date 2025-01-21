import cv2
import numpy as np
import time 
from typing import *

class VideoProcessorConfig():
    def __init__(self,
                frame_width: int | None = None,
                frame_height: int | None = None,
                roi_width: int | None = None,
                roi_height: int | None = None,
                lower_color_bound: Iterable | None = None,
                upper_color_bound: Iterable | None = None,
                fps_font: int | None = None
                ):
        """
        Config dataclass for VideoProcessor class.
            frame_size: Size of input frame, default to 1920x1080.
            roi_size: Size of region of interest, a rectangle in the center of screen, around crosshair, default to 100x25.
            lower_color_bound: Array of HSV value, default to let purple pass through.
            upper_color_bound: Array of HSV value, default to let purple pass through.
            fps_font: Font for displaying fps on screen, default to cv2.FONT_HERSHEY_SIMPLEX.
        """
        self.frame_width = frame_width if frame_width is not None else 1920
        self.frame_height = frame_height if frame_height is not None else 1080
        self.roi_width = roi_width if roi_width is not None else 100
        self.roi_height = roi_height if roi_height is not None else 50
        
        if lower_color_bound is None:
            self.lower_color_bound = np.array([120, 50, 50])
        else: 
            self.lower_color_bound = lower_color_bound if isinstance(lower_color_bound, np.ndarray) else np.array(lower_color_bound)
        
        if upper_color_bound is None:
            self.upper_color_bound = np.array([160, 255, 255])
        else:
            self.upper_color_bound = upper_color_bound if isinstance(upper_color_bound,np.ndarray) else np.array(upper_color_bound)

        self.fps_font = fps_font if fps_font is not None else cv2.FONT_HERSHEY_SIMPLEX

class VideoProcessor():
    def __init__(self, 
                config: VideoProcessorConfig = VideoProcessorConfig()
                ):
        """
        Initialize the custom video processor class.
        """

        self.frame_size = config.frame_width, config.frame_height

        self.roi_size = (config.roi_width, config.roi_height)
        self.__roi_center_X = config.roi_width // 2 # x,y | width, height
        self.__roi_center_Y = config.roi_height // 2

        self.__topleft_corner_X = config.frame_width // 2 - config.roi_width // 2
        self.__topleft_corner_Y = config.frame_height // 2 - config.roi_height // 2
        self.__bottomright_corner_X = self.__topleft_corner_X + config.roi_width
        self.__bottomright_corner_Y = self.__topleft_corner_Y + config.roi_height
        self.lower_color_bound = config.lower_color_bound
        self.upper_color_bound = config.upper_color_bound

        self.__fps_font = config.fps_font

    def getBitMapROI(self, image: np.ndarray) -> np.ndarray:
        # Region of interest
        roi = image[self.__topleft_corner_Y:self.__bottomright_corner_Y, self.__topleft_corner_X:self.__bottomright_corner_X]
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV) # Convert to HSV color system
        roi = cv2.inRange(roi, self.lower_color_bound, self.upper_color_bound) # Check if any pixel is inside color bound
        roi = (roi > 0).astype(np.uint8) # Convert to 2d array with 0 and 1

        return roi

    def isEnemy(self, bitmap: np.ndarray) -> Tuple[bool,str]:
        """
        Check if crosshair is set on an enemy or not
            bitmap : A 2d boolean value 
            -> return bool and reason
        """ 
        
        if bitmap[self.__roi_center_Y,self.__roi_center_X] == 1:
            return True , "center"
        else:
            left_side = bitmap[self.__roi_center_Y, :self.__roi_center_X]
            right_side = bitmap[self.__roi_center_Y, self.__roi_center_X+1:]

            if 1 in left_side and 1 in right_side:
                return True, "left-right"
            
        return False, "nothing"

    def displayOriginalFrame(self, capture: cv2.VideoCapture, showFPS: bool = False) -> None:
        """
        Display original video, press 'q' to end.
            capture: a cv2.VideoCapture instance.
            showFPS: boolean value.
        """
        if showFPS:
            prev_frame_time, new_frame_time = 0,0

        while capture.isOpened():
            status, image = capture.read()

            if not status:
                break

            if showFPS:
                new_frame_time = time.time()

                fps = 1 / (new_frame_time-prev_frame_time)
                prev_frame_time = new_frame_time

                fps = str(int(fps))

                cv2.putText(image, fps, (0, 20), self.__fps_font , 1, (100, 255, 0), 1, cv2.LINE_AA) 

            cv2.imshow("Original", image)
            cv2.waitKey(1)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def displayProcessedROI(self, capture: cv2.VideoCapture, showFPS = False, verbose = False) -> None:
        """
        Display processed ROI, press 'q' to end.
            capture: a cv2.VideoCapture instance.
            showFPS: boolean value.
            verbose: set to True if you want to see reason for shoot function
        """
        if showFPS:
            prev_frame_time, new_frame_time = 0,0

        while capture.isOpened():
            status, image = capture.read()

            if not status:
                break

            bitmap = self.getBitMapROI(image)
            shoot, reason = self.isEnemy(bitmap)
            if shoot and verbose:
                print(reason)

            if showFPS:
                new_frame_time = time.time()

                fps = 1 / (new_frame_time-prev_frame_time)
                prev_frame_time = new_frame_time

                fps = str(int(fps))

                cv2.putText(bitmap, fps, (0, 20), self.__fps_font , 1, (100, 255, 0), 1, cv2.LINE_AA) 

            cv2.imshow("Bitmap", bitmap)
            cv2.waitKey(1)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def displayROI(self, capture: cv2.VideoCapture, showFPS = False) -> None:
        """
        Display ROI at its original state, press 'q' to end.
            capture: a cv2.VideoCapture instance.
            showFPS: boolean value.
        """
        if showFPS:
            prev_frame_time, new_frame_time = 0,0

        while capture.isOpened():
            status, image = capture.read()
            
            if not status:
                break
                
            roi = image[self.__topleft_corner_Y:self.__bottomright_corner_Y, self.__topleft_corner_X:self.__bottomright_corner_X]

            if showFPS:
                new_frame_time = time.time()

                fps = 1 / (new_frame_time-prev_frame_time)
                prev_frame_time = new_frame_time

                fps = str(int(fps))

                cv2.putText(roi, fps, (0, 20), self.__fps_font , 1, (100, 255, 0), 1, cv2.LINE_AA) 

            cv2.imshow("Original ROI", roi)
            cv2.waitKey(1)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == "__main__":
    video_source = "/home/tminh/Downloads/prx_forsaken_gameplay.mp4"
    cap = cv2.VideoCapture(video_source)
    vpc = VideoProcessorConfig( 
                            frame_width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                            frame_height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                            )
    vp = VideoProcessor(vpc)
    vp.displayProcessedROI(cap, showFPS=True, verbose=True)

