import urx
from math import radians
import robot_class
import numpy as np
import matplotlib.pyplot as plt

IP = "192.168.1.101"
defaultPose = (0, radians(-90), 0, radians(-135), radians(90), 0)



rob = robot_class.RobotClass(IP, defaultPose)

rob.getHSV()

#plt.ion()
#plt.show()

for i in range(5):
    img = rob.getImage()
    plt.imshow(img)
    plt.show()
    #plt.draw()
    #plt.pause(0.001)
    print("Showing")

#rob.resetPose()

rob.close()
exit()