import urx
import robot_class
import cv2
import matplotlib.pyplot as plt
import numpy as np
from computer_vision import get_coords, get_circled_objects

speed = 0.3
prepickup_height = 0.3
pickup_height = 0.2

rw_tl = (0.72503, 0.43804, prepickup_height, 2.221, -2.221, 0)
rw_tr = (0.73363, -0.44639, prepickup_height, 2.221, -2.221, 0)
rw_bl = (0.06462, 0.40767, prepickup_height, 2.221, -2.221, 0)
rw_br = (0.11665, -0.43755, prepickup_height, 2.221, -2.221, 0)

rw_x_limts = [(rw_bl[0]+rw_br[0])/2,(rw_tl[0]+rw_tr[0])/2]
rw_y_limts = [(rw_tl[1]+rw_bl[1])/2,(rw_tr[1]+rw_br[1])/2]

yellow_bucket_coords = (0.11, 0.54, prepickup_height, 2.221, -2.221, 0)
orange_bucket_coords = (0.31, 0.54, prepickup_height, 2.221, -2.221, 0)
green_bucket_coords = (0.51, 0.54, prepickup_height, 2.221, -2.221, 0)


## Translate image coordinates into real world spatial values.
## Relative to robots base.
def im_to_rw(obj, rw_x_limts, rw_y_limts):
	imgSize = [640,480]
	rw_obj = [obj[1]/imgSize[1] * (rw_x_limts[1] - rw_x_limts[0]) + rw_x_limts[0], obj[0]/imgSize[0] * (rw_y_limts[1] - rw_y_limts[0]) + rw_y_limts[0]]
	return rw_obj

## Displayed image taken from camera with mask showing a singular, isolated color
def show_masked_world(rob, color = "yellow", show_interm = False):
	rob.rob.movel(rob.cameraPose, speed, speed)
	eroded, circles = get_circled_objects(rob.getImage(), color = color, show_interm = show_interm)

	for circle in circles:
		obj = [640-circle[0], circle[1]]

		ii = (obj[0])//128
		jj = obj[1]//96

		rw_cords = im_to_rw(obj, rw_x_limts, rw_y_limts)

		print("\tFound " + str(color) + " object in quadrant " + str([ii,jj]) + "\n\tImage cords are: " + str(obj) + ", translated real world cords are: " + str(rw_cords) + "\n")

	if show_interm:
		plt.imshow(eroded)

		plt.plot([128, 128],[0,480], color = "black")
		plt.plot([256, 256],[0,480], color = "black")
		plt.plot([384, 384],[0,480], color = "black")
		plt.plot([512, 512],[0,480], color = "black")

		plt.plot([0,640], [96, 96], color = "black")
		plt.plot([0,640], [192, 192], color = "black")
		plt.plot([0,640], [288, 288], color = "black")
		plt.plot([0,640], [384, 384], color = "black")
		plt.xlim([0,640])
		plt.ylim([0,480])
		plt.show()

	return eroded, circles

## Driver code behind the picking up operation
def pick_object(rob, iterations = 1, show_interm = False, color = "yellow"):
	for ii in range(iterations):
		rob.rob.movel(rob.defaultPose,0.3,speed)
		rob.rob.movel(rob.cameraPose,0.3,speed)
		obj, obj_remaining = get_coords(rob.getImage(), color = color, show_interm = show_interm)
		
		if obj != []:
			print("\tObject found in " + color + " mask of image at " + str(obj) + ". " + str(obj_remaining) + " objects of this color left")
			rw_obj = im_to_rw(obj, rw_x_limts, rw_y_limts)
			print("\t\tImage co-ordinates translated to " + str(rw_obj) + " in real world.")

			## These static offsets are used for robot ur5e2 only
			static_offsets = [
			[[-0.02,0.025], [-0.01, 0.01], [0,0], [0,0], [0,0]],
			[[-0.025, 0.01], [-0.02, 0], [0,0], [0,0], [0,0]],
			[[-0.03,0], [-0.02, -0.01], [-0.01,-0.01], [0,0], [0,0]],
			[[-0.03,-0.015], [-0.02, -0.01], [-0.01, -0.01], [0,0], [0,0]],
			[[-0.04, -0.03], [-0.02, -0.02], [-0.02, -0.01], [-0.03,0], [0,0]]]

			jj = obj[0]//128
			ii = 4-obj[1]//96

			print("\t\tStatic Offset for quadrant " + str(ii) + " " + str(jj) +" is: " + str(static_offsets[ii][jj]))
			print("\t\tPickup position: [" + str(rw_obj[0] + static_offsets[ii][jj][0]) + ", " + str(rw_obj[1] + static_offsets[ii][jj][1]) + "]")

			rw_obj_pose = (rw_obj[0] + static_offsets[ii][jj][0], rw_obj[1] + static_offsets[ii][jj][1], prepickup_height, 2.221, -2.221, 0)

			rob.rob.movel(rob.defaultPose,speed,speed)

			rob.rob.movel(rw_obj_pose,speed, speed)

			if color == "yellow":
				bucket = yellow_bucket_coords
			elif color == "orange":
				bucket = orange_bucket_coords
			elif color == "green":
				bucket = green_bucket_coords

			rob.pickplace_object(bucket)

			rob.rob.movel(rob.defaultPose, speed, speed)

		return obj_remaining


def single_image_pick_and_place(rob):
	rob.rob.movel(rob.cameraPose, speed, speed)

	yellow_eroded, yellow_objs = show_masked_world(rob, color = "yellow", show_interm = False)
	orange_eroded, orange_objs = show_masked_world(rob, color = "orange", show_interm = False)
	green_eroded, green_objs = show_masked_world(rob, color = "green", show_interm = False)

	img = np.array(rob.getImage())

	queue = list([])

	for obj in yellow_objs:
		print("Found yellow object at: " + str(obj))
		cv2.circle(img, (obj[0],obj[1]), 5, (255, 255, 0), 2)
		queue.append([[640-obj[0],obj[1]], yellow_bucket_coords])
	for obj in orange_objs:
		print("Found orange object at: " + str(obj))
		cv2.circle(img, (obj[0],obj[1]), 5, (255, 150, 0), 2)
		queue.append([[640-obj[0],obj[1]], orange_bucket_coords])
	for obj in green_objs:
		print("Found green object at: " + str(obj))
		cv2.circle(img, (obj[0],obj[1]), 5, (0, 255, 0), 2)
		queue.append([[640-obj[0],obj[1]], green_bucket_coords])

	img = np.fliplr(img)
	img = np.flipud(img)

	plt.imshow(img)
	plt.show()

	rob.rob.movel(rob.defaultPose, speed, speed)

	while queue:
		pos = queue.pop(0)
		im_obj = pos[0]

		rw_obj = im_to_rw(im_obj, rw_x_limts, rw_y_limts)

		static_offsets = [
		[[-0.02,0.025], [-0.01, 0.01], [0,0], [0,0], [0,0]],
		[[-0.025, 0.01], [-0.02, 0], [0,0], [0,0], [0,0]],
		[[-0.03,0], [-0.02, -0.01], [-0.01,-0.01], [0,0], [0,0]],
		[[-0.03,-0.015], [-0.02, -0.01], [-0.01, -0.01], [0,0], [0,0]],
		[[-0.04, -0.03], [-0.02, -0.02], [-0.02, -0.01], [-0.03,0], [0,0]]]

		jj = im_obj[0]//128
		ii = 4-im_obj[1]//96

		rw_obj_pose = (rw_obj[0] + static_offsets[ii][jj][0], rw_obj[1] + static_offsets[ii][jj][1], prepickup_height, 2.221, -2.221, 0)

		rob.rob.movel(rw_obj_pose,speed, speed)

		rob.pickplace_object(pos[1])

	rob.rob.movel(rob.defaultPose, speed, speed)
		

	print("************************")
	print("Pick and Place complete.")
	print("There were " + str(len(yellow_objs)) + " yellow objects picked up.")
	print("There were " + str(len(orange_objs)) + " orange objects picked up.")
	print("There were " + str(len(green_objs)) + " green objects picked up.")
	print("************************")
