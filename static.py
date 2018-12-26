import RPi.GPIO as gpio
import time
import dcmotor as pwm
import obstacleAvoid as umeasure



gpio.setwarnings(False)
def ab():
    stop=0
    d=0
    while(True):
        distance = umeasure.measure()
        print("distance ", distance)
        if distance <20:
            pwm.stop()
##            pwm.reverse()
##            time.sleep(1)
##            pwm.right()
##            time.sleep(1.5)
##            pwm.forward()
##            time.sleep(1)
##            pwm.stop()
##            time.sleep(1)
##            pwm.left()
##            time.sleep(1.5)
##            d=1
        else:
            pwm.forward()
            stop= stop+1
            if stop== 200:
                pwm.stop()
                time.sleep(1)
                pwm.left()
                time.sleep(1.6)
            if stop== 400:
                pwm.stop()
                time.sleep(1)
                pwm.right()
                time.sleep(1.6)
            if stop== 600:
                pwm.stop()
                time.sleep(1)
                pwm.right()
                time.sleep(1.6)
            if stop== 800:
                pwm.stop()
                time.sleep(1)
                pwm.left()
                time.sleep(1.6)
            if stop == 1000:
                print("Reached b") 
                pwm.stop()
                break
def bc():
    l=0
    stop=0
    while (True):
        distance = umeasure.measure()
        print("distance ", distance)
        if distance <20:
            pwm.stop()
        else:
                        
            if l==0:
                pwm.left()
                time.sleep(1.6)
                l=1
            else:
                pwm.forward()
                stop= stop+1
                if stop== 200:
                    pwm.stop()
                    time.sleep(1)
                    pwm.left()
                    time.sleep(1.6)
                if stop== 400:
                    pwm.stop()
                    time.sleep(1)
                    pwm.right()
                    time.sleep(1.6)
                if stop== 600:
                    pwm.stop()
                    time.sleep(1)
                    pwm.right()
                    time.sleep(1.6)
                if stop== 800:
                    pwm.stop()
                    time.sleep(1)
                    pwm.left()
                    time.sleep(1.6)
                if stop == 1000:
                    print("Reached c")
                    pwm.stop()
                    break
                
def cb():
    stop=0
    while(True):
        distance = umeasure.measure()
        print("distance ", distance)
        if distance <20:
            pwm.stop()
        else:
            pwm.forward()
            stop= stop+1
            if stop== 200:
                pwm.stop()
                time.sleep(1)
                pwm.right()
                time.sleep(1.6)
            if stop== 400:
                pwm.stop()
                time.sleep(1)
                pwm.left()
                time.sleep(1.6)
            if stop== 600:
                pwm.stop()
                time.sleep(1)
                pwm.left()
                time.sleep(1.6)
            if stop== 800:
                pwm.stop()
                time.sleep(1)
                pwm.right()
                time.sleep(1.6)
            if stop == 1000:
                print("Reached b")
                pwm.stop()
                break
def ba():
    stop=0
    l=0
    while (True):
        distance = umeasure.measure()
        print("distance ", distance)
        if distance <20:
            pwm.stop()
        else:
                        
            if l==0:
                pwm.right()
                time.sleep(1.6)
                l=1
            else:
                pwm.forward() 
                stop= stop+1
                if stop== 200:
                    pwm.stop()
                    time.sleep(1)
                    pwm.right()
                    time.sleep(1.6)
                if stop== 400:
                    pwm.stop()
                    time.sleep(1)
                    pwm.left()
                    time.sleep(1.6)
                if stop== 600:
                    pwm.stop()
                    time.sleep(1)
                    pwm.left()
                    time.sleep(1.6)
                if stop== 800:
                    pwm.stop()
                    time.sleep(1)
                    pwm.right()
                    time.sleep(1.6)
                if stop == 1000:
                    print("Reached a")
                    pwm.stop()
                    break
def cd():
    stop=0
    l=0
    while (True):
        distance = umeasure.measure()
        print("distance ", distance)
        if distance <20:
            pwm.stop()
        else:
                        
            if l==0:
                pwm.left()
                time.sleep(1.6)
                l=1
            else:
                pwm.forward() 
                stop= stop+1
                if stop== 400:
                    pwm.stop()
                    time.sleep(1)
                    pwm.left()
                    time.sleep(1.6)
                if stop== 600:
                    pwm.stop()
                    time.sleep(1)
                    pwm.right()
                    time.sleep(1.6)
                if stop == 1000:
                    print("Reached d")
                    pwm.stop()
                    break
def dc():
    stop=0
    l=0
    while (True):
        distance = umeasure.measure()
        print("distance ", distance)
        if distance <20:
            pwm.stop()
        else:
            pwm.forward() 
            stop= stop+1
            if stop== 400:
                pwm.stop()
                time.sleep(1)
                pwm.left()
                time.sleep(1.6)
            if stop== 600:
                pwm.stop()
                time.sleep(1)
                pwm.right()
                time.sleep(1.6)
            if stop == 1000:
                print("Reached c")
                pwm.stop()
                break
                
start= input("starting point A, B, C or D: ");
end= input("destination A, B, C or D: ");
if start=='a':
    if end=='b':
        ab()
        
        
if start=='a':
    if end=='c':
        ab() 
        time.sleep(1)
        bc()
        
        
if start=='a':
    if end=='d':
        ab()
        time.sleep(1)
        bc()
        time.sleep(1)
        cd()
        
if start=='b':
    if end=='a':
        ba()
        
        
if start =='b':
    if end=='c':
        bc()
        
        
if start =='b':
    if end =='d':
        bc()
        time.sleep(1)
        cd()
         
      
            
if start == 'c':
    if end =='d':
        cd()
        
if start == 'c':
    if end =='b':
        cb()
        
if start == 'c':
    if end =='a':
        cb()
        time.sleep(1)
        ba()
        
if start == 'd':
    if end =='c':
        dc()
        
if start == 'd':
    if end =='b':
        dc()
        time.sleep(1)
        cb()
        
if start == 'd':
    if end =='a':
        dc()
        time.sleep(1)
        cb()
        time.sleep(1)
        ba()
        
    
    
