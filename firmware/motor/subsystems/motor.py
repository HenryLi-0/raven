import digitalio

from constants import Constants

class Motor:
    def __init__(self, mosfetPin):
        self.mosfet = digitalio.DigitalInOut(mosfetPin)
        self.mosfet.direction = digitalio.Direction.OUTPUT
        self.mosfet.value = False
    def setPower(self, value):
        # Turns the MOSFET on/off. Unfortunately no specific voltages (unless you consider PWM?).
        self.mosfet.value = value

MOTOR = Motor(Constants.Pins.MOSFET)