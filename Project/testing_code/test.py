import urx
import time
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
import numpy as np

ROBOT_LOADED = 0

try:
    rob = urx.Robot("192.168.1.101")
    ROBOT_LOADED = 1
except:
    pass
if ROBOT_LOADED:
    gripper = Robotiq_Two_Finger_Gripper(rob)

    lastPos = rob.getj()

    temp_array = []
    rev_array = []
    for count,x in enumerate(lastPos):
        if count == 0:
            temp_array.append(x + 90/180*3.14)
            rev_array.append(x)
        else:
            temp_array.append(x)
            rev_array.append(x)


    a=0.1
    v=0.1
    try:
        rob.movej(temp_array, a, v,wait=True)
    except Exception as e:
        print(e)
    while (abs(temp_array[0] - rob.getj()[0])) > 0.05:
        time.sleep(0.1)
        print("Sleep")

    try:
        rob.movej(rev_array, a, v,wait=True)
    except:
        pass

    rob.close()