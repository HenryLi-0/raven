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
    STARTUP_SYS_CHECK = True

    class Pins:
        # All the pins
        LEDS = board.D0
        LEDS_LEN = 6

        MOSFET = board.D0
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

class SubsystemStatus:
    # This defines the subsystem status.
    OPERATIONAL = 1
    IDLE = 0
    DANGER = -1

class State:
    # This defines the subsystem state.
    timestamp = 0
    currentRPM = 0
    targetRPM = 0