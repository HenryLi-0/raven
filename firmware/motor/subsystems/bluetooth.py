'''
It would be way faster to have the actual microcontroller and quickly test
things out (and that's really the only good way you can do this quickly),
so here's just a basic structure of a future implementation. (This will be
updated when said future implementation is complete!)
'''

class Bluetooth:
    def __init__(self):
        self.lastRecieve = -1
    def ping(self):
        pass
    def check(self, timestamp):
        pass
        # self.lastRecieve = timestamp
        return False
    def getLastRecieve(self):
        return self.lastRecieve

BLUETOOTH = Bluetooth()
