import requests
import os
import RPi.GPIO as GPIO
import time
import picamera
import datetime
from pad4pi import rpi_gpio
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

servoPin = 21

GPIO.setup(servoPin, GPIO.OUT)

motorPWM = GPIO.PWM(servoPin, 50)
motorPWM.start(0)
motorPWM.ChangeDutyCycle(7.5) ## 90

KEYPAD = [
        ["1","4","7","*"],
        ["2","5","8","0"],
        ["3","6","9","#"],
        ["A","B","C","D"]
]

ROW_PINS = [5,6,13,19] # BCM numbering
COL_PINS = [1,7,8,25] # BCM numbering

factory = rpi_gpio.KeypadFactory()

keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)


BUZZER = 23
GPIO.setup(BUZZER, GPIO.OUT)

PUSH_PIN1 = 15
PUSH_PIN2 = 14

toggle1 = 0
toggle2 = 0

isSong = False
isCapture = False

GPIO.setup(PUSH_PIN1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(PUSH_PIN2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def CameraCapture():
    
    cam = picamera.PiCamera()
    global isCapture
    isCapture = True
    saveLocation = ("./{0}.png".format(str(datetime.datetime.now()).replace('-','_').replace(':','_').replace(' ','_').split('.')[0]))
    
    print('save location : ')
    print(saveLocation)

    cam.capture(saveLocation)

    cam.close()
    
    url = 'http://172.30.1.39:5000/save/photo'

    with open(saveLocation, 'rb') as img:
        name_img = os.path.basename(saveLocation)
        files = {'photo' : (name_img, img, 'multipart/form-data',{'Expires' : '0'})}
        with requests.Session() as s:
            r = s.post(url, files = files)
            print("status_code = {0}".format(r.status_code))
    
    isCapture = False

def buzz(noteFreq, duration):
    halveWaveTime = 1 / (noteFreq * 2)
    waves = int(duration * noteFreq)
    for i in range(waves):
       GPIO.output(BUZZER, True)
       time.sleep(halveWaveTime)
       GPIO.output(BUZZER, False)
       time.sleep(halveWaveTime)
       
def play():
    global isSong
    isSong = True
    t=0
    notes=[262,294,330,262,262,294,330,262,330,349,392,330,349,392,392,440,392,349,330,262,392,440,392,349,330,262,262,196,262,262,196,262]
    duration=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,0.5,1,0.25,0.25,0.25,0.25,0.5,0.5,0.25,0.25,0.25,0.25,0.5,0.5,0.5,0.5,1,0.5,0.5,1]
    for n in notes:
        buzz(n, duration[t] / 3)
        time.sleep(duration[t] *0.1)
        t+=1
    isSong = False
    return
       
def Button():
    global toggle1
    global toggle2
    
    threading.Timer(0.1, Button).start()
    if GPIO.input(PUSH_PIN1) == GPIO.LOW:
        if toggle1 == 0:
            print("push1 DOWN")
            toggle1 = 1
            if isSong == False:
                threading.Thread(target = play, args = ()).start()
            if isCapture == False:
                threading.Thread(target = CameraCapture, args = ()).start()
    else:
        if toggle1 == 1:
            toggle1 = 0
            print("push1 UP")
    if GPIO.input(PUSH_PIN2) == GPIO.LOW:
        if toggle2 == 0:
            print("push2 DOWN")
            toggle2 = 1
            doorClose()
    else:
        if toggle2 == 1:
            toggle2 = 0
            print("push2 UP")
            
    return

Button()

def doorOpen():
    motorPWM.ChangeDutyCycle(3) # 0
    
    buzz(783, 0.08)
    time.sleep(0.01)
#     time.sleep(0.21)
    buzz(880, 0.08)
    time.sleep(0.01)
#     time.sleep(0.21)
    buzz(987, 0.08)
    time.sleep(0.1)
    
def doorClose():
    motorPWM.ChangeDutyCycle(7.5) ## 90
    
    buzz(987, 0.08)
    time.sleep(0.01)
#     time.sleep(0.21)
    buzz(880, 0.08)
    time.sleep(0.01)
#     time.sleep(0.21)
    buzz(400, 0.08)
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
    



doorFailCount = 0
doorClickCount = 0
passwd = ""
passwdResetCode = "ABCD"
isReset = False


def PasswdReset(newPasswd):
    global isReset
    f = open("./passwd.txt", 'w')
    f.write(newPasswd)
    f.close()
    isReset = False

def printKey(key):
    global doorClickCount
    global doorFailCount
    global passwd
    global isReset
    
    
    doorClickCount = doorClickCount + 1
    passwd = passwd + key
    
    keypadClick()
    
    print(key)
    
    if doorClickCount == 4:
        myPasswd = ""
        time.sleep(0.1)
        try:
            f = open('./passwd.txt', 'r')
            myPasswd = f.read()
            print("my passwd = {}".format(myPasswd))
            print("passwd = {}".format(passwd))
            
            f.close()
            
            if isReset == True:
                if passwd == passwdResetCode:
                    doorFail()
                    passwd = ""
                    doorClickCount = 0
                    return
                PasswdReset(passwd)
                doorFailCount = 0
            elif passwd == passwdResetCode:
                isReset = True
            elif passwd == myPasswd:
                doorOpen()
                doorFailCount = 0
            else:
                doorFailCount = doorFailCount + 1
                doorFail()
                if doorFailCount == 3:
                    if isCapture == False:
                        threading.Thread(target = CameraCapture, args = ()).start()
                    doorFailCount = 0
        except:
            PasswdReset(passwd)
            
        passwd = ""
        doorClickCount = 0
    
    

# printKey will be called each time a keypad button is pressed
keypad.registerKeyPressHandler(printKey)

