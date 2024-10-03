import RPi.GPIO as GPIO
import time

# Configuración del modo de numeración de pines
GPIO.setmode(GPIO.BCM)

# Configuración de los pines
# Botón para iniciar movimiento de motor
pin_button_read = 5   # Pin para leer el estado
pin_button_read_2 = 6   # Pin para leer el estado

# Interruptor para conocer el sentido de giro
Direccion = 12   # Pin para guardar el estado

# Definimos los pines a utilizar
step_pin = 4
dir_pin = 2
enable_pin = 18
reset = 22
sleep = 10

# Configuración pines
GPIO.setup(step_pin, GPIO.OUT)
GPIO.setup(enable_pin, GPIO.OUT)
GPIO.output(enable_pin, GPIO.LOW)
GPIO.setup(pin_button_read, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Direccion, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_button_read_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sleep, GPIO.OUT)
# Configuración pines
GPIO.setmode(GPIO.BCM)
GPIO.setup(step_pin, GPIO.OUT)
GPIO.setup(dir_pin, GPIO.OUT)
GPIO.setup(enable_pin, GPIO.OUT)
GPIO.output(enable_pin, GPIO.LOW)  # Habilitar el motor
GPIO.setup(reset, GPIO.OUT)
GPIO.output(reset, GPIO.LOW)  
GPIO.output(reset, GPIO.HIGH) 
GPIO.setup(sleep, GPIO.OUT)
GPIO.output(sleep, GPIO.LOW)  
GPIO.output(sleep, GPIO.HIGH) 

# Número de pasos y velocidad de motor (esto es medio estándar, así que)
pasos = 10
delay = 0.1  # Esto es el tiempo que debe demorar un paso

# Variable para guardar el estado del botón
giro = None


# Función para girar el motor
def step_motor(pasos, direccion, delay):
    print("Iniciando movimiento del motor")
    GPIO.output(dir_pin, direccion)
    for i in range(pasos):
        # Activa el motor y lo deja operar por el tiempo de pasos
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(delay)
        
        # Desactiva el motor y espera un momento
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(delay)
    print("Movimiento del motor terminado")


while True:
	# Lee el estado del botón para el giro
	print("esperando boton")
	if(GPIO.input(Direccion)==GPIO.HIGH):
		direccion=1
		print("1")
	else:
		direccion=0
	# Guarda el estado en la variable 'giro' si el botón de guardar se presiona
	if GPIO.input(pin_button_read) == GPIO.HIGH:  # Cambiado de pin_button_save a pin_button_read
		print( "motor" )
		step_motor(pasos, direccion,delay)
	time.sleep(0.1)
GPIO.cleanup()
