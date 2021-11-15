import flask
from flask import request
from flask_cors import CORS

import cv2
import asyncio
import json
import sys
import threading

import util

app = flask.Flask(__name__)
cors = CORS(app)

objectTracker = object()

# Main function to respond to requests
@app.route("/", methods=["GET"])
def home():
    response = asyncio.run(build_response())
    return json.dumps(response), {"Content-Type": "application/json"}


# Build a response to send to the client
# asynchronously waiting for external APIs
async def build_response():
    response = {}
    response["results"] = await get_position()
    return response


# Function to build a json response containing the coordinates of the boundary box
async def get_position():
    response = {}
    response["center"] = objectTracker.getCenter()
    response["x"] = objectTracker.getXCenter()
    response["y"] = objectTracker.getYCenter()
    print(response)
    return json.dumps(response)


# Generate an JSON error response
def generateError(reason):
    return {
        "reasons": [
            {
                "language": "en",
                "message": reason
            }
        ]
    }


# Class for the object tracker
class ObjectTracker():
    def __init__(self, capture, ret, frame, bbox, tracker, draw):
        self._capture = capture
        self._ret = ret
        self._frame = frame
        self._bbox = bbox
        self._tracker = tracker
        self._draw = draw
        self._points = []

           
    # Function to maintain a rectangle to define the boundary box around the tracked object 
    def drawBoundaryBox(self, frame, bbox):
        x = int(bbox[0])
        y = int(bbox[1])
        width = int(bbox[2])
        height = int(bbox[3])
        p1 = (x, y)
        p2 = (x + width, y + height)
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)


    # Function to get the center of boundary box
    def getCenter(self):
        xcenter = self.getXCenter()
        ycenter = self.getYCenter()
        return xcenter, ycenter


    # Function to get the x coordinate of the center of the boundary box
    def getXCenter(self):
        x = int(self._bbox[0])
        width = int(self._bbox[2])
        xCenter = x + (width / 2)
        return xCenter


    # Function to get the y coordinate of the center of the boundary box
    def getYCenter(self):
        y = int(self._bbox[1])
        height = int(self._bbox[3])
        yCenter = y + (height / 2)
        return yCenter


    # Function to build a json response containing the coordinates of the boundary box
    async def get_position(self):
        response = {}
        # response["center"] = self.getCenter()
        response["x"] = self.getXCenter()
        response["y"] = self.getYCenter()
        print(response)
        return json.dumps(response)


    # Main method to run object tracker
    def runTracker(self):
        # Loop to maintain video capture device input and display
        while(self._capture.isOpened()):
            timer = cv2.getTickCount() 
            self._ret, self._frame = self._capture.read()
            
            # ret will return 'True' if video caputre is good and 'False' if video capture is bad
            if not self._ret:
                break

            # Update the tracker every frame
            self._ret, self._bbox = self._tracker.update(self._frame)

            # Display 'Tracking' if tracking is successful and 'Lost' if tracking is unsuccessful
            if self._ret:
                self.drawBoundaryBox(self._frame, self._bbox)
                cv2.putText(self._frame, "Tracking", (0, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            else:
                cv2.putText(self._frame, "Lost", (0, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

            # Calculate and display frames per second (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
            cv2.putText(self._frame, "FPS : " + str(int(fps)), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            # Draw lines according to the position of the center of the boundary box and display the center of the boundary box
            if self._draw == True:
                # xcenter, ycenter = util.getCenter(bbox)
                xcenter = self.getXCenter()
                ycenter = self.getYCenter()
                # print(xcenter, ",", ycenter)
                cv2.putText(self._frame, "Center: " + str(int(xcenter)) + ", " + str(int(ycenter)), (0, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                cv2.putText(self._frame, "Drawing", (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                
            else:
                cv2.putText(self._frame, "Stopped", (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)

            # Change video capture input to grayscale
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Display video capture
            #cv2.imshow('object-tracker', gray)
            cv2.imshow('object-tracker', self._frame)

            # Toggle drawing (activation of drawing pen)
            if cv2.waitKey(1) & 0xFF == ord(' '):
                if self._draw == True:
                    self._draw = False
                else:
                    self._draw = True

            # Press 'esc' key to exit
            if cv2.waitKey(1) & 0xFF == 27:
                # Kill all video capture processes and displays
                self._capture.release()
                cv2.destroyAllWindows()

    
    @property
    def capture(self):
        return self._capture

    def ret(self):
        return self._ret

    def frame(self):
        return self._frame

    def bbox(self):
        return self._bbox

    def tracker(self):
        return self._tracker

    def draw(self):
        return self._draw

    def points(self):
        return self._points


def initializeTracker():
    draw = False

    # Declare video capture device (webcam)
    capture = cv2.VideoCapture(0)

    # Check video capture device works
    if not capture.isOpened():
        print("Could not open video capture device")
        sys.exit()

    # Declare the type of tracking used
    tracker = cv2.TrackerCSRT_create()

    # Read the first frame and initialize the boundary box for the tracker
    ret, frame = capture.read()
    bbox = cv2.selectROI(frame, False)
    tracker.init(frame, bbox)

    return capture, ret, frame, bbox, tracker, draw


def getTracker():
    return objectTracker


# Function to run the API
def runAPI(DEBUG, PORT, SSL_CONTEXT):
    app.config["DEBUG"] = DEBUG
    app.run(port=PORT, ssl_context=SSL_CONTEXT)
 

# Main method to run API
if __name__ == "__main__":
    PORT = 5000  # port to run the server on
    DEBUG = False  # whether to run in debug mode
    SSL_CONTEXT = None  # indicates whether to use HTTPS

    if "--debug" in sys.argv:
        DEBUG = True

    if "--https" in sys.argv:
        SSL_CONTEXT = "ahdoc"

    capture, ret, frame, bbox, tracker, draw = initializeTracker()
    objectTracker = ObjectTracker(capture, ret, frame, bbox, tracker, draw)
    trackerThread = threading.Thread(target=objectTracker.runTracker)

    apiThread = threading.Thread(target=runAPI, args=(DEBUG, PORT, SSL_CONTEXT,))

    apiThread.start()
    trackerThread.start()

    apiThread.join()
    trackerThread.join()

    print("Program Terminated")