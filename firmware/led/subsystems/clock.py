import time, math
from constants import Constants

class Clock:
    def __init__(self):
        self.setTime()
        self.rate = 0
        self.count = 0
        self.bucket = self.snapshot // Constants.Clock.BUCKET_LENGTH

    def setTime(self):
        # Sets the snapshot time.
        self.snapshot = time.monotonic_ns()/(10**9)
    def getTime(self):
        # Gets the snapshot time.
        return self.snapshot
    
'''clock init'''
CLOCK = Clock()


class Counter:
    # Counts and estimated the number of updates it receives per second.
    def __init__(self):
        pass

    def ping(self):
        # Updates the bucket counter and buckets.
        temp = CLOCK.snapshot // Constants.Clock.BUCKET_LENGTH
        if self.bucket != temp:
            self.bucket = temp
            self.rate = self.count * (1/Constants.Clock.BUCKET_LENGTH)
            self.count = 0
        self.count += 1
    
    def getPings(self):
        # Returns the latest bucket count (or, more accurately, the estimated number of pings per second).
        return self.rate

class Updater:
    def __init__(self):
        self.bucket = -1
    def needUpdate(self):
        temp = CLOCK.snapshot // Constants.Clock.UPDATER_LENGTH
        if self.bucket != temp:
            self.bucket = temp
            return True
        return False