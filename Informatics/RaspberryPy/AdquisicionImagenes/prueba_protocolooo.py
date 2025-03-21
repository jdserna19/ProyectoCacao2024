import RPi.GPIO as GPIO
import time
import shutil
import os
from datetime import datetime
import cv2
reinicio = 0
while reinicio == 0:
        try:
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
                        GPIO.output(enable_pin, GPIO.LOW)  # Deshabilita el motor cuando no está en uso
                        print("Iniciando movimiento del motor")
                        if(direccion == 1):
                                GPIO.output(dir_pin, GPIO.LOW)
                        else:
                                GPIO.output(dir_pin, GPIO.HIGH)
                        for i in range(pasos):
                                # Activa el motor y lo deja operar por el tiempo de pasos
                                GPIO.output(step_pin, GPIO.LOW)
                                time.sleep(delay)
                        
                                # Desactiva el motor y espera un momento
                                GPIO.output(step_pin, GPIO.HIGH)
                                time.sleep(delay)
                        print("Movimiento del motor terminado")

                # Configuration of GPIO pins
                GPIO.setmode(GPIO.BCM)
                GPIO.setwarnings(False)
                logitech_cam_index = 0  
                # Pins for button and motor control
                up_button = 6
                Down_button = 13
                switch = 11
                Direccion = 12
                step_pin =  4
                dir_pin = 2
                enable_pin = 3
                reset = 27
                sleep = 22


                # Directories for image handling
                source_dir_re = "/media/lcd/0000-0001/DCIM/Photo"
                source_dir_rgn = "/media/lcd/0000-0001/DCIM/Photo"
                dest_dir = "/home/lcd/Desktop/pictures"

                GPIO.setup(up_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.cleanup()

                GPIO.setmode(GPIO.BCM)
                GPIO.setwarnings(False)
                GPIO.setup(up_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(Down_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                pin = 26  # GPIO pin for triggering the RE and RGN cameras
                pin_2 = 16

                GPIO.setup(pin, GPIO.OUT)
                GPIO.setup(pin_2, GPIO.OUT)
                GPIO.setup(Direccion, GPIO.IN, pull_up_down=GPIO.PUD_UP)

                GPIO.setup(step_pin, GPIO.OUT)
                GPIO.setup(dir_pin, GPIO.OUT)
                GPIO.setup(enable_pin, GPIO.OUT)
                GPIO.setup(reset, GPIO.OUT)
                GPIO.setup(sleep, GPIO.OUT)

                # Habilitar motor antes de iniciar el movimiento
                GPIO.output(enable_pin, GPIO.HIGH)  
                GPIO.output(reset, GPIO.LOW)  
                GPIO.output(sleep, GPIO.LOW)  
                GPIO.output(enable_pin, GPIO.LOW)  # LOW habilita el motor
                GPIO.output(reset, GPIO.HIGH)  # HIGH saca al motor del estado de reset
                GPIO.output(sleep, GPIO.HIGH)  # HIGH saca al motor del modo de reposo
                # Motor parameters
                pasos = 50
                delay = 0.0006 # Tiempo que debe demorar un paso

                # Initialize variables
                captured_images = []
                step_counter = 0
                temp = 2



                # Main loop
                k=1
                while True:
                        print("en estas andamos")
                        if k == 1:
                                try:
                                        logitech_cam = cv2.VideoCapture(0)
                                        k=0
                                except:
                                        k=1
                        b=0    
                        print("esperando comando")
                        if GPIO.input(switch) == GPIO.HIGH:
                                        lao = 1
                        else:
                                        lao = 0
                        # Check button to start or stop actions
                        if GPIO.input(up_button) == GPIO.HIGH:
                                a=0
                        time.sleep(1)
                        if GPIO.input(up_button) == GPIO.LOW:
                                a=1
                        
                        if not logitech_cam.isOpened():
                            print("Error: No se pudo abrir la cámara Logitech.")
                        else:
                            print("Cámara Logitech abierta con éxito.")

                        while a==0:
                                try:
                                        # Trigger the RE and RGN cameras
                                        GPIO.output(pin, GPIO.HIGH)
                                        GPIO.output(pin_2, GPIO.HIGH)
                                        time.sleep(0.002)
                                        GPIO.output(pin, GPIO.LOW)
                                        GPIO.output(pin_2, GPIO.LOW)
                                        time.sleep(1)
                                        print(f"Trigger {step_counter}")

                                        # Placeholder for capturing image from Logitech camera
                                        #Example code to capture an image (uncomment if needed)
                                        ret, frame = logitech_cam.read()
                                        if ret:
                                                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                                                rgb_filename = f"RGB-step{step_counter}-{timestamp}.png"
                                                rgb_filepath = os.path.join(dest_dir, rgb_filename)
                                                cv2.imwrite(rgb_filepath, frame)

                                        captured_images.append(step_counter)
                                        step_counter += 1
                                        GPIO.output(pin, GPIO.LOW)
                                        GPIO.output(pin, GPIO.HIGH)
                                        GPIO.output(pin_2, GPIO.LOW)
                                        GPIO.output(pin_2, GPIO.HIGH)
                                        time.sleep(0.001)
                                        GPIO.output(pin, GPIO.LOW)
                                        GPIO.output(pin_2, GPIO.LOW)

                                        time.sleep(1)
                                        
                                        GPIO.output(enable_pin, GPIO.HIGH)
                                        GPIO.output(enable_pin, GPIO.LOW)
                                        GPIO.output(reset, GPIO.LOW)
                                        GPIO.output(sleep, GPIO.LOW)
                                        GPIO.output(reset, GPIO.HIGH)
                                        GPIO.output(sleep, GPIO.HIGH)
                                        step_motor(pasos, lao, delay)
                                        b= b+1

                                        time.sleep(1)
                                        print("antes de terminar el ciclo")
                                        if GPIO.input(Down_button) == GPIO.HIGH or b==4:
                                                a=1
                                                time.sleep(1)
                                                if GPIO.input(switch) == GPIO.HIGH:
                                                        lao = 0
                                                else:
                                                        lao = 1
                                                GPIO.output(enable_pin, GPIO.HIGH)
                                                GPIO.output(enable_pin, GPIO.LOW)
                                                GPIO.output(reset, GPIO.LOW)
                                                GPIO.output(sleep, GPIO.LOW)
                                                GPIO.output(reset, GPIO.HIGH)
                                                GPIO.output(sleep, GPIO.HIGH)
                                                step_motor(b*pasos, lao, delay)
                                                GPIO.output(sleep, GPIO.LOW)
                                                GPIO.output(enable_pin, GPIO.LOW)
                                                b=0
                                                GPIO.output(pin, GPIO.LOW)
                                                
                                                GPIO.output(pin, GPIO.HIGH)
                                                time.sleep(0.0015)
                                                GPIO.output(pin, GPIO.LOW)
                                                time.sleep(7)
                                                GPIO.output(pin, GPIO.HIGH)
                                                time.sleep(0.001)
                                                GPIO.output(pin, GPIO.LOW)
                                                time.sleep(1)
                                                
                                                # Transfer and rename all captured RE images
                                                for step in captured_images:
                                                    files_re = os.listdir(source_dir_re)
                                                    if files_re:
                                                        # Adding a small delay to ensure the file is completely written
                                                        time.sleep(1)
                                                        latest_file_re = max([os.path.join(source_dir_re, f) for f in files_re], key=os.path.getctime)

                                                        # Generate the new filename
                                                        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                                                        re_filename = f"RE-step{step}-{timestamp}.jpg"

                                                        # Move and rename the file
                                                        shutil.move(latest_file_re, os.path.join(dest_dir, re_filename))
                                                        print(f"Transferred {re_filename} to {dest_dir}")
                                                        # Eliminar el archivo original si se desea una limpieza adicional
                                                        if os.path.exists(latest_file_re):
                                                            os.remove(latest_file_re)
                                                            print(f"Deleted {latest_file_re}")
                                                        step_counter = 0
                                                GPIO.output(pin_2, GPIO.HIGH)
                                                time.sleep(0.001)
                                                GPIO.output(pin_2, GPIO.LOW)
                                                time.sleep(1)
                                                GPIO.output(pin, GPIO.HIGH)
                                                time.sleep(0.0015)
                                                GPIO.output(pin, GPIO.LOW)
                                                time.sleep(2)
                                                GPIO.output(pin_2, GPIO.HIGH)
                                                time.sleep(0.0015)
                                                GPIO.output(pin_2, GPIO.LOW)
                                                time.sleep(10)
                                                GPIO.output(pin_2, GPIO.HIGH)
                                                time.sleep(0.001)
                                                GPIO.output(pin_2, GPIO.LOW)
                                                time.sleep(10)
                                                for step in captured_images:
                                                        
                                                        # Transfer and rename all captured RE images
                                                        files_re = os.listdir(source_dir_rgn)
                                                        if files_re:
                                                                # Adding a small delay to ensure the file is completely written
                                                                time.sleep(1)
                                                                latest_file_re = max([os.path.join(source_dir_re, f) for f in files_re], key=os.path.getctime)

                                                                # Generate the new filename
                                                                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                                                                re_filename = f"RGN-step{step}-{timestamp}.jpg"

                                                                # Move and rename the file
                                                                shutil.move(latest_file_re, os.path.join(dest_dir, re_filename))
                                                                print(f"Transferred {re_filename} to {dest_dir}")
                                                                # Eliminar el archivo original si se desea una limpieza adicional
                                                                if os.path.exists(latest_file_re):
                                                                    os.remove(latest_file_re)
                                                                    print(f"Deleted {latest_file_re}")
                                                                else:
                                                                        print("No RGN files found in the source directory.")
                                                        
                                                                step_counter = 0
                                                                GPIO.output(pin_2, GPIO.HIGH)
                                                                time.sleep(0.001)
                                                                GPIO.output(pin_2, GPIO.LOW)
                                                                time.sleep(1)
                                                                GPIO.output(pin_2, GPIO.HIGH)
                                                                time.sleep(0.0015)
                                                                GPIO.output(pin_2, GPIO.LOW)
                                                                time.sleep(2)
                                                                GPIO.output(enable_pin, GPIO.LOW)  # Deshabilita el motor cuando no está en uso
                                                captured_images=[]                        
                                        print("e el ciclo")
                                except:
                                        GPIO.cleanup()
        except:
                iguana = 0
