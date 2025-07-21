from library.neopixel import NeoPixel

from constants import Constants

class LEDs_Status:
    PASS = (  0, 255,   0)
    LOAD = (  0,   0, 255)
    FAIL = (255,   0,   0)
    NONE = (  0,   0,   0)

class LEDs_Board(NeoPixel):
    def __init__(self, pin):
        super.__init__(pin, Constants.Pins.LEDS_LEN)
        self.fill((0,0,0))


'''Initialize all Neopixel strips (on the LED subsystem)'''
BOARD = LEDs_Board(Constants.Pins.LEDS)