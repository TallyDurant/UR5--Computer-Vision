# This program detects objects based on their colour using HSV. It opens
# several windows, each detecting a different object.

# TODO: Fine tune pick-and-place object detection (orange, yellow and green
# colours).

import cv2 as cv
import numpy as np

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
#img = cv.imread('object_recognition/Buckets_side.jpg')
#img = cv.imread('object_recognition/Objects.jpg')


# Resize (shrink) the shown window because the original image is very large.
SCALE_FACTOR = 1/6
HEIGHT, WIDTH, CHANNELS = img.shape

width  = int(SCALE_FACTOR * WIDTH)
height = int(SCALE_FACTOR * HEIGHT)
dim = (width, height)

show_image('Original', img, dim)

# Convert to HSV.
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)


# Detect the objects to be picked and placed.
# Range of orange objects.
lower_range_orng1 = np.array([173, 100, 100])
upper_range_orng1 = np.array([179, 255, 255])

lower_range_orng2 = np.array([0, 100, 100])
upper_range_orng2 = np.array([1, 255, 255])

orng1_mask = cv.inRange(hsv, lower_range_orng1, upper_range_orng1)
orng2_mask = cv.inRange(hsv, lower_range_orng2, upper_range_orng2)
orng_mask = cv.bitwise_or(orng1_mask, orng2_mask)
orng_mask = cv.bitwise_and(img, img, mask=orng_mask)

# Orange objects should show up as white, everything else black.
show_image('Orange Objects', orng_mask, dim)

# Range of yellow objects.
lower_range_yel = np.array([30, 100, 100])
upper_range_yel = np.array([42, 255, 255])
yel_mask = cv.inRange(hsv, lower_range_yel, upper_range_yel)
yel_mask = cv.bitwise_and(img, img, mask=yel_mask)
show_image('Yellow Objects', yel_mask, dim)

# Range of green objects.
lower_range_grn = np.array([54, 100, 50])
upper_range_grn = np.array([62, 255, 255])
grn_mask = cv.inRange(hsv, lower_range_grn, upper_range_grn)
grn_mask = cv.bitwise_and(img, img, mask=grn_mask)
show_image('Green Objects', grn_mask, dim)


# Detect the buckets. They have the following hue ranges (0-359):
#   - Red: 0-7
#   - Green: 174-183
#   - Blue: 206-255
# 
# Note: Need to divide hue values by 2 to normalise to 0-180 range that
# cv.inRange() requires.

# Range of red bucket.
lower_range_red_bucket = np.array([0/2, 100, 76])
upper_range_red_bucket = np.array([7/2, 255, 255])
red_bucket_mask = cv.inRange(hsv, lower_range_red_bucket, upper_range_red_bucket)
red_bucket_mask = cv.bitwise_and(img, img, mask=red_bucket_mask)
show_image('Red Bucket', red_bucket_mask, dim)

# Range of green bucket.
lower_range_green_bucket = np.array([174/2, 100,  33])
upper_range_green_bucket = np.array([183/2, 255, 255])
green_bucket_mask = cv.inRange(hsv, lower_range_green_bucket, upper_range_green_bucket)
green_bucket_mask = cv.bitwise_and(img, img, mask=green_bucket_mask)
show_image('Green Bucket', green_bucket_mask, dim)

# Range of blue bucket.
lower_range_blue_bucket = np.array([206/2, 100,  10])
upper_range_blue_bucket = np.array([255/2, 255, 255])
blue_bucket_mask = cv.inRange(hsv, lower_range_blue_bucket, upper_range_blue_bucket)
blue_bucket_mask = cv.bitwise_and(img, img, mask=blue_bucket_mask)
show_image('Blue Bucket', blue_bucket_mask, dim)


cv.waitKey(0)
cv.destroyAllWindows()