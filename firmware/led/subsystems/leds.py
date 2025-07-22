from library.neopixel import NeoPixel

from constants import Constants

class LEDs_Panel(NeoPixel):
    def __init__(self, pin):
        super.__init__(pin, Constants.Pins.PANEL_LENGTH)
    def load(self, data):
        for i, led in enumerate(data):
            self[i] = led

class LEDs_Status:
    PASS = (  0, 255,   0)
    LOAD = (  0,   0, 255)
    FAIL = (255,   0,   0)
    NONE = (  0,   0,   0)

class LEDs_Board(NeoPixel):
    def __init__(self, pin):
        super.__init__(pin, Constants.Pins.BOARD_LENGTH)
        self.fill((0,0,0))


'''Initialize all Neopixel strips (on the LED subsystem)'''
PANEL = [LEDs_Panel(Constants.Pins.LED_PANELS[i]) for i in range(len(Constants.PIN_LED_PANELS))]
BOARD = LEDs_Board(Constants.Pins.LED_BOARD)