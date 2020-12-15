import freenect
#import cv2 as cv
import numpy as np
import time
from navigation import *
import threading as th
from SETTINGS import *
from collision_avoidance_algorithm import *

def get_kinect_processed_data(data):
    data_m = np.where(data==0,9999,data)
    data_m = data_m[230:250,0:-10]
    data_m = np.amin(data_m, axis = 0)
    data_m = data_m/(10*(DISTANCE_LOOK/600))
    return data_m

depth_data = []
video_data = []

#dev is some pointer. data is the depth data 2d array. timestamp is a timestamp
def depth_func(dev, data, timestamp):
    if state_handler.shutdown_flag:
        sys.exit()
    global depth_data
    depth_data = data

def video_func(dev, data, timestamp):
    global video_data
    if state_handler.shutdown_flag:
        sys.exit()
    video_data = data

def background():
    mdev = freenect.open_device(freenect.init(), 0)
    freenect.set_depth_mode(mdev, freenect.RESOLUTION_MEDIUM, freenect.DEPTH_MM)
    freenect.runloop(dev=mdev, depth=depth_func, video=video_func)
    #freenect.runloop(dev=mdev, depth=depth_func)

def init_kinect():
    loop = th.Thread(name='background', target=background)
    loop.start()

