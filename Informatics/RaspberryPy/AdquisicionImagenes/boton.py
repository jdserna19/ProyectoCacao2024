import RPi.GPIO as GPIO
import time

# Configuración del modo de numeración de pines
GPIO.setmode(GPIO.BCM)

# Configuración de los pines
pin_button_read = 5   # Pin para leer el estado
pin_button_read_2 = 6   # Pin para leer el estado
pin_button_save = 12   # Pin para guardar el estado
GPIO.setup(pin_button_read, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_button_read_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_button_save, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variable para guardar el estado del botón
giro = None

try:
    while True:
        # Lee el estado del botón para el giro
        button_read_state = GPIO.input(pin_button_read)
        button_read_state_2 = GPIO.input(pin_button_read_2)
        
        # Guarda el estado en la variable 'giro' si el botón de guardar se presiona
        if GPIO.input(pin_button_save) == GPIO.HIGH:
            giro = button_read_state
            boton =button_read_state_2
            
            print(f"Estado guardado en 'giro': {'Izquierda' if giro == GPIO.LOW else 'Derecha'} {'inicio' if boton == GPIO.LOW else 'apaGAO'}")
            
            time.sleep(0.5)  # Pequeña espera para evitar múltiples lecturas rápidas
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Programa terminado")

finally:
    # Limpia la configuración de GPIO
    GPIO.cleanup()
