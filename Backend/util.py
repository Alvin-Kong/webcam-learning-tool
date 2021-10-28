import cv2
import object_tracker

def getFrame():
    return object_tracker.getFrame()

def getBBox():
    return object_tracker.getBBox()


# Function to get the center of boundary box
def getCenter(bbox):
    xcenter = getXCenter(bbox)
    ycenter = getYCenter(bbox)
    return xcenter, ycenter


# Function to get the x coordinate of the center of the boundary box
def getXCenter(bbox):
    x = int(bbox[0])
    width = int(bbox[2])
    xCenter = x + (width / 2)
    return xCenter


# Function to get the y coordinate of the center of the boundary box
def getYCenter(bbox):
    y = int(bbox[1])
    height = int(bbox[3])
    yCenter = y + (height / 2)
    return yCenter