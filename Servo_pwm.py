import RPi.GPIO as g
import time
import threading

#include <stdio.h>
#include <wiringPi.h>
#include <softPwm.h>

#define PIN 12 

servoPin = 21

g.setmode(g.BCM)
g.setup(servoPin, g.OUT)

servoDelay = 0.0015

def Servo():
    g.output(servoPin, 1)
    time.sleep(servoDelay)
    g.output(servoPin, 0)
    time.sleep(0.02 - servoDelay)
    threading.Thread(target = Servo, args = ()).start()

threading.Thread(target = Servo, args = ()).start()
