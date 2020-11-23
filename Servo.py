import RPi.GPIO as g
import time

pin = 21

g.setmode(g.BCM)
g.setup(pin, g.OUT)

motorPWM = g.PWM(pin, 50)
motorPWM.start(0)

motorPWM.ChangeDutyCycle(3) # 0
time.sleep(3);

# motorPWM.ChangeDutyCycle(12) # 180
# time.sleep(3);

motorPWM.ChangeDutyCycle(7.5) ## 90
time.sleep(3);

g.cleanup()