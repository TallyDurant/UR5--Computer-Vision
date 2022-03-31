import urx
from math import radians
import robot_class, pose_class

#IP = "192.168.1.101"
IP = "192.168.1.123"

# THINGS
# x
defaultPose = (0, radians(-105), radians(-30), radians(-135), radians(90), 0)

rob = robot_class.RobotClass(IP, defaultPose)
rob.resetPose()
rob.gripper_open()

location = (radians(54.1), radians(-108.0), radians(-112.1), radians(-49.0), radians(91.3), radians(-75))
bucket_loc = (radians(-24.6), radians(-78.9), radians(-94.4), radians(-93.5), radians(91.8), radians(-97.5))
object_location = [-250, 500, -200]
bucket_location = [350, 200, 100]

pickup_pose = pose_class.Pose(object_location[0], object_location[1], object_location[2]+50, radians(180), radians(180), radians(0))

dropoff_pose = pose_class.Pose(bucket_location[0], bucket_location[1], bucket_location[2]+200, radians(180), radians(180), radians(0))


#rob.move_to_location((-250, 500, -150, radians(180), radians(180), radians(0)), 0.3, 0.05)
#rob.move_to_location((500, 250, 0, radians(180), radians(180), radians(0)), 0.3, 0.05)
#newvar = rob.rob.getl()
rob.rob.movej(location, 0.3, 0.1)
rob.gripper_close()
rob.rob.movej(bucket_loc, 0.3, 0.15)
rob.gripper_open()
rob.resetPose()
#pickup_pose.getPose()
"""
rob.translate(0,0,-50, 0.3, 0.05)

rob.gripper_close()

rob.translate(0,0,50, 0.3, 0.05)

rob.move_to_location(dropoff_pose.getPose())

rob.translate(0,0,-50,0.3,0.05)

rob.gripper_open()

rob.translate(0,0,50,0.3,0.05)

rob.resetPose()
"""