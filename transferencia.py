import RPi.GPIO as GPIO
import time
import shutil
import os

GPIO.setwarnings(False)

# Configura el pin para enviar la señal de modo transferencia
pin = 18  # Cambia este número si estás usando otro pin

# Directorios
source_dir = "/media/jdserna/0000-0001/DCIM/Photo"
dest_dir = "/home/jdserna/Desktop/project/capturas"

def send_transfer_signal():
    # Envía la señal de modo transferencia
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.0015)  # Ajusta el tiempo de acuerdo a la especificación del dispositivo
    GPIO.output(pin, GPIO.LOW)
    print("Señal de modo transferencia enviada")
    
    # Limpia la configuración del pin
    GPIO.cleanup()

def transfer_latest_image():
    # Verifica si el directorio fuente existe
    if os.path.exists(source_dir):
        # Filtra y ordena las imágenes JPG por fecha de creación
        jpg_files = sorted(
            [f for f in os.listdir(source_dir) if f.lower().endswith('.jpg')],
            key=lambda x: os.path.getctime(os.path.join(source_dir, x))
        )
        if jpg_files:
            # Selecciona la imagen más reciente
            latest_file = jpg_files[-1]
            # Copia la imagen al directorio de destino
            shutil.copy(os.path.join(source_dir, latest_file), os.path.join(dest_dir, latest_file))
            print(f"Imagen {latest_file} transferida a {dest_dir}")
        else:
            print("No se encontraron imágenes JPG en el directorio.")
    else:
        print(f"El directorio {source_dir} no existe.")

# Envía la señal de modo transferencia
send_transfer_signal()

# Espera unos segundos para asegurarse de que la unidad esté montada
time.sleep(7)

# Transfiere la imagen más reciente
transfer_latest_image()


