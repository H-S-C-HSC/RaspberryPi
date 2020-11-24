import serial
import time
import threading

message = 'led'

ser = serial.Serial('/dev/ttyACM1', 9600)

# ser.write(message.encode())
# while True:

# while True:
#     if(ser.readable()):
#         res = ser.readline()
#         print(res)
        
def Serial():
    threading.Timer(1.0, Serial).start()
    if(ser.readable()):
        res = ser.readline()
        print(res)
Serial()
    