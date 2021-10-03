import cv2

# Function to get the center of boundary box
def getCenter(frame, bbox):
    x = getXCenter(bbox)
    y = getYCenter(bbox)
    center = (x, y)
    cv2.putText(frame, "Center: " + str(int(x)) + ", " + str(int(y)), (0, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    return center


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