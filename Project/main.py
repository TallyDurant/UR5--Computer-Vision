import robot_class
import computer_vision
import pick_and_place


def show_world():
	rob.rob.movel(defaultPose, speed, speed)
	rob.rob.movel(cameraPose, speed, speed)
	rob.getImage()
	rob.showImage()

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Testing code designed to extract gridded offset values in real time
def manual_offset_testing():
	key = "g"

	while key != "e":
		if key == "g":
			show_masked_world(color = "yellow")
		#rob.rob.movel(defaultPose,speed,speed)

		key = input("image x")
		if key != "e":
			x = int(key)
			y = int(input("image y"))
			offx = float(input("offset x"))
			offy = float(input("offset y"))

			manual_correction(pos = [640-x, y], offset = [offx,offy])

			key = input()

## Moves to provided [x,y] with specified offset, testing code to ascertain grid offsets
def manual_correction(pos = [0,0], offset = [0,0]):
	print("Manual correction to: [" + str(pos[0]) + ", " + str(pos[1]) + "]")

	ii = pos[0]//128
	jj = pos[1]//96

	print ("offset " + str(ii) + " " + str(jj))

	rw_obj = im_to_rw(pos,rw_x_limts, rw_y_limts)

	rw_obj_pose = (rw_obj[0] + offset[0], rw_obj[1] + offset[1], prepickup_height, 2.221, -2.221, 0)

	rob.rob.movel(rw_obj_pose, 0.1, 0.1)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

UR5e = 2
speed = 0.3
prepickup_height = 0.3
pickup_height = 0.2


if UR5e == 1:
	cameraPose = (0.28235, 0.13005, 0.900, 2.443, -2.334, 0.865)

	#base height of object 184
	rw_tl = (0.560, -0.38715, 0.18484, 2.221, -2.221, 0)
	rw_tr = (0.9964, 0.41368, 0.22078, 2.221, -2.221, 0)
	rw_bl = (0.71085, -0.42338, 0.2082, 2.221, -2.221, 0)
	rw_br = (0.64301, 0.39963, 0.20777, 2.221, -2.221, 0)

elif UR5e == 2:
	cameraPose = (0.28013, -0.12439, 0.93497, 2.580, -2.520, 0.690)

	#base height of object 184
	rw_tl = (0.72503, 0.43804, prepickup_height, 2.221, -2.221, 0)
	rw_tr = (0.73363, -0.44639, prepickup_height, 2.221, -2.221, 0)
	rw_bl = (0.06462, 0.40767, prepickup_height, 2.221, -2.221, 0)
	rw_br = (0.11665, -0.43755, prepickup_height, 2.221, -2.221, 0)

	rw_x_limts = [(rw_bl[0]+rw_br[0])/2,(rw_tl[0]+rw_tr[0])/2]
	print("RW X limits " + str(rw_x_limts))
	rw_y_limts = [(rw_tl[1]+rw_bl[1])/2,(rw_tr[1]+rw_br[1])/2]
	print("RW Y limits " + str(rw_y_limts))

	yellow_bucket_coords = (0.28, 0.54, prepickup_height, 2.221, -2.221, 0)
	orange_bucket_coords = (0.31, 0.54, prepickup_height, 2.221, -2.221, 0)
	green_bucket_coords = (0.34, 0.54, prepickup_height, 2.221, -2.221, 0)

defaultPose = (0.49225, -0.13405, 0.48888, 2.21, -2.221, 0)

IP = input("Enter ip address: ")
rob = robot_class.RobotClass(IP, defaultPose, cameraPose)

if rob.connected:
	obj_remaining = 1

	function = input("Select fuction: \n1 - Manual, 2- Automatic Re-image, 3- Camera, 4- Automatic Single Image\te- exit...\n")

	if (function == "Manual") or (function == "1"):
		print("Running manual pick and place.")
		color = ""
		while color != "e":
			color = input("Color to pick: ")
			if color != "e":
				obj_remaining = pick_and_place.pick_object(rob, iterations = 1, show_interm = True, color = color)

	elif (function == "Automatic") or (function == "2"):
		print("Running automatic pick and place with re-image.")
		complete = False
		colors = ["yellow", "orange", "green"]
		pickedup = [0,0,0]
		color = 0
		while not complete:
			if obj_remaining > 0:
				obj_remaining = pick_and_place.pick_object(rob, iterations = 1, show_interm = False, color = colors[color])
				pickedup[color] += 1
			else:
				color += 1
				obj_remaining = 1
			if color > 2:
				complete = True

		print("************************")
		print("Pick and Place complete.")
		print("There were " + str(pickedup[0]) + " yellow objects picked up.")
		print("There were " + str(pickedup[1]) + " orange objects picked up.")
		print("There were " + str(pickedup[2]) + " green objects picked up.")
		print("************************")


	elif (function == "Camera") or (function == "3"):
		key = ""
		while (key != "exit") and (key != "e"):
			key = input("Menu:\ne-exit\tc-Camera Pose\ty-Yellow Mask\to-Orange Mask\tg-Green Mask\n")

			if key == "c":
				rob.rob.movel(cameraPose,speed,speed)
			elif key == "y":
				pick_and_place.show_masked_world(rob, color = "yellow", show_interm = True)
			elif key == "o":
				pick_and_place.show_masked_world(rob, color = "orange", show_interm = True)
			elif key == "g":
				pick_and_place.show_masked_world(rob, color = "green", show_interm = True)
	elif function == "4":
		print("Running automatic pick and place with single image.")

		pick_and_place.single_image_pick_and_place(rob)

	rob.close()
else:
	print("Could not connect to robot after 10 attempts. Check IP address and connected network.")