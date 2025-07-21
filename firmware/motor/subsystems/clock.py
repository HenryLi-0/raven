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
    
    def ping(self):
        # Updates the bucket counter and buckets.
        temp = self.snapshot // Constants.Clock.BUCKET_LENGTH
        if self.bucket != temp:
            self.bucket = temp
            self.rate = self.count * (1/Constants.Clock.BUCKET_LENGTH)
            self.count = 0
        self.count += 1
    
    def getPings(self):
        # Returns the latest bucket count (or, more accurately, the estimated number of pings per second).
        return self.rate


'''clock init'''
CLOCK = Clock()