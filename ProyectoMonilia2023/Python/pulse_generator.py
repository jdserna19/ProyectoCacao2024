import RPi.GPIO as GPIO
import os
from time import time
from time import sleep


class PulseGenerator:
    ENTER_EXIT_USB_TRANSFER_TIME = 10
    CAPTURE_IMAGE_TIME = 10
    
    def __init__(self, rgn_camera_pin, re_camera_pin, pwm_frequency, do_nothing_dc, enter_exit_usb_transfer_dc, 
                 capture_image_dc, rgn_camera_path_indicator, re_camera_path_indicator):
        """Configures all pins references using their pin number, cleans them and sets them PWM signals."""
        GPIO.setwarnings(False)
        self.clean_up()
        self.rgn_camera_pin = rgn_camera_pin
        self.re_camera_pin = re_camera_pin
        self.do_nothing_dc = do_nothing_dc
        self.enter_exit_usb_transfer_dc = enter_exit_usb_transfer_dc
        self.capture_image_dc = capture_image_dc
        self.rgn_camera_path_indicator = rgn_camera_path_indicator
        self.re_camera_path_indicator = re_camera_path_indicator
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.rgn_camera_pin, GPIO.OUT)
        GPIO.setup(self.re_camera_pin, GPIO.OUT)
        GPIO.output(self.rgn_camera_pin, 0)
        GPIO.output(self.re_camera_pin, 0)
        self.rgn_camera = GPIO.PWM(self.rgn_camera_pin, pwm_frequency)
        self.re_camera = GPIO.PWM(self.re_camera_pin, pwm_frequency)
        
    def start_pwm(self):
        """Starts the PWM in order to keep the communication with the multispectral cameras."""
        self.rgn_camera.start(self.do_nothing_dc)
        self.re_camera.start(self.do_nothing_dc)
        
    def enter_exit_usb_transfer(self, multispectral_camera_pin):
        """Activates and deactivates the USB transfer mode of the multispectral camera and waits the necessary time."""
        print("Enter enter_exit")
        if multispectral_camera_pin is self.rgn_camera_pin:
            print("Enter enter_exit RGN")
            self.rgn_camera.ChangeDutyCycle(self.enter_exit_usb_transfer_dc)
            sleep(0.1)
            self.rgn_camera.ChangeDutyCycle(self.do_nothing_dc)
        else:
            print("Enter enter_exit RE")
            self.re_camera.ChangeDutyCycle(self.enter_exit_usb_transfer_dc)
            sleep(0.1)
            self.re_camera.ChangeDutyCycle(self.do_nothing_dc)
        initial_time = time()
        while (time() - initial_time) < self.ENTER_EXIT_USB_TRANSFER_TIME:
            None
        
    def capture_image(self, multispectral_camera_pin):
        """Captures an image using the corresponding multispectral camera and waits the necessary time."""
        if multispectral_camera_pin is self.rgn_camera_pin:
            self.rgn_camera.ChangeDutyCycle(self.capture_image_dc)
            sleep(0.1)
            self.rgn_camera.ChangeDutyCycle(self.do_nothing_dc)
        else:
            self.re_camera.ChangeDutyCycle(self.capture_image_dc)
            sleep(0.1)
            self.re_camera.ChangeDutyCycle(self.do_nothing_dc)
        initial_time = time()
        while (time() - initial_time) < self.CAPTURE_IMAGE_TIME:
            None

    def put_multispectral_cameras_in_capture_mode(self):
        """Makes sure that the multispectral cameras are in capture mode."""
        if os.path.exists(self.rgn_camera_path_indicator):
            self.enter_exit_usb_transfer(self.rgn_camera_pin)
            self.enter_exit_usb_transfer(self.re_camera_pin)
            if os.path.exists(self.re_camera_path_indicator):
                self.enter_exit_usb_transfer(self.re_camera_pin)
        if os.path.exists(self.re_camera_path_indicator):
            self.enter_exit_usb_transfer(self.re_camera_pin)
            self.enter_exit_usb_transfer(self.rgn_camera_pin)
            if os.path.exists(self.rgn_camera_path_indicator):
                self.enter_exit_usb_transfer(self.rgn_camera_pin)

    def generate_pulse(self, multispectral_camera_pin, seconds):
        """Generates a pulse on the given pin during the given time in seconds."""
        initial_time = time()
        while (time() - initial_time) < seconds:
            # Sets the pin to HIGH during the given time.
            GPIO.output(multispectral_camera_pin, 1)
        # Sets the pin to LOW.
        GPIO.output(multispectral_camera_pin, 0)
    
    def clean_up(self):
        """Cleans up all set pins."""
        GPIO.cleanup()

from data_copier import DataCopier

RGN_CAMERA_PIN = 7
RE_CAMERA_PIN = 13
PWM_FREQUENCY = 400
MULTISPECTRAL_CAMERA_DO_NOTHING = 37.6
MULTISPECTRAL_CAMERA_ENTER_EXIT_USB_TRANSFER = 57.6
MULTISPECTRAL_CAMERA_CAPTURE_IMAGE = 77.6
RGN_CAMERA_PATH_INDICATOR = "/media/pi/VOLUME1/DCIM/Photo/rgn.txt"
RE_CAMERA_PATH_INDICATOR = "/media/pi/VOLUME1/DCIM/Photo/re.txt"
RGN_CAMERA_FILES_DIRECTORY = "/media/pi/VOLUME1/DCIM/Photo/"
RE_CAMERA_FILES_DIRECTORY = "/media/pi/VOLUME1/DCIM/Photo/"
MULTISPECTRAL_IMAGES_NAMES = ["rgn", "re"]
data_copier = DataCopier(rgn_camera_files_directory=RGN_CAMERA_FILES_DIRECTORY,
                         re_camera_files_directory=RE_CAMERA_FILES_DIRECTORY,
                         rgn_image_filename=MULTISPECTRAL_IMAGES_NAMES[0],
                         re_image_filename=MULTISPECTRAL_IMAGES_NAMES[1])

pulse_generator = PulseGenerator(rgn_camera_pin=RGN_CAMERA_PIN, re_camera_pin=RE_CAMERA_PIN,
                                 pwm_frequency=PWM_FREQUENCY, do_nothing_dc=MULTISPECTRAL_CAMERA_DO_NOTHING,
                                 enter_exit_usb_transfer_dc=MULTISPECTRAL_CAMERA_ENTER_EXIT_USB_TRANSFER,
                                 capture_image_dc=MULTISPECTRAL_CAMERA_CAPTURE_IMAGE,
                                 rgn_camera_path_indicator=RGN_CAMERA_PATH_INDICATOR,
                                 re_camera_path_indicator=RE_CAMERA_PATH_INDICATOR)

pulse_generator.start_pwm()

initial_time = time()
while (time() - initial_time) < 5:
    None

# TODO Add to master.
# pulse_generator.put_multispectral_cameras_in_capture_mode(RGN_CAMERA_FILES_DIRECTORY + "rgn.txt", RE_CAMERA_FILES_DIRECTORY + "re.txt")

for i in range(1):
    print(i+1)
    print() 
    
    pulse_generator.put_multispectral_cameras_in_capture_mode()
    
    pulse_generator.capture_image(RGN_CAMERA_PIN)
    pulse_generator.capture_image(RE_CAMERA_PIN)
    
    pulse_generator.enter_exit_usb_transfer(RGN_CAMERA_PIN)
   
    multispectral_image_name = MULTISPECTRAL_IMAGES_NAMES[0]
    print(multispectral_image_name)
    _, multispectral_image_path = data_copier \
        .copy_latest_multispectral_image_to_destination(destination_directory="data/",
                                                        multispectral_image_name=multispectral_image_name)
    
    pulse_generator.enter_exit_usb_transfer(RGN_CAMERA_PIN)
    
    pulse_generator.put_multispectral_cameras_in_capture_mode()
    
    pulse_generator.enter_exit_usb_transfer(RE_CAMERA_PIN)
    
    multispectral_image_name = MULTISPECTRAL_IMAGES_NAMES[1]
    print(multispectral_image_name)
    _, multispectral_image_path = data_copier \
        .copy_latest_multispectral_image_to_destination(destination_directory="data/"     ,
                                                        multispectral_image_name=multispectral_image_name)
    
    pulse_generator.enter_exit_usb_transfer(RE_CAMERA_PIN)
  
    print()
pulse_generator.clean_up()   
