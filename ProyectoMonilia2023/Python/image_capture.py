import datetime as dt
import os
import cv2
from time import sleep


class ImageCapture():
    CAMERA_WINDOW_NAME = "RGB Camera"
    TIMEZONE = dt.timezone(dt.timedelta(hours=-5))
    IMAGES_ROOT_DIR_NAME = "images/"
    DATE_TIME_FORMAT = "%d%m%Y%H%M%S/"
    FRAME_WIDTH = 1280
    FRAME_HEIGHT = 960

    def __init__(self):
        cv2.namedWindow(self.CAMERA_WINDOW_NAME, cv2.WINDOW_NORMAL)
        self.rgb_camera = None

    def create_image_dir(self):
        """Creates a new directory for the images according to the current date
        and time."""
        current_dt = dt.datetime.now(self.TIMEZONE)
        image_dir = current_dt.strftime(self.DATE_TIME_FORMAT)
        os.makedirs(self.IMAGES_ROOT_DIR_NAME + image_dir)
        # Returns the path to the created directory.
        return image_dir

    def capture_rgb_image(self, image_dir, image_name):
        """Captures an image and stores it in the given directory under the 
        given name."""
        self.rgb_camera = cv2.VideoCapture(0)
        # 3 = frame width (def. 640, max. 1280); 4 = frame height (def. 480, 
        # max. 720).
        self.rgb_camera.set(3, self.FRAME_WIDTH)
        self.rgb_camera.set(4, self.FRAME_HEIGHT)
        # Waits 3 seconds so that the camera focuses.
        sleep(3)
        # Tries to capture the image.
        is_image_captured, image = self.rgb_camera.read()
        if not is_image_captured:
            image_path = None
        else:
            image_path = self.IMAGES_ROOT_DIR_NAME + image_dir + image_name
            # Stores the image in the given image path.
            cv2.imwrite(image_path, image)
        # The camera is released after every capture.
        self.rgb_camera.release()
        # Returns the path where the image is located.
        return image_path

    def stop_camera_feed(self):
        """Releases the camera and stops the feed."""
        self.rgb_camera.release()
        cv2.destroyAllWindows()
