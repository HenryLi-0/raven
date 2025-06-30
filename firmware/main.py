import board
import digitalio
from neopixel import NeoPixel
import time

print(dir(board))

'''
Pins:

board.D0  - LED 4
board.D1  - LED 3
board.D2  - LED BACKUP 2
board.D3  - LED 2
board.D4  - LED BACKUP 1
board.D5  - LED 1
board.D6  - LED 0

board.D7  - HALL EFFECT SENSOR
board.D8  - HALL EFFECT SENSOR BACKUP
board.D9  - MOSFET
board.D10 - MOSFET BACKUP
'''

class Constants:
    PIN_LEDS = [
        board.D6,
        board.D5,
        board.D3,
        board.D1,
        board.D0,
    ]
    PANEL_OFFSET = lambda i: i*45
    PIN_MOSFET = board.D9
    PIN_HALL = board.D7

    STARTUP_SYS_CHECK = True

# init

LEDS = [NeoPixel(Constants.PIN_LEDS[i], 10) for i in range(len(Constants.PIN_LEDS))]
for panel in LEDS: panel.fill((0,0,0))

MOSFET = digitalio.DigitalInOut(Constants.PIN_MOSFET)
MOSFET.direction = digitalio.Direction.OUTPUT
MOSFET.value = False

HALL = digitalio.DigitalInOut(Constants.PIN_HALL)
HALL.direction = digitalio.Direction.INPUT

# STARTUP SYSTEMS CHECK

success = False
if Constants.STARTUP_SYS_CHECK:
    print("Starting Systems Check")
    print(" | LEDs On")
    for panel in LEDS: panel.fill((255,255,255))
    time.sleep(1)
    print(" | LEDs Off")
    for panel in LEDS: panel.fill((0,0,0))
    time.sleep(1)
    print(" | MOSFET and Hall")
    start = time.time()
    success = False
    MOSFET.value = True
    time.sleep(0.2)
    while abs(time.time() - start) < 1:
        if HALL.value:
            success = True
            break
    MOSFET.value = False
    print(" |  | " + ("SUCCESS" if success else "FAIL"))
else: success = True

if not(success):
    print("Safety Exit (Unsuccessful Systems Check)")
    exit()

# start

# CURRENT CODE HERE IS AN EXPERIMENT!

# blep