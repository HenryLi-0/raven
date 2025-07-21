import board
'''
Pins:

board.D0  - LED 0
board.D1  - LED 1
board.D2  - LED BACKUP 2
board.D3  - LED 2
board.D4  - LED BACKUP 1
board.D5  - LED 3
board.D6  - LED 4

board.D7  - HALL EFFECT SENSOR
board.D8  - HALL EFFECT SENSOR BACKUP
board.D10 - SELF LEDS
'''

class Constants:
    STARTUP_SYS_CHECK = True

    class Pins:
        LED_PANELS = [
            board.D0,
            board.D1,
            board.D3,
            board.D5,
            board.D6,
        ]
        LED_BOARD = board.D10
        PANEL_OFFSET = lambda i: i*45
        PANEL_LENGTH = 10
        BOARD_LENGTH = 3

        HALL = board.D7

    class Clock:
        # This defines the time length of each bucket (in seconds).
        BUCKET_LENGTH = 0.01
        # This defines the length of time between each update.
        UPDATER_LENGTH = BUCKET_LENGTH

class SubsystemStatus:
    # This defines the subsystem status.
    OPERATIONAL = 1
    IDLE = 0
    DANGER = -1

class State:
    # This defines the subsystem state.
    status = None
    timestamp = 0
    currentRPM = 1e-9
    rotationTime = 1/currentRPM
    position = 0