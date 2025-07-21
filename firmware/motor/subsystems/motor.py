import digitalio

from constants import *

class Motor:
    def __init__(self, mosfetPin):
        self.mosfet = digitalio.DigitalInOut(mosfetPin)
        self.mosfet.direction = digitalio.Direction.OUTPUT
        self.mosfet.value = False
    def setValue(self, value):
        self.mosfet.value = value

MOTOR = Motor(Constants.Pins.MOSFET)