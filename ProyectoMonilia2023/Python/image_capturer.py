import cv2
from time import sleep


class ImageCapturer():
    CAMERA_WINDOW_NAME = "RGB Camera"
    LOT_ID_RGB_CAMERA_PORT = {"L1\n": 0, "L2\n": 3, "L3\n": 2, "L4\n": 1}
    FRAME_WIDTH = 1280
    FRAME_HEIGHT = 960
    IMAGE_FILE_EXTENSION = ".JPG"

    def __init__(self):
        cv2.namedWindow(self.CAMERA_WINDOW_NAME, cv2.WINDOW_NORMAL)
        self.rgb_camera = None

    def try_rgb_image_capture(self, command, image_directory, image_name):
        """Makes at most two attempts to capture the image."""
        is_image_path_ok = True
        image_path = self.capture_rgb_image(command=command, image_directory=image_directory, image_name=image_name)
        if image_path is None:
            # Waits for 1 second and tries to capture the image again.
            sleep(1)
            image_path = self.capture_rgb_image(command=command, image_directory=image_directory, image_name=image_name)
            if image_path is None:
                # After two attempts, it was not possible to capture the image.
                print("After two attempts, it was not possible to capture the image.")
                is_image_path_ok = False
        return is_image_path_ok, image_path

    def capture_rgb_image(self, command, image_directory, image_name):
        """Captures an image and stores it in the given directory under the given name."""
        self.rgb_camera = cv2.VideoCapture(self.LOT_ID_RGB_CAMERA_PORT[command])
        # 3 = frame width (def. 640, max. 1280); 4 = frame height (def. 480, max. 960).
        self.rgb_camera.set(3, self.FRAME_WIDTH)
        self.rgb_camera.set(4, self.FRAME_HEIGHT)
        # Waits for 3 seconds so that the camera focuses.
        sleep(3)
        # Tries to capture the image.
        is_image_captured, image = self.rgb_camera.read()
        if not is_image_captured:
            image_path = None
        else:
            image_path = "{}{}{}".format(image_directory, image_name, self.IMAGE_FILE_EXTENSION)
            # Stores the image in the given image path.
            cv2.imwrite(image_path, image)
        # Releases the camera after every capture.
        self.rgb_camera.release()
        # Returns the path where the image is located.
        return image_path

    def stop_camera_feed(self):
        """Releases the camera and stops the feed."""
        self.rgb_camera.release()
        cv2.destroyAllWindows()

image_capturer = ImageCapturer()
_, image_path = image_capturer.try_rgb_image_capture(command="L1\n",
                                                     image_directory="images/",
                                                     image_name="plant_1")
print(image_path)