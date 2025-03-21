import RPi.GPIO as GPIO
import time
import shutil
import os
from datetime import datetime
import cv2

# Configuración de constantes
logitech_cam_index = 0  # Cambia esto a 1 si tu cámara está en /dev/video1
pin_button_save = 6
pin_button_read = 5
pin_button_read_2 = 13
Direccion = 12
step_pin = 4
dir_pin = 2
enable_pin = 3
reset = 22
sleep = 23
pin = 26  # Pin de disparo para las cámaras RE y RGN
source_dir_re = "/media/david/0000-0001/DCIM/Photo"
source_dir_rgn = "/media/david/0000-00011/DCIM/Photo"
dest_dir = "/home/lcd/Desktop/pictures"
pasos = 50
delay = 0.0006

# Configurar la numeración de pines
GPIO.setmode(GPIO.BCM)  # Establece el modo de numeración BCM
GPIO.setwarnings(False)

# Configurar pines del motor
GPIO.setup(step_pin, GPIO.OUT)
GPIO.setup(dir_pin, GPIO.OUT)
GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(reset, GPIO.OUT)
GPIO.setup(sleep, GPIO.OUT)
# Habilitar motor antes de iniciar el movimiento
GPIO.output(enable_pin, GPIO.LOW)  # LOW habilita el motor
GPIO.output(reset, GPIO.HIGH)  # HIGH saca al motor del estado de reset
GPIO.output(sleep, GPIO.HIGH)  # HIGH saca al motor del modo de reposo

# Configurar pines de los botones
GPIO.setup(pin_button_save, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_button_read, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_button_read_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Direccion, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Configurar pin de disparo de las cámaras RE y RGN
GPIO.setup(pin, GPIO.OUT)

# Función para limpiar los recursos al finalizar
def cleanup(logitech_cam):
    logitech_cam.release()
    GPIO.cleanup()

# Función para mover el motor paso a paso
def step_motor(pasos, direccion, delay):
    print("Iniciando movimiento del motor")
    GPIO.output(dir_pin, GPIO.LOW if direccion == 1 else GPIO.HIGH)
    for i in range(pasos):
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(delay)
    print("Movimiento del motor terminado")

# Función para capturar imágenes
def capture_images(step_counter, dest_dir, logitech_cam):
    # Disparar las cámaras RE y RGN
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.002)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(1)
    
    # Capturar desde la cámara Logitech
    ret, frame = logitech_cam.read()
    if ret:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        rgb_filename = f"RGB-step{step_counter}-{timestamp}.png"
        rgb_filepath = os.path.join(dest_dir, rgb_filename)
        cv2.imwrite(rgb_filepath, frame)
        print(f"Captured {rgb_filename}")
    else:
        print("Error: No se pudo capturar la imagen de la cámara Logitech.")

# Función para transferir imágenes de las cámaras RE y RGN
def transfer_images(step, source_dir_re, source_dir_rgn, dest_dir):
    # Transferir imágenes de la cámara RE
    if os.path.exists(source_dir_re):
        files_re = os.listdir(source_dir_re)
        if files_re:
            latest_file_re = max([os.path.join(source_dir_re, f) for f in files_re], key=os.path.getctime)
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            re_filename = f"RE-step{step}-{timestamp}.jpg"
            shutil.move(latest_file_re, os.path.join(dest_dir, re_filename))
            print(f"Transferred {re_filename} to {dest_dir}")
        else:
            print(f"No se encontraron archivos en {source_dir_re}.")
    else:
        print(f"Error: El directorio {source_dir_re} no existe.")

    # Transferir imágenes de la cámara RGN
    if os.path.exists(source_dir_rgn):
        files_rgn = os.listdir(source_dir_rgn)
        if files_rgn:
            latest_file_rgn = max([os.path.join(source_dir_rgn, f) for f in files_rgn], key=os.path.getctime)
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            rgn_filename = f"RGN-step{step}-{timestamp}.jpg"
            shutil.move(latest_file_rgn, os.path.join(dest_dir, rgn_filename))
            print(f"Transferred {rgn_filename} to {dest_dir}")
        else:
            print(f"No se encontraron archivos en {source_dir_rgn}.")
    else:
        print(f"Error: El directorio {source_dir_rgn} no existe.")

# Lógica principal del protocolo
def start_capture_protocol():
    step_counter = 0
    total_steps = 0  # Para llevar el control del número de pasos realizados

    # Inicializar la cámara Logitech
    logitech_cam = cv2.VideoCapture(logitech_cam_index)
    if not logitech_cam.isOpened():
        print("Error: No se pudo abrir la cámara Logitech.")
        return

    try:
        while True:
            if GPIO.input(pin_button_save) == GPIO.HIGH:
                time.sleep(1)  # Pausa para evitar rebotes

                if GPIO.input(pin_button_save) == GPIO.HIGH:  # Verificar si el botón sigue presionado
                    a = 0

                    while a == 0:
                        capture_images(step_counter, dest_dir, logitech_cam)
                        transfer_images(step_counter, source_dir_re, source_dir_rgn, dest_dir)

                        # Mover motor paso a paso en dirección normal
                        lao = 1 if GPIO.input(pin_button_read_2) == GPIO.HIGH else 0
                        step_motor(pasos, lao, delay)
                        total_steps += pasos

                        step_counter += 1
                        time.sleep(2)  # Pausa entre capturas

                        if GPIO.input(pin_button_read) == GPIO.HIGH or step_counter == 4:
                            a = 1
                            break

                    # Regresar a la posición inicial invirtiendo la dirección del motor
                    print(f"Regresando motor a la posición inicial ({total_steps} pasos)")
                    step_motor(total_steps, not lao, delay)  # Invertir dirección
                    total_steps = 0  # Reiniciar el contador de pasos

            time.sleep(0.1)  # Evitar consumo excesivo de CPU

    finally:
        cleanup(logitech_cam)

# Ejecutar el protocolo
start_capture_protocol()
