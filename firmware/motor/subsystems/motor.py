import digitalio

from constants import *

class Motor:
    def __init__(self, mosfetPin):
        self.mosfet = digitalio.DigitalInOut(mosfetPin)
        self.mosfet.direction = digitalio.Direction.OUTPUT
        self.mosfet.value = False

        self.target = 0
    def setValue(self, value):
        self.mosfet.value = value
    def setSpeed(self, speed):
        self.target = speed
    def getSpeed(self):
        return 0

MOTOR = Motor(Constants.PIN_MOSFET)