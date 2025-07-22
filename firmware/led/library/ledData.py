import math

class Data:
    def __init__(self, data = None):
        if data != None:
            self.loadData(data)
    def getFrame(self, timestamp, angle):
        # Returns the LED values for an angle at a timestamp.
        theta = timestamp * 5 + angle/180*math.pi
        return[[
                ((-math.sin(theta) + 1) * 255/2),
                (( math.sin(theta) + 1) * 255/2),
                (( math.cos(theta) + 1) * 255/2)
            ]
            for x in range(10)]
    def loadData(self):
        # TODO future features!
        pass





# import matplotlib.pyplot as plt
# import numpy as np
# import time

# test = Data()

# values = [test.getFrame(time.time(), x*45) for x in range(5)]
# fig, ax = plt.subplots(figsize=(10, 6))
# ax.set_aspect('equal')
# ax.axis('off')

# points = []
# for line in range(5):
#     temp = []
#     for led in range(10):
#         angle = line * np.pi / 4
#         radius = (led + 1)
#         x = radius * np.cos(angle)
#         y = radius * np.sin(angle)
#         color = [x/255 for x in values[line][led]]
#         point, = ax.plot(x, y, 'o', markersize=12, color=color)
#         temp.append(point)
#     points.append(temp)

# plt.show(block=False)



# while True:
#     values = [test.getFrame(time.time(), x*45) for x in range(5)]
#     for line in range(5):
#         for led in range(10):
#             color = [x/255 for x in values[line][led]]
#             points[line][led].set_color(color)

#     plt.draw()
#     plt.pause(0.05)