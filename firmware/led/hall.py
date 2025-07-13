import digitalio

from constants import *

class Hall:
    def __init__(self, pin):
        self.sensor = digitalio.DigitalInOut(pin)
        self.sensor.direction = digitalio.Direction.INPUT
    def getValue(self):
        return self.sensor.value


HALL = Hall(Constants.PIN_HALL)