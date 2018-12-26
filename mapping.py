import time
import RPi.GPIO as GPIO
from time import sleep
import dcmotor as pwm

import matplotlib.pyplot as plt

def measure():
    GPIO.setmode(GPIO.BCM)
    GPIO_TRIGGER = 4
    GPIO_ECHO    = 18
    GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
    GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.333)
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
numbers=[15,30,45,60,75,90,105,120,135,150,165,180,195,210,225,240,255,270,285,300,315,330,345,360]


for num in numbers:
    if num==360:
        GPIO.cleanup()
        break
    else:
        pwm.left()
        dist=measure()
        print("distance =", dist )
        plt.title('distance over angle')
        
        plt.ylabel('distance')
        plt.xlabel('angle')
        plt.bar(num,dist)
plt.show()
