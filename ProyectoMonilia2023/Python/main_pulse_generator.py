import RPi.GPIO as GPIO
from time import time
from time import sleep


GPIO.setmode(GPIO.BOARD)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)
GPIO.output(33, 0)
GPIO.output(40, 0)
p_1 = GPIO.PWM(33, 400)
p_2 = GPIO.PWM(40, 400)
p_1.start(37.6)
p_2.start(37.6)

'''
p_1.ChangeDutyCycle(77.6)
sleep(0.1)
p_1.ChangeDutyCycle(37.6)
initial_time = time()
while (time() - initial_time) < 2:
    None
p_2.ChangeDutyCycle(77.6)
sleep(0.1)
p_2.ChangeDutyCycle(37.6)
initial_time = time()
while (time() - initial_time) < 2:
    None
'''

p_1.ChangeDutyCycle(57.6)
sleep(0.1)
p_1.ChangeDutyCycle(37.6)
initial_time = time()
while (time() - initial_time) < 5:
    None
print("CAM 1 IN USB TRANSFER MODE")
# Copy image here.
p_1.ChangeDutyCycle(57.6)
sleep(0.1)
p_1.ChangeDutyCycle(37.6)
initial_time = time()
while (time() - initial_time) < 5:
    None
print("CAM 1 IN USB EXIT MODE")

p_2.ChangeDutyCycle(57.6)
sleep(0.1)
p_2.ChangeDutyCycle(37.6)
initial_time = time()
while (time() - initial_time) < 5:
    None
print("CAM 2 IN USB TRANSFER MODE")
p_2.ChangeDutyCycle(57.6)
sleep(0.1)
p_2.ChangeDutyCycle(37.6)
initial_time = time()
while (time() - initial_time) < 5:
    None
print("CAM 2 IN USB EXIT MODE")