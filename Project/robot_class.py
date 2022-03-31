import time
import urx
import requests

from PIL import Image
from io import BytesIO
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

bucket_coords = (0.31, 0.54, 0.3, 2.221, -2.221, 0)

# The primary class containing robot-specific operations and testing functions.
class RobotClass():
    def __init__(self, ip, default, camera):
        self.ip = ip
        self.defaultPose = default
        self.cameraPose = camera
        self.connected = False
        attempts = 0
        self.image = 0

        while (not self.connected) & (attempts < 10):
            try:
                self.rob = urx.Robot(self.ip)
                self.connected = True
                print("Successfully connected to robot " + str(ip))
            except:
                attempts += 1
                print("Retrying connection: " + str(attempts))
                time.sleep(0.5)
        if self.connected:
            self.gripper = Robotiq_Two_Finger_Gripper(self.rob)
            self.gripper_open()

    # assumes already above and the gripper is open
    def pickplace_object(self, color_bucket_coords):
        self.rob.translate((0, 0, -0.1), 0.1, 0.1)
        self.gripper_close()
        self.rob.translate((0, 0, 0.1), 0.1, 0.1)
        self.rob.movel(color_bucket_coords, 0.25,0.25)
        self.gripper_open()

    # Access the URE5 camera and returns the 640x480 image.
    def getImage(self):
        url = "http://" + str(self.ip) + ":4242/current.jpg?annotations=on"
        requests.get(url)
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        self.image = img
        return img

    # A testing function to display the current image in focus.
    def showImage(self):
        if self.image != 0:
            self.image.show()

    def gripper_open(self):
        self.gripper.open_gripper()

    def gripper_close(self):
        self.gripper.close_gripper()

    def resetPose(self):
        self.rob.movel(self.defaultPose,0.1,0.314)

    def close(self):
        self.rob.close()

    def getPose(self):
        return self.rob.get_pose()

    def getLocation(self):
        return self.rob.getl()

    def getX(self):
        return self.rob.getl()[0]

    def getY(self):
        return self.rob.getl()[1]

    def getZ(self):
        return self.rob.getl()[2]
