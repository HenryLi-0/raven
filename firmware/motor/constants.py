import board
'''
Pins:

board.D0  - 
board.D1  - 
board.D2  - 
board.D3  - 
board.D4  - 
board.D5  - 
board.D6  - 

board.D7  - 
board.D8  - 
board.D10 - 
'''

class Constants:
    # Whether or not to do the startup systems check. Recommended to keep True.
    STARTUP_SYS_CHECK = True

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