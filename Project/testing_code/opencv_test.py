import cv2
import numpy as np 
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb, rgb_to_hsv
from PIL import Image

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



"""img = Image.open('object_recognition/Figure_4.png').convert("RGB")

rgb_img = np.array(img)
#hsv_img = cv2.cvtColor(rgb_img,cv2.COLOR_RGB2HSV)



mask_orange = (150, "lb",50, "ub" ,50, "ub")
mask_green = (85,"ub",85, "lb", 30, "ub")
mask_yellow = (100,"lb", 125, "lb", 50, "ub")

fig,sub = plt.subplots(1,3)


sub[0].imshow(maskImg(rgb_img,mask_orange))
rgb_img = np.array(img)
sub[1].imshow(maskImg(rgb_img,mask_green))
rgb_img = np.array(img)
sub[2].imshow(maskImg(rgb_img,mask_yellow))
#plt.imshow(maskImg(rgb_img,mask_yellow))
plt.show()"""



"""img = cv2.imread('object_recognition/Figure_6.png')
edges = cv2.Canny(img,100,200)


rgb_array= np.array(img)
hsv_img = cv2.cvtColor(rgb_array,cv2.COLOR_BGR2HSV)

lbOrange = np.array([10,20,20])
ubOrange = np.array([25,255,255])

#mask = cv2.inRange(hsv_img, lbOrange, ubOrange)
mask = cv2.inRange(hsv_img,(10,25,25),(25,255,255))

res = cv2.bitwise_and(img,img, mask = mask)
print(res)

plt.imshow(res)
plt.show()"""

"""cv2.imshow('frame',img)
cv2.imshow('mask', mask)
cv2.imshow('res', res)"""

#cv2.imshow("s channel", hsv_img)
#cv2.waitKey(5000)