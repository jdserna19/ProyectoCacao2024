import RPi.GPIO as GPIO
import time
import shutil
import os
from datetime import datetime
import cv2

# Function to check button press duration
def check_button(pin):
    start_time = time.time()
    while GPIO.input(pin) == GPIO.HIGH:
        pass
    duration = time.time() - start_time
    print(duration)
    return 1 if duration >= 3 else 0

# Function to trigger the motor
def step_motor(pasos, direccion, delay):
    print("Iniciando movimiento del motor")
    GPIO.output(dir_pin, direccion)
    for _ in range(pasos):
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(delay)
    print("Movimiento del motor terminado")

# Configuration of GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pins for button and motor control
pin_button_save = 6
pin_button_read = 5
pin_button_read_2 = 6
Direccion = 12
step_pin = 4
dir_pin = 17
enable_pin = 3
reset = 22
sleep = 23

# Setup pins


# Directories for image handling
source_dir_re = "/media/david/0000-0001/DCIM/Photo"
#source_dir_rgn = "/media/david/0000-00011/DCIM/Photo"
dest_dir = "/home/david/Desktop/pictures"

GPIO.setup(pin_button_save, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_button_read, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_button_read_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
pin = 26  # GPIO pin for triggering the RE and RGN cameras

GPIO.setup(pin, GPIO.OUT)
GPIO.setup(Direccion, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Motor parameters
pasos = 20
delay = 0.005

# Initialize variables
captured_images = []
step_counter = 0
temp = 2

# Main loop
while True:
        

    # Check button to start or stop actions
    if GPIO.input(pin_button_save) == GPIO.HIGH:
        temp = check_button(pin_button_save)
    
    if temp == 0:
        # Trigger the RE and RGN cameras
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.002)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.1)
        print(f"Trigger {step_counter}")

        # Placeholder for capturing image from Logitech camera
        # Example code to capture an image (uncomment if needed)
        # ret, frame = cv2.VideoCapture(0).read()
        # if ret:
        #     timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        #     rgb_filename = f"RGB-step{step_counter}-{timestamp}.png"
        #     rgb_filepath = os.path.join(dest_dir, rgb_filename)
        #     cv2.imwrite(rgb_filepath, frame)
        #     print(f"Captured {rgb_filename}")

        captured_images.append(step_counter)
        step_counter += 1

        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(pin, GPIO.LOW)
        temp = 2
        time.sleep(1)
        GPIO.setup(step_pin, GPIO.OUT)
        GPIO.setup(dir_pin, GPIO.OUT)
        GPIO.setup(enable_pin, GPIO.OUT)
        GPIO.setup(reset, GPIO.OUT)
        GPIO.setup(sleep, GPIO.OUT)

        GPIO.output(enable_pin, GPIO.HIGH)
        GPIO.output(reset, GPIO.HIGH)
        GPIO.output(sleep, GPIO.HIGH) 
        step_motor(pasos, direccion, delay)
        GPIO.cleanup()
        time.sleep(0.1)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_button_save, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(pin_button_read, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(pin_button_read_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(Direccion, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(pin, GPIO.OUT)
    elif temp == 1:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.0015)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.1)
        print("SD Mount/UnMount")

        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(pin, GPIO.LOW)

        time.sleep(7)

        # Transfer and rename RE images
        for step in captured_images:
            files_re = os.listdir(source_dir_re)
            if files_re:
                time.sleep(0.5)
                latest_file_re = max([os.path.join(source_dir_re, f) for f in files_re], key=os.path.getctime)
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                re_filename = f"RE-step{step}-{timestamp}.jpg"
                shutil.move(latest_file_re, os.path.join(dest_dir, re_filename))
                print(f"Transferred {re_filename} to {dest_dir}")
            else:
                print("No RE files found in the source directory.")

            #files_rgn = os.listdir(source_dir_rgn)
            # if files_rgn:
                # time.sleep(0.5)
                # latest_file_rgn = max([os.path.join(source_dir_rgn, f) for f in files_rgn], key=os.path.getctime)
                # timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                # rgn_filename = f"RGN-step{step}-{timestamp}.jpg"
                # shutil.move(latest_file_rgn, os.path.join(dest_dir, rgn_filename))
                # print(f"Transferred {rgn_filename} to {dest_dir}")
            # else:
                # print("No RGN files found in the source directory.")

        captured_images.clear()
        temp = 2
        time.sleep(1)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.0015)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.1)
        print("SD Mount/UnMount")

        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(pin, GPIO.LOW)

        time.sleep(7)
    # Motor control
    if GPIO.input(Direccion) == GPIO.HIGH:
        direccion = 1
    else:
        direccion = 0

    # if GPIO.input(pin_button_read) == GPIO.HIGH:
        # print("motor")
        # step_motor(pasos, direccion, delay)

    time.sleep(0.1)

# Cleanup GPIO

GPIO.cleanup()
