import math

from constants import Constants

def clamp(minV, val, maxV):
    # Clamps a value between minV and maxV.
    return max(minV, min(val, maxV))

class Controller:
    def __init__(self):
        self.goal = 0
        pass
    def calculate(self, measurement, goal):
        self.setGoal(goal)

    def setGoal(self, goal):
        self.goal = goal

class Profile:
    pass

class TrapezoidProfile(Profile):
    # A Trapezoid Profile.
    def __init__(self, maxVelocity, maxAcceleration):
        self.maxVelocity = maxVelocity
        self.maxAcceleration = maxAcceleration


class PIDController(Controller):
    # A PID Controller.
    def __init__(self, p, i, d, measurement = 0, timestamp = 0):
        super().__init__()
        self.p = p
        self.i = i
        self.d = d
        self.lastMeasurement = measurement
        self.lastError = 0
        self.lastTime = timestamp
        self.totalError = 0

    def calculate(self, measurement, goal, timestamp):
        self.totalError += (goal-measurement)*(timestamp-self.lastTime)
        value = (self.p*(goal-measurement)
            + self.i*(self.totalError)
            + self.d*((goal-measurement)-self.lastError)/(timestamp-self.lastTime+1e-6)
        )
        self.lastMeasurement = measurement
        self.lastError = goal-measurement
        self.lastTime = timestamp
        return value

class PWM:
    # A PWM. Updating the quality affects all PWM.
    quality = Constants.PWM.FREQUENCY
    def setQuality(quality):
        PWM.quality = quality

    def __init__(self):
        self.dutyCycle = 0.0
    def set(self, dutyCycle):
        self.dutyCycle = clamp(0.0, dutyCycle, 1.0)
    def get(self, timestamp):
        return (timestamp % PWM.quality) <= (PWM.quality * self.dutyCycle)
        