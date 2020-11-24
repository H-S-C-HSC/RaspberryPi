from pad4pi import rpi_gpio
import time

# Setup Keypad
KEYPAD = [
        ["1","4","7","*"],
        ["2","5","8","0"],
        ["3","6","9","#"],
        ["A","B","C","D"]
]

# same as calling: factory.create_4_by_4_keypad, still we put here fyi:
ROW_PINS = [19,13,6,5] # BCM numbering
COL_PINS = [1,7,8,25] # BCM numbering

factory = rpi_gpio.KeypadFactory()

# Try factory.create_4_by_3_keypadz
# and factory.create_4_by_4_keypad for reasonable defaults
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

#keypad.cleanup()

def printKey(key):
  print(key)

# printKey will be called each time a keypad button is pressed
keypad.registerKeyPressHandler(printKey)

try:
  while(True):
    time.sleep(0.2)
except:
  keypad.cleanup()