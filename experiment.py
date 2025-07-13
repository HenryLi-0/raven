import time

from firmware.motor.library.control import *

class Constants:
    P = 0.2
    I = 0
    D = 0.03

current = 0
controller = PIDController(Constants.P,
                           Constants.I,
                           Constants.D,
                           current,
                           time.time()
                )
goal = 0
start = time.time()
while abs(time.time()-start) < 0.3:
    current += controller.calculate(current, goal, time.time())
    print("goal: {:03} | current: {}".format(goal, current))
    time.sleep(0.1)
goal = 10
start = time.time()
while abs(time.time()-start) < 3:
    current += controller.calculate(current, goal, time.time())
    print("goal: {:03} | current: {}".format(goal, current))
    time.sleep(0.1)