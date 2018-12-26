from bluedot import BlueDot
from signal import pause
 
import time, RPi.GPIO as GPIO
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
 
def dpad(pos):
    if pos.top:
        print("Forward")
        GPIO.output (22, 1)
        GPIO.output (23, 1)
        GPIO.output (17, 0)
        GPIO.output (24, 0)
 
    elif pos.bottom:
        print("down")
        GPIO.output (22, 0)
        GPIO.output (23, 0)
        GPIO.output (17, 1)
        GPIO.output (24, 1)        
 
    elif pos.left:
        print("left")
        GPIO.output (22, 1)
        GPIO.output (17, 0)
        GPIO.output (23, 0)
        GPIO.output (24, 0)
        
    elif pos.right:
        print("right")
        GPIO.output (22, 0)
        GPIO.output (17, 0)
        GPIO.output (23, 1)
        GPIO.output (24, 0)
        
    elif pos.middle:
        print("STOP")
        GPIO.output (17, 0)
        GPIO.output (22, 0)
        GPIO.output (24, 0)
        GPIO.output (23, 0)
        
 
bd = BlueDot()
bd.when_pressed = dpad
 
pause()
