import freenect
#import cv2 as cv
import numpy as np
import time
from navigation_old import *
import threading as th

def show(data):
    data_m = np.where(data==0,9999,data)
    data_m = data_m[230:250,0:-10]
    data_m = np.amin(data_m, axis = 0)
    runVisual(data_m)

depth_data = []
video_data = []

#dev is some pointer. data is the depth data 2d array. timestamp is a timestamp
def depth_func(dev, data, timestamp):
    global depth_data
    depth_data = data

def video_func(dev, data, timestamp):
    global video_data
    video_data = data

def background():
    mdev = freenect.open_device(freenect.init(), 0)
    freenect.set_depth_mode(mdev, freenect.RESOLUTION_MEDIUM, freenect.DEPTH_MM)
    freenect.runloop(dev=mdev, depth=depth_func, video=video_func)
    #freenect.runloop(dev=mdev, depth=depth_func)

loop = th.Thread(name='background', target=background)
loop.start()

while len(depth_data)==0:
    x=1

while 1:
    show(depth_data)


