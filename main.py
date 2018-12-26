from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from picamera.array import PiRGBArray
import RPi.GPIO as GPIO
from picamera import PiCamera
import time
from time import sleep
import cv2
import numpy as np
import math
import dcmotor as pwm
import obstacleAvoid as usensor
import subprocess

camera = PiCamera()

def btn_clicked():
    print ("Button Pressed")
    QMessageBox.information(MainWindow, 'AUTOMATIC', 'ROBOT IS SELF DRIVING MODE')
    ob=0
    theta=0
    minLineLength = 5
    maxLineGap = 10
    
    camera.resolution = (320, 240)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(320, 240))
    stopCascade = cv2.CascadeClassifier('/home/pi/harrcascade_stopsign.xml')
    time.sleep(0.1)
    def obright():
        pwm.reverse()
        time.sleep(1)
        pwm.right()
        time.sleep(1)
        pwm.forward()
        time.sleep(0.8)
        pwm.left()
        time.sleep(1)
    def obleft():
        pwm.reverse()
        time.sleep(1)
        pwm.left()
        time.sleep(1)
        pwm.forward()
        time.sleep(0.8)
        pwm.right()
        time.sleep(1)
        
    try:
     for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
       
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #traffic
        hsv= cv2.cvtColor(image, cv2.COLOR_BGR2HSV)   
        #  red color

        red_lower = np.array([169,100,100],np.uint8)
        red_upper = np.array([189,255,255],np.uint8)
        # green color

        green_lower = np.array([65,60,60],np.uint8)
        green_upper = np.array([80,255,255],np.uint8)
        red = cv2.inRange(hsv, red_lower, red_upper)
        green = cv2.inRange(hsv, green_lower, green_upper)
     # Morphological Transform, Dilation

        kernal = np.ones((5, 5), "uint8")

        red = cv2.dilate(red, kernal)
        res_red = cv2.bitwise_and(image, image, mask = red)
        green = cv2.dilate(green, kernal)
        res_green = cv2.bitwise_and(image, image, mask = green)
      
        

        #lane and stop   
        
        stop = stopCascade.detectMultiScale(gray,1.3,5)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 85, 85)
        lines = cv2.HoughLinesP(edged,1,np.pi/180,10,minLineLength,maxLineGap)
        if(lines !=None):
            for x in range(0, len(lines)):
                for x1,y1,x2,y2 in lines[x]:
                    cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
                    theta=theta+math.atan2((y2-y1),(x2-x1))
        threshold=6
    ##   move=2/10
        if (len(stop)!=0):
            for (x,y,w,h) in stop:
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
                cv2.putText(image, str("stop"), (x,y-40), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = image[y:y+h, x:x+w]
            pwm.stop()
            print("stop sign detected! stopping... ")
        else:    
            distance = usensor.measure()
            if(distance <30):
                pwm.stop()
                print("OBSTACLE AHEAD!!!!")
                print("obstacle distance: ", distance,"cm")
                pwm.stop()
                if usensor.measure()<25:
                    pwm.stop()
                else:    
                    if ob==0:    
                        obright()
                        ob=ob+1
                    else:
                        obleft()
                        ob=0
##                    if(usensor.measure() <30):
##                        pwm.stop()
##                        break
                
            else:
                traffic=0
                (_, contours, hierarchy)=cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                for pic, contour in enumerate(contours):
                    area = cv2.contourArea(contour)
                    if(area > 300):
                        #green
                        x, y, w, h = cv2.boundingRect(contour)
                        img = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(img, "Green Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
                        print("green traffic light GO")
                        
                        
                (_, contours, hierarchy)=cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                for pic, contour in enumerate(contours):
                    area = cv2.contourArea(contour)
                    if(area > 300):
                        x, y, w, h = cv2.boundingRect(contour)
                        img = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        cv2.putText(img, "Red Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))
                        print("red traffic light STOP")
                        traffic= 2 
                        
                if(traffic > 1):
                    print("stopping")
                    pwm.stop()
                else:
                    print("moving")
                    if(theta>threshold):
                        pwm.left()
                        print("left")
                        
                        
                    if(theta<-threshold):
                        pwm.right()
                        print("right")
                        
                        
        ##       time.sleep(1)
                    if(abs(theta)<threshold):
                        pwm.forward()
                        print("forward")
                        
                    
        ##       time.sleep(2)
                    theta=0
        cv2.imshow("Frame",image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("q"):
            break
    finally:
     GPIO.cleanup()


def btn1_clicked():
    print ("Button Pressed")
    QMessageBox.information(MainWindow, 'REMOTE', 'ROBOT IS IN REMOTE CONTROL MODE')
    from bluedot import BlueDot
    from signal import pause
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    GPIO.output (22, 0)
    GPIO.output (23, 0)
    GPIO.output (17, 0)
    GPIO.output (24, 0) 
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
    
def btn2_clicked():
    QMessageBox.information(MainWindow, 'STOP', 'Closing')
    sys.exit(app.exec_())
def btn3_clicked():
    QMessageBox.information(MainWindow, 'wait', 'importing')
        
    import sys, termios, tty, os, getch



    button_delay = 0.2


    while True:
        char = getch.getch() 

        if (char == "a"):
            print ('Left pressed')
            pwm.a(1) 
            time.sleep(button_delay)

        if (char == "d"):
            print ('Right pressed')
            pwm.d(1)
            time.sleep(button_delay)          

        elif (char == "w"):
            print ('Up pressed') 
            pwm.w(1)      
            time.sleep(button_delay)          
        
        elif (char == "s"):
            print ('Down pressed')    
            pwm.stop()
            time.sleep(button_delay)  
        if (char=="q"):
            break
        elif (char == "r"):
            print ('Down pressed')    
            pwm.r(1)
            time.sleep(button_delay)   
def btn4_clicked():
    import matplotlib.pyplot as plt
    


    for num in range(180):
        if num==180:
            break
        else:
            
            pwm.left()
            dist=usensor.measure()
            print("distance =", dist )
            plt.title('distance over angle')
            
            plt.ylabel('distance " cm"')
            plt.xlabel('angle')
            plt.bar(num*2,dist)
    GPIO.cleanup()
    plt.show()
def btn5_clicked():
    QMessageBox.information(MainWindow, 'PARKING', 'parking')
    import time
    import RPi.GPIO as GPIO
    from time import sleep
    import dcmotor as pwm
    
    def measure():
        GPIO.setmode(GPIO.BCM)
        GPIO_TRIGGER = 20
        GPIO_ECHO    = 21
        
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
    distanc=0
    while (True):
        dis=measure()
        print("distance", dis)
        if distanc==0:
            pwm.forward()
            if dis<20:
                print("forward")
                
            if dis>20 :
                print("forward")
                if measure()>20:
                    if measure()>20:
                        if measure()>20:
                            if measure()>20:
                                if measure()>20:
                                    if measure()>20:
                                        distanc=1
                                        print ("Parking....") 
                                        pwm.stop()  
                                        pwm.reverse()
                                        time.sleep(3)
                                        pwm.stop()
                                        if measure()<10:
                                            pwm.forward()
                                            time.sleep(1)
                                            pwm.stop()
                                            time.sleep(1)
                                            pwm.left()
                                            time.sleep(1)
                                            pwm.stop()
                                            time.sleep(1)
                                            pwm.forward()
                                            time.sleep(1)
                                            pwm.stop()
                                            time.sleep(1)
                                            pwm.right()
                                            time.sleep(1)
                                            pwm.stop()
                                            GPIO.cleanup()
                                            break
                                        if measure()>10:
                                            pwm.forward()
                                            time.sleep(1)
                                            pwm.stop()
                                            time.sleep(1)
                                            pwm.left()
                                            time.sleep(1)
                                            pwm.stop()
                                            time.sleep(1)
                                            pwm.forward()
                                            time.sleep(1)
                                            pwm.stop()
                                            time.sleep(1)
                                            pwm.right()
                                            time.sleep(1)
                                            pwm.stop()
                                            GPIO.cleanup()
                                            break
##                                        pwm.stop()
##                                        time.sleep(1)
##                                        pwm.right()
##                                        time.sleep(1)
                                        
                                       
        if distanc==1:
            if dis<20:
                print("stop go back n park")
                pwm.stop()
                
    GPIO.cleanup()
def btn6_clicked():
    QMessageBox.information(MainWindow, 'DEFINED PATH', 'choose path a, b, c or d')
    import subprocess
    
    subprocess.Popen(['python3', 'static.py'])
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(450, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn = QtWidgets.QPushButton(self.centralwidget)
        self.btn.setGeometry(QtCore.QRect(345, 10, 100, 31))
        self.btn.setObjectName("btn")
        self.btn1 = QtWidgets.QPushButton(self.centralwidget)
        self.btn1.setGeometry(QtCore.QRect(345, 50, 100, 31))
        self.btn1.setObjectName("btn1")
        self.btn2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn2.setGeometry(QtCore.QRect(345, 250, 100, 31))
        self.btn2.setObjectName("btn2")
        self.btn3 = QtWidgets.QPushButton(self.centralwidget)
        self.btn3.setGeometry(QtCore.QRect(345, 90, 100, 31))
        self.btn3.setObjectName("btn3")
        self.btn4 = QtWidgets.QPushButton(self.centralwidget)
        self.btn4.setGeometry(QtCore.QRect(345, 130, 100, 31))
        self.btn4.setObjectName("btn4")
        self.btn5 = QtWidgets.QPushButton(self.centralwidget)
        self.btn5.setGeometry(QtCore.QRect(345, 170, 100, 31))
        self.btn5.setObjectName("btn5")
        self.btn6 = QtWidgets.QPushButton(self.centralwidget)
        self.btn6.setGeometry(QtCore.QRect(345, 210, 100, 31))
        self.btn6.setObjectName("btn6")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SELF DRIVING ROBOT"))
        MainWindow.setStyleSheet("background-image: url(/home/pi/Downloads/back.jpg)")
        self.btn.setStyleSheet("color: white; background: black")
        self.btn1.setStyleSheet("color: white; background: black")
        self.btn2.setStyleSheet("color: black; background: white")
        self.btn3.setStyleSheet("color: white; background: black")
        self.btn4.setStyleSheet("color: white; background: black")
        self.btn5.setStyleSheet("color: white; background: black")
        self.btn6.setStyleSheet("color: white; background: black")
        
        self.btn.setText(_translate("MainWindow", "AUTOMATIC"))
        self.btn1.setText(_translate("MainWindow", "BLUEDOT"))
        self.btn2.setText(_translate("MainWindow", "EXIT"))
        self.btn3.setText(_translate("MainWindow", "REMOTE"))
        self.btn4.setText(_translate("MainWindow", "MAPPING"))
        self.btn5.setText(_translate("MainWindow", "PARKING"))
        self.btn6.setText(_translate("MainWindow", "DEFINED PATH"))
        
        '''User Code'''
        self.btn.clicked.connect( btn_clicked )
        self.btn1.clicked.connect( btn1_clicked )
        self.btn2.clicked.connect( btn2_clicked)
        self.btn3.clicked.connect( btn3_clicked)
        self.btn4.clicked.connect( btn4_clicked)
        self.btn5.clicked.connect( btn5_clicked)
        self.btn6.clicked.connect( btn6_clicked)
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
