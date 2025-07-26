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
    # Whether or not to do the startup systems check. Recommended to keep True.
    STARTUP_SYS_CHECK = True
    # Number of seconds without microcontroller communication before both systems automatically shutdown.
    TIMEOUT_UNITL_SHUTDOWN = 3.0

    class Pins:
        # LED Panel Data Pins
        LED_PANELS = [
            board.D0,
            board.D1,
            board.D3,
            board.D5,
            board.D6,
        ]
        # The number of panels
        NUMBER_OF_PANELS = len(LED_PANELS)
        # Offset between each panel
        PANEL_OFFSET = 180/(NUMBER_OF_PANELS-1)
        # Number of LEDs on each panel
        PANEL_LENGTH = 10
        
        # Board LED Data Pin
        LED_BOARD = board.D10
        # Number of LEDs on the board LED strip
        BOARD_LENGTH = 3

        # Hall Effect Sensor Pin
        HALL = board.D7

    class Clock:
        # This defines the time length of each bucket (in seconds).
        BUCKET_LENGTH = 0.01
        # This defines the length of time between each update.
        UPDATER_LENGTH = BUCKET_LENGTH

class SubsystemStatus:
    # This defines the subsystem status.
    OPERATIONAL = 1         # Safe :D
    IDLE = 0                # Nothing
    DANGER = -1             # "Uh oh"

class State:
    # This defines the subsystem state.
    
    # The status
    status = None
    # The current time
    timestamp = 0
    # The current RPM
    currentRPM = 1e-9
    # The length of time for one rotation
    rotationTime = 1/currentRPM
    # Defines the rotation position of the LED subsystem, as a decimal (ex. 0.5 means 180 degrees)
    position = 0