import RPi.GPIO as GPIO
import time
import shutil
import os
from datetime import datetime
import cv2  

def check_button():
    start_time = time.time()
    while GPIO.input(pin_button_save) == GPIO.HIGH:
        pass
    duration = time.time() - start_time
    print(duration)
    duration = float(duration)
    if duration >= 3:
        temp = 1
    else:
        print("entró a esto")
        temp = 0
    return temp    
        
# Configuración del modo de numeración de pines
GPIO.setmode(GPIO.BCM)

pin_button_save = 6   # Pin para guardar el estado
GPIO.setup(pin_button_save, GPIO.IN, pull_up_down=GPIO.PUD_UP)


GPIO.setwarnings(False)

pin = 26  # GPIO pin for triggering the RE and RGN cameras

GPIO.setup(pin, GPIO.OUT)
time.sleep(0.001)

temp = 2

# Define the source and destination directories
source_dir_re = "/media/david/0000-0001/DCIM/Photo"
source_dir_rgn = "/media/david/0000-00011/DCIM/Photo"
dest_dir = "/home/david/Desktop/pictures"

step_counter = 0  # Initialize the step counter

# List to store captured image paths
captured_images = []


while True:
    if GPIO.input(pin_button_save) == GPIO.HIGH:
            temp= check_button()
    if temp == 0:
        # Trigger the RE and RGN cameras
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.002)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.1)
        print(f"Trigger {step_counter}")

        # Capture image from the Logitech camera
        # if ret:
            # timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            # rgb_filename = f"RGB-step{step_counter}-{timestamp}.png"
            # rgb_filepath = os.path.join(dest_dir, rgb_filename)
            # cv2.imwrite(rgb_filepath, frame)
            # print(f"Captured {rgb_filename}")

        # After triggering, the RE and RGN cameras capture an image
        
        captured_images.append(step_counter)  # Add the step to the captured_images list
        step_counter += 1  # Increment the step counter
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(pin, GPIO.LOW)
        temp = 2
        time.sleep(1)
    elif temp == 1:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.0015)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.1)
        print("SD Mount/UnMount")

        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(pin, GPIO.LOW)

        # Wait 7 seconds before transferring the images, (raspi3)
        time.sleep(7)

        # Transfer and rename all captured RE images
        for step in captured_images:
            files_re = os.listdir(source_dir_re)
            if files_re:
                # Adding a small delay to ensure the file is completely written
                time.sleep(0.5)
                latest_file_re = max([os.path.join(source_dir_re, f) for f in files_re], key=os.path.getctime)

                # Generate the new filename
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                re_filename = f"RE-step{step}-{timestamp}.jpg"

                # Move and rename the file
                shutil.move(latest_file_re, os.path.join(dest_dir, re_filename))
                print(f"Transferred {re_filename} to {dest_dir}")
            else:
                print("No RE files found in the source directory.")

            files_rgn = os.listdir(source_dir_rgn)
            if files_rgn:
                # Adding a small delay to ensure the file is completely written
                time.sleep(0.5)
                latest_file_rgn = max([os.path.join(source_dir_rgn, f) for f in files_rgn], key=os.path.getctime)

                # Generate the new filename
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                rgn_filename = f"RGN-step{step}-{timestamp}.jpg"

                # Move and rename the file
                shutil.move(latest_file_rgn, os.path.join(dest_dir, rgn_filename))
                print(f"Transferred {rgn_filename} to {dest_dir}")
            else:
                print("No RGN files found in the source directory.")

        # Clear the captured_images list after transfer
        captured_images.clear()
        temp = 2
        time.sleep(1)

