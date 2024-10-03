import RPi.GPIO as GPIO
import time

# Definimos los pines a utilizar
step_pin = 4
dir_pin = 2
enable_pin = 3
reset = 22
sleep = 23

# Configuración pines
GPIO.setmode(GPIO.BCM)
GPIO.setup(step_pin, GPIO.OUT)
GPIO.setup(dir_pin, GPIO.OUT)
GPIO.setup(enable_pin, GPIO.OUT)
  # Habilitar el motor
GPIO.setup(reset, GPIO.OUT)
GPIO.setup(sleep, GPIO.OUT)
GPIO.output(enable_pin, GPIO.HIGH)
GPIO.output(reset, GPIO.HIGH)
GPIO.output(sleep, GPIO.HIGH) 

time.sleep(0.1)
 
# Dirección del motor (0 o 1 según el sentido deseado)
direccion = 1
  # Cambia esto a 0 o 1 según necesites

# Número de pasos y velocidad del motor
pasos = 1
delay = 0.005 # Tiempo que debe demorar un paso

# Función para girar el motor
def step_motor(pasos, direccion, delay):
    print("Iniciando movimiento del motor")
    if(direccion == 1):
        GPIO.output(dir_pin, GPIO.HIGH)
    else:
        GPIO.output(dir_pin, GPIO.LOW)
    for i in range(pasos):
        # Activa el motor y lo deja operar por el tiempo de pasos
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(delay)
        
        # Desactiva el motor y espera un momento
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(delay)
    print("Movimiento del motor terminado")

# Llamamos a la función para mover el motor
try:
    step_motor(pasos, direccion, delay)
finally:
    # Limpia los pines GPIO y termina el proceso
    GPIO.cleanup()
    print("GPIO limpiado y programa terminado")
