import RPi.GPIO as GPIO
import time
import shutil
import os
from datetime import datetime
import cv2  

GPIO.setwarnings(False)

pin = 18  # GPIO pin for triggering the RE and RGN cameras
logitech_cam_index = 0  

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
time.sleep(0.001)
GPIO.cleanup()

print("\nCommands:")
print("t + Enter: Trigger both cameras")
print("s + Enter: SD Card Mount/UnMount (1500us) and Transfer Images")
print("e + Enter: Exit\n")

# Define the source and destination directories
source_dir_re = "/media/jdserna/0000-0001/DCIM/Photo"
source_dir_rgn = "/media/jdserna/0000-00011/DCIM/Photo"
dest_dir = "/home/jdserna/Desktop/project/capturas"

step_counter = 0  # Initialize the step counter

# List to store captured image paths
captured_images = []

# Initialize the Logitech camera
logitech_cam = cv2.VideoCapture(logitech_cam_index)

while True:
    key = input(">")
    if key == "t":
        # Trigger the RE and RGN cameras
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.002)
        GPIO.cleanup()

        time.sleep(0.1)
        print(f"Trigger {step_counter}")

        # Capture image from the Logitech camera
        ret, frame = logitech_cam.read()
        if ret:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            rgb_filename = f"RGB-step{step_counter}-{timestamp}.png"
            rgb_filepath = os.path.join(dest_dir, rgb_filename)
            cv2.imwrite(rgb_filepath, frame)
            print(f"Captured {rgb_filename}")

        # After triggering, the RE and RGN cameras capture an image
        captured_images.append(step_counter)  # Add the step to the captured_images list
        step_counter += 1  # Increment the step counter

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        time.sleep(0.001)
        GPIO.cleanup()

    elif key == "s":
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.0015)
        GPIO.cleanup()

        time.sleep(0.1)
        print("SD Mount/UnMount")

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        time.sleep(0.001)
        GPIO.cleanup()

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

    elif key == "e":
        # Release the Logitech camera
        logitech_cam.release()
        print("Exiting\n")
        break

    else:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        time.sleep(0.001)
        GPIO.cleanup()
