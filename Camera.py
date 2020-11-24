import picamera
import datetime
import time

cam = picamera.PiCamera()

print(str(datetime.datetime.now()).replace('-','_').replace(':','_').replace(' ','_').split('.')[0])

cam.capture("./{0}.png".format(str(datetime.datetime.now()).replace('-','_').replace(':','_').replace(' ','_').split('.')[0]))

cam.close()

