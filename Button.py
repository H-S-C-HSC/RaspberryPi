import RPi.GPIO as g
import time

PUSH_PIN1 = 14
PUSH_PIN2 = 15

toggle1 = 0
toggle2 = 0

g.setmode(g.BCM)

g.setup(PUSH_PIN1, g.IN, pull_up_down = g.PUD_DOWN)
g.setup(PUSH_PIN2, g.IN, pull_up_down = g.PUD_DOWN)

while True:
    if g.input(PUSH_PIN1) == g.LOW:
        if toggle1 == 0:
            print("push1 DOWN")
            toggle1 = 1
    else:
        if toggle1 == 1:
            toggle1 = 0
            print("push1 UP")
    if g.input(PUSH_PIN2) == g.LOW:
        if toggle2 == 0:
            print("push2 DOWN")
            toggle2 = 1
    else:
        if toggle2 == 1:
            toggle2 = 0
            print("push2 UP")
    
    time.sleep(0.1)
