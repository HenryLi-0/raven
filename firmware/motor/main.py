import board
import digitalio
import time

from constants import *
from library.control import *
from subsystems.bluetooth import *
from subsystems.clock import *
from subsystems.hall import *
from subsystems.leds import *
from subsystems.motor import *

print(dir(board))

'''###############################################################################################'''
'''                                     STARTUP SYSTEMS CHECK                                     '''
'''###############################################################################################'''

success = True
if Constants.STARTUP_SYS_CHECK:
    print("Starting Systems Check")
    BOARD.fill(LEDs_Status.LOAD)
    time.sleep(1)
    BOARD.fill(LEDs_Status.NONE)
    time.sleep(1)
    
    print(" | MOTOR")
    for i in range(3):
        BOARD[i] = LEDs_Status.LOAD
        MOTOR.setSpeed(i*20)
        time.sleep(3)
        temp = (abs(MOTOR.getSpeed()-i*20) < 1)
        BOARD[i] = LEDs_Status.PASS if temp else LEDs_Status.FAIL
        success = success and temp

    print(" |  | " + ("SUCCESS" if success else "FAIL"))
else:
    success = True
time.sleep(1)

if not(success):
    print("Safety Exit (Unsuccessful Systems Check)")
    BOARD.fill(LEDs_Status.FAIL)
    State.status = SubsystemStatus.DANGER
    exit()
else:
    BOARD.fill(LEDs_Status.PASS)
    State.status = SubsystemStatus.OPERATIONAL
time.sleep(1)
BOARD.fill(LEDs_Status.NONE)

'''###############################################################################################'''
'''                                             START                                             '''
'''###############################################################################################'''

# init logic
poseUpdater = Updater()
hallCounter = Counter()

pid = PIDController(Constants.Motor.kP, Constants.Motor.kI, Constants.Motor.kD)
motorPWM = PWM()

while State.status == SubsystemStatus.OPERATIONAL:
    State.timestamp = CLOCK.getTime()

    BLUETOOTH.ping()
    BLUETOOTH.check(State.timestamp)
    if abs(State.timestamp - BLUETOOTH.getLastRecieve()) > Constants.TIMEOUT_UNITL_SHUTDOWN:
        State.status = SubsystemStatus.DANGER
    
    if HALL.getValue():
        hallCounter.ping()
    
    if poseUpdater.needUpdate():
        State.currentRPM = hallCounter.getPings()


    # PID controlling motor PWM
    fb = pid.calculate(State.currentRPM, State.targetRPM, State.timestamp)
    print(fb)
    motorPWM.set(fb)
    MOTOR.setPower(motorPWM.get(State.timestamp))

    