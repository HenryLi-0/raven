import board
'''
Pins:

board.D0  - LED 0
board.D1  - LED 1
board.D2  - LED BACKUP 2
board.D3  - LED 2
board.D4  - LED BACKUP 1
board.D5  - LED 3
board.D6  - LED 4

board.D7  - HALL EFFECT SENSOR
board.D8  - HALL EFFECT SENSOR BACKUP
board.D10 - SELF LEDS
'''

class Constants:
    PIN_LEDS = board.D0
    LED_LENGTH = 8

    PIN_MOSFET = board.D0

    PIN_HALL = board.D7
    
    STARTUP_SYS_CHECK = True