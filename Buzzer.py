import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
BUZZER = 23
GPIO.setup(BUZZER, GPIO.OUT)

def buzz(noteFreq, duration):
    halveWaveTime = 1 / (noteFreq * 2)
    waves = int(duration * noteFreq)
    for i in range(waves):
       GPIO.output(BUZZER, True)
       time.sleep(halveWaveTime)
       GPIO.output(BUZZER, False)
       time.sleep(halveWaveTime)

def doorOpen():
    buzz(783, 0.08)
    time.sleep(0.01)
#     time.sleep(0.21)
    buzz(880, 0.08)
    time.sleep(0.01)
#     time.sleep(0.21)
    buzz(987, 0.08)
    time.sleep(0.1)
    
def doorFail():
    buzz(1576, 0.2)
    time.sleep(0.1)
    buzz(1576, 0.2)
    time.sleep(0.1)
    buzz(1576, 0.2)
    time.sleep(0.1)
    
def keypadClick():
    buzz(1480, 0.08)

keypadClick()