from PIL import Image
import requests
from io import BytesIO
import numpy as np
import colorsys
import matplotlib as plt

IP = "192.168.1.101"
PORT = "4242"

#rob = urx.Robot(IP)

url = "http://" + IP + "." + PORT + "/current.jpg?annotations=on"
url = "http://192.168.1.101:4242/current.jpg?annotations=on"
response = requests.get(url)
img = Image.open(BytesIO(response.content))

rgb_array= np.array(img)

hsv_array = plt.colors.rgb_to_hsv(rgb_array)


