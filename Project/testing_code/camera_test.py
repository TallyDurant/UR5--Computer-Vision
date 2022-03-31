import urx
import numpy as np
import socket
from PIL import Image
import time
import urllib.request
from selenium import webdriver

HOST = "192.168.1.101"
PORT = 30002
url  = "http://192.168.1.101:4242/current.jpg?annotations=on"

ROBOT_LOADED = 0

try:
    rob = urx.Robot(HOST)
    ROBOT_LOADED = 1
except:
    print("error connecting")
if ROBOT_LOADED:
    while True:
        driver = webdriver.Chrome()
        driver.get(url)
        driver.refresh()
        driver.close()
        urllib.request.urlretrieve(url,"current.jpg")
        time.sleep(0.1)

    rob.close()


"""
from PIL import Image
import requests
from io import BytesIO

url = "https://baobab-poseannotation-appfile.s3.amazonaws.com/media/project_5/images/images01/01418849d54b3005.o.1.jpg"
response = requests.get(url)
img = Image.open(BytesIO(response.content))
img.show()
"""