import time
import RPi.GPIO as GPIO
from time import sleep
def measure():
    GPIO.setmode(GPIO.BCM)
    GPIO_TRIGGER = 4
    GPIO_ECHO    = 18
    GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
    GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo
##    GPIO.output(GPIO_TRIGGER, False)
##    time.sleep(0.333)
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()
    while GPIO.input(GPIO_ECHO)==0:
      start = time.time()
    while GPIO.input(GPIO_ECHO)==1:
      stop = time.time()
    elapsed = stop-start
    distance = elapsed * 17150
    distance = round(distance, 2)
    return distance
    GPIO.cleanup()