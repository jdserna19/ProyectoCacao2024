import RPi.GPIO as GPIO
import time

# Configuration of GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin definitions
UP_BUTTON = 6
SWITCH = 11
STEP_PIN = 4
DIR_PIN = 2
ENABLE_PIN = 3
sleep = 22
reset = 27

# Setup GPIO pins
GPIO.setup(UP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SWITCH, GPIO.IN)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(ENABLE_PIN, GPIO.OUT)
GPIO.setup(sleep, GPIO.OUT)
GPIO.setup(reset, GPIO.OUT)

# Initially disable the motor
GPIO.output(ENABLE_PIN, GPIO.HIGH)
GPIO.output(reset, GPIO.HIGH)

def step_motor(direction, delay):
    
    GPIO.output(DIR_PIN, direction)
    
    GPIO.output(STEP_PIN, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(STEP_PIN, GPIO.LOW)
    time.sleep(delay)

try:
    I = 0
    while True:
        
        direction = GPIO.input(SWITCH)  # Read the direction from the switch
        print(direction)
        if 100000 > I:

            
            GPIO.output(sleep, GPIO.HIGH)
            GPIO.output(ENABLE_PIN, GPIO.LOW)  # Enable the motor
            while 100000 > I: 
                print("b")
                step_motor(direction, 0.0007)  # Adjust delay as needed for desired speed
                I+=1
            GPIO.output(sleep, GPIO.LOW)  # HIGH saca al motor del modo de reposo
        else:
            GPIO.output(sleep, GPIO.LOW)
            GPIO.output(ENABLE_PIN, GPIO.HIGH)
            GPIO.output(sleep, GPIO.HIGH)  # Disable the motor when button is not pressed
        
        time.sleep(0.01)  # Small delay to prevent CPU hogging

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    GPIO.output(ENABLE_PIN, GPIO.HIGH)  # Ensure motor is disabled
    GPIO.cleanup()
    print("GPIO cleaned up")
