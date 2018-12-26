import RPi.GPIO as gpio
import time
 
def init():
 gpio.setmode(gpio.BCM)
 gpio.setup(17, gpio.OUT)
 gpio.setup(22, gpio.OUT)
 gpio.setup(23, gpio.OUT)
 gpio.setup(24, gpio.OUT)
## p= gpio.PWM(17,50)
## q= gpio.PWM(22,50)
## r= gpio.PWM(23,50)
## s= gpio.PWM(24,50)
def forward():
 init()
 gpio.output(17, False)
 gpio.output(22, True)
 gpio.output(23, True) 
 gpio.output(24, False)
## time.sleep(tf)
## gpio.cleanup()
 
def reverse():
 init()
 gpio.output(17, True)
 gpio.output(22, False)
 gpio.output(23, False) 
 gpio.output(24, True)
## time.sleep(tf)
## gpio.cleanup()
 
def left():
 init()
 gpio.output(17, False)
 gpio.output(22, True)
 gpio.output(23, False) 
 gpio.output(24, False)
## time.sleep(tf)
## gpio.cleanup() 

def right():
 init()
 gpio.output(17, False)
 gpio.output(22, False)
 gpio.output(23, True) 
 gpio.output(24, False)
## time.sleep()
## gpio.cleanup()

def stop():
 init()
 gpio.output(17, False)
 gpio.output(22, False)
 gpio.output(23, False) 
 gpio.output(24, False)
## time.sleep()
## gpio.cleanup()


def stopsign(tf):
 init()
 gpio.output(17, False)
 gpio.output(22, False)
 gpio.output(23, False) 
 gpio.output(24, False)
 time.sleep(tf)
## gpio.cleanup()
 
 
def a(tf):
 init()
 gpio.output(17, False)
 gpio.output(22, True)
 gpio.output(23, False) 
 gpio.output(24, False)
 time.sleep(tf)
 gpio.cleanup()
 
 

def d(tf):
 init()
 gpio.output(17, False)
 gpio.output(22, False)
 gpio.output(23, True) 
 gpio.output(24, False)
 time.sleep(tf)
 gpio.cleanup()
 
 

def w(tf):
 init()
 gpio.output(17, False)
 gpio.output(22, True)
 gpio.output(23, True) 
 gpio.output(24, False)
 time.sleep(tf)
 gpio.cleanup()
 
 

def r(tf):
 init()
 gpio.output(17, True)
 gpio.output(22, False)
 gpio.output(23, False) 
 gpio.output(24, True)
 time.sleep(tf)
 gpio.cleanup()
 
 
