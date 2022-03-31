# This program detects the green bucket in the image and draws a circle around
# it. It is now easy to extract the image coordinates of circle origins.
# 
# Sources:
# https://docs.opencv.org/master/d4/d70/tutorial_hough_circle.html
# https://docs.opencv.org/master/dd/d1a/group__imgproc__feature.html#ga47849c3be0d0406ad3ca45db65a25d2d
# https://www.thepythoncode.com/article/detect-shapes-hough-transform-opencv-python

# TODO: Fine tune cv.HoughCircles() parameters for other objects.

import numpy as np
import cv2 as cv

def show_image(name, img, dim):
    """
    Display an image in a new window.
    
    name: a string, the name of the window.\n
    image: numpy array of the image to be shown.\n
    dim: tuple contains the width and height (in pixels) of the image.
    """
    cv.namedWindow(name, cv.WINDOW_NORMAL)
    cv.resizeWindow(name, dim)
    cv.imshow(name, img)


img = cv.imread('object_recognition/Buckets.png')
# Resize (shrink) the shown window because the original image is very large.
SCALE_FACTOR = 1/6
HEIGHT, WIDTH, CHANNELS = img.shape

width  = int(SCALE_FACTOR * WIDTH)
height = int(SCALE_FACTOR * HEIGHT)
dim = (width, height)

hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# Range of green bucket.
lower_range_green_bucket = np.array([174/2, 100,  33])
upper_range_green_bucket = np.array([183/2, 255, 255])
green_bucket_mask = cv.inRange(hsv, lower_range_green_bucket, upper_range_green_bucket)
green_bucket_mask = cv.bitwise_and(img, img, mask=green_bucket_mask)

# Find circles from mask (must convert to GRAY).
# Note: Can change which mask is used so that cv.HoughCircles() will only be
# searching at the identified objects themselves. This heavily reduces the
# chance of finding a "ghost circle."
cimg = cv.cvtColor(green_bucket_mask, cv.COLOR_HSV2RGB)
cimg = cv.cvtColor(cimg, cv.COLOR_RGB2GRAY)
cimg = cv.medianBlur(cimg, 5)
circles = cv.HoughCircles(cimg, cv.HOUGH_GRADIENT, dp=0.9, minDist=500, param1=100, param2=30, minRadius=50, maxRadius=1000)

# Draw all found circles back on original image. 
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        center = (i[0], i[1])
        # Circle center.
        cv.circle(img, center, 1, (0, 0, 255), 3)
        # Circle outline.
        radius = i[2]
        cv.circle(img, center, radius, (0, 255, 0), 3)

show_image('Circles', img, dim)

cv.waitKey(0)
cv.destroyAllWindows()