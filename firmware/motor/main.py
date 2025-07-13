import board
import digitalio
import time

from constants import *
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
    exit()
else:
    BOARD.fill(LEDs_Status.PASS)
time.sleep(1)
BOARD.fill(LEDs_Status.NONE)

'''###############################################################################################'''
'''                                             START                                             '''
'''###############################################################################################'''

# blep