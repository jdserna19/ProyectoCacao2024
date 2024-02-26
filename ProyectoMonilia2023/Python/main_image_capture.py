from image_capture import ImageCapture
from time import sleep

NUMBER_OF_IMAGES = 4

# Creates a new directory according to the current date and time, captures 
# some images and stores them in the created directory.
image_capture = ImageCapture()
image_dir = image_capture.create_image_dir()
print("Directory {} created.".format(image_dir))
for i in range(NUMBER_OF_IMAGES):
    image_name = "image_{}.png".format(str(i + 1))
    image_path = image_capture.capture_rgb_image(image_dir=image_dir, 
                                                 image_name=image_name)
    print("{} stored in {}.".format(image_name, image_path))
    sleep(3)
image_capture.stop_camera_feed()
