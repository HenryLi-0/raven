import board
import time

from constants import *
from library.ledData import *
from subsystems.bluetooth import *
from subsystems.clock import *
from subsystems.leds import *
from subsystems.hall import *

print(dir(board))

for panel in PANEL: panel.fill((0,0,0))

'''###############################################################################################'''
'''                                     STARTUP SYSTEMS CHECK                                     '''
'''###############################################################################################'''

success = True
if Constants.STARTUP_SYS_CHECK:
    print("Starting Systems Check")
    BOARD.fill(LEDs_Status.LOAD)
    time.sleep(1)
    BOARD.fill(LEDs_Status.NONE)
    
    print(" | LEDs")
    BOARD[0] = LEDs_Status.LOAD
    for panel in PANEL: panel.fill((255,255,255))
    time.sleep(1)
    for panel in PANEL: panel.fill((0,0,0))
    time.sleep(1)
    BOARD[0] = LEDs_Status.PASS

    print(" | HALL")
    BOARD[1] = LEDs_Status.LOAD
    start = time.time()
    temp = False
    while abs(time.time()-start) < 5 or temp:
        temp = HALL.getValue() or temp
    BOARD[1] = LEDs_Status.PASS if temp else LEDs_Status.FAIL
    success = success and temp

    print(" | Signal")
    # TODO
    BOARD[2] = LEDs_Status.PASS

    print(" |  | " + ("SUCCESS" if success else "FAIL"))
else:
    success = True
    State.status = SubsystemStatus.OPERATIONAL
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
data = Data()

# main loop!
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
        if State.currentRPM == 0:
            State.currentRPM = 1e-9
            State.rotationTime = 1 / State.currentRPM
    
    State.position = (State.timestamp % State.rotationTime)/(State.rotationTime)

    for i in range(Constants.Pins.NUMBER_OF_PANELS):
       PANEL[i].load(data.getFrame(State.timestamp, Constants.Pins.PANEL_OFFSET(i) + State.position*360))

# blep