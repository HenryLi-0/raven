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
    def __init__(self, maxVelocity, maxAcceleration):
        self.maxVelocity = maxVelocity
        self.maxAcceleration = maxAcceleration


class PIDController(Controller):
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