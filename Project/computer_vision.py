import cv2
import numpy as np
import matplotlib.pyplot as plt

def maskImg(img, mask):
    outimg = np.array(img)
    for rowCount, row in enumerate(outimg):
        for colCount, col in enumerate(row):
            if mask[1] == 'lb':
                maskedRed = col[0] > mask[0]
            else:
                maskedRed = col[0] < mask[0]
            if mask[3] == 'lb':
                maskedGreen = col[1] > mask[2]
            else:
                maskedGreen = col[1] < mask[2]
            if mask[5] == 'lb':
                maskedBlue = col[2] > mask[4]
            else:
                maskedBlue = col[2] < mask[4]


            if not (maskedRed & maskedGreen & maskedBlue):
                outimg[rowCount,colCount] = (0,0,0) 

    return outimg

# Driving function behind the computer vision component, returns [x,y] of a desired object in image
def get_coords(base_img, color = "yellow", show_interm = False):

    if color == "yellow":
        mask_yellow = (70,"lb", 70, "lb", 40, "ub")
        img_yellow = maskImg(base_img, mask_yellow)
        img = img_yellow
    elif color == "green":
        mask_green = (40,"ub",50, "lb", 30, "ub")
        img_green = maskImg(base_img, mask_green)
        img = img_green
    elif color == "orange":
        mask_orange = (85, "lb",100, "ub" ,50, "ub")
        img_orange = maskImg(base_img, mask_orange)
        img = img_orange
    else:
        print("Color not recognised, an error has occured")

    kernal = np.ones((5,5), np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, black_white = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    dilated = cv2.dilate(black_white, kernal, iterations = 2)
    eroded = cv2.erode(dilated, kernal, iterations = 3)

    if show_interm:
        plt.imshow(eroded)
        plt.show()

    countours, c = cv2.findContours(eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if countours:
        pos = cv2.moments(countours[0])
        if pos["m00"] != 0:
            x = int(pos["m10"]/pos["m00"])
            y = int(pos["m01"]/pos["m00"])
        else:
            x = 0
            y = 0

        obj = [640-x,y]
        obj_remaining = len(countours) - 1
    else:
        obj = []
        obj_remaining = 0

    return obj, obj_remaining

# Used to return entire selection of available objects in the image. 
##  Only applies to a single color at a time. Circles object in returned image
def get_circled_objects(base_img, color = "yellow", show_interm = False):
    if show_interm:
        plt.imshow(base_img)
        plt.show()

    if color == "yellow":
        mask_yellow = (70,"lb", 70, "lb", 40, "ub")
        img_yellow = maskImg(base_img, mask_yellow)
        img = img_yellow
    elif color == "green":
        mask_green = (40,"ub",50, "lb", 30, "ub")
        img_green = maskImg(base_img, mask_green)
        img = img_green
    elif color == "orange":
        mask_orange = (85, "lb",100, "ub" ,50, "ub")
        img_orange = maskImg(base_img, mask_orange)
        img = img_orange
    else:
        print("Color not recognised, an error has occured")

    if show_interm:
        plt.imshow(img)
        plt.show()

    kernal = np.ones((5,5), np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if show_interm:
        plt.imshow(gray)
        plt.show()

    ret, black_white = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    if show_interm:
        plt.imshow(black_white)
        plt.show()

    dilated = cv2.dilate(black_white, kernal, iterations = 2)

    if show_interm:
        plt.imshow(dilated)
        plt.show()

    eroded = cv2.erode(dilated, kernal, iterations = 3)


    if show_interm:
        plt.imshow(eroded)
        plt.show()

    countours, c = cv2.findContours(eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    circles = []

    for ii in range(len(countours)):
        pos = cv2.moments(countours[ii])
        x=0
        y=0
        if pos["m00"] != 0:
            x = int(pos["m10"]/pos["m00"])
            y = int(pos["m01"]/pos["m00"])
            cv2.circle(eroded, (x,y), 5, (0, 0, 255), 2)
            circles.append([x,y])

    return eroded, circles