import board
'''
Pins:

board.D0  - LED
board.D1  - NA
board.D2  - NA
board.D3  - NA
board.D4  - NA
board.D5  - NA
board.D6  - NA

board.D7  - MOSFET
board.D8  - MOSFET BACKUP
board.D9  - HALL EFFECT SENSOR BACKUP
board.D10 - HALL EFFECT SENSOR
'''

class Constants:
    # Whether or not to do the startup systems check. Recommended to keep True.
    STARTUP_SYS_CHECK = True
    # Number of seconds without microcontroller communication before both systems automatically shutdown.
    TIMEOUT_UNITL_SHUTDOWN = 3.0

    class Pins:
        # Board LED Data Pin
        LEDS = board.D0
        # Number of LEDs on the board
        LEDS_LENGTH = 6
        # MOSFET Data Pin
        MOSFET = board.D0
        # Hall Effect Sensor Pin
        HALL = board.D7

    class Motor:
        # PID values for the motor PID.
        # TODO tune
        kP = 0
        kI = 0
        kD = 0
    
    class PWM:
        # This defines the frequency of the PWM. Must be less than the code frequency.
        FREQUENCY = 1/250

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
    currentRPM = 0
    # The target RPM
    targetRPM = 0