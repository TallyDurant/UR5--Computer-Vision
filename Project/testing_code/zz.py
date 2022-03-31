import cv2
from opencv_test import maskImg
from PIL import Image
import numpy as np 




img = Image.open('object_recognition/Figure_2.png').convert("RGB")

rgb_img = np.array(img)

mask_orange = (150, "lb",50, "ub" ,50, "ub")
mask_green = (85,"ub",85, "lb", 30, "ub")
mask_yellow = (100,"lb", 125, "lb", 50, "ub")

masked = maskImg(rgb_img, mask_yellow)

(x,y), r =cv2.minEnclosingCircle(masked)

center = (int(x),int(y))
radius = int(r)
img = cv2.circle(img,center,radius,(0,255,0),2)