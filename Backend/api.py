import flask
from flask import Flask, request
from flask_cors import CORS

import cv2
import asyncio
import json
import sys
import threading
import os
import requests

import tracing

app = Flask(__name__) 
cors = CORS(app)

objectTracker = object()
getTraceData = None
isOff = False
tempPath = {}


# ====================================================================================================================
# ======================================================= API ========================================================
# Main function to respond to requests
@app.route("/", methods=['GET', 'POST'])
def home():
    # GET method
    if request.method == 'GET':
        query = request.args
        getTemplatePath = isOff = None
        response = {}

        if "getTemplatePath" in query:
            getTemplatePath = query["getTemplatePath"]
            response["template_response"] = asyncio.run(build_template_response(getTemplatePath))

        if "isOff" in query:
            isOff = query["isOff"]
            if isOff == "false" or None:
                response["tracking_response"] = asyncio.run(build_tracking_response())
        
        return json.dumps(response), {"Content-Type": "application/json"}

    if request.method == 'POST':
        query = json.loads(request.data.decode('utf-8'))
        postTemplatePath = file = kill = None
        response = {}

        if "postTemplatePath" in query:
            postTemplatePath = query["postTemplatePath"]
            tempPath["postTemplatePath"] = postTemplatePath

        if "file" in query:
            file = query["file"]
            file = file.split(',')[1]
            response["tracing_stats_response"] = asyncio.run(get_tracing_stats(file))

        return json.dumps(response), {"Content-Type": "application/json"}

    else:
        return json.dumps(generateError("Request method not recognized. Please use 'GET' or 'POST' only.")), 300, {
            "Content-Type": "application/json"}


# ================================================== Error Handling ==================================================
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


# ============================================== Build Response Methods ==============================================
# Build a tracing response to send to the client
async def build_tracing_response():
    response = {}
    response["tracing_results"] = await get_tracing_stats()
    return response


# Build a response to send the template file that will be used for tracing mode
async def build_template_response(choice):
    response = {}
    response["template_results"] = await get_template(choice)
    return response


# Build a tracking response to send to the client
async def build_tracking_response():
    response = {}
    response["tracking_results"] = await get_position()
    return response


# ==================================================== Get Methods ====================================================
# Function to build a json response containing the returned data from tracing.py's trace method
async def get_tracing_stats(f):
    response = {}
    response["rating"], response["percentage"] = tracing.trace(tempPath["postTemplatePath"], f)
    return response


# Function to build a json response containing the file path to the template file to be used during tracing mode
async def get_template(choice):
    response = {}
    response["template"] = tracing.getOriginal(choice)
    return response


# Function to build a json response containing the coordinates of the boundary box
async def get_position():
    response = {}
    response["center"] = objectTracker.getCenter()
    response["x"] = objectTracker.getXCenter()
    response["y"] = objectTracker.getYCenter()
    response["draw"] = objectTracker._draw
    return response
# =====================================================================================================================
# =====================================================================================================================


# =====================================================================================================================
# ================================================= Object Tracker ====================================================
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


    # Main method to run object tracker
    def runTracker(self):
        # Loop to maintain video capture device input and display
        while(self._capture.isOpened()):
            timer = cv2.getTickCount() 
            self._ret, self._frame = self._capture.read()
            self._frame = cv2.flip(self._frame, 1)
            
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
                self._draw = False

            # Calculate and display frames per second (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
            cv2.putText(self._frame, "FPS : " + str(int(fps)), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            # Draw lines according to the position of the center of the boundary box and display the center of the boundary box
            if self._draw == True:
                xcenter = self.getXCenter()
                ycenter = self.getYCenter()
                cv2.putText(self._frame, "Center: " + str(int(xcenter)) + ", " + str(int(ycenter)), (0, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                cv2.putText(self._frame, "Drawing", (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                
            else:
                cv2.putText(self._frame, "Stopped", (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)


            # Display the webcam input with tracker on
            cv2.imshow('object-tracker', self._frame)


            # Toggle drawing (activation of drawing pen)
            if cv2.waitKey(1) & 0xFF == ord(' '):
                if self._draw == True:
                    self._draw = False
                else:
                    self._draw = True


            # Recalibrate tracker when object is lost
            if cv2.waitKey(1) & 0xFF == ord('r'):
                self._capture.release()
                cv2.destroyAllWindows()
                capture, ret, frame, bbox, tracker, draw = initializeTracker()
                newTracker = ObjectTracker(capture, ret, frame, bbox, tracker, draw)
                newTracker.runTracker


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
# =====================================================================================================================
# =====================================================================================================================


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
    frame = cv2.flip(frame, 1)
    bbox = cv2.selectROI(frame, False)
    tracker.init(frame, bbox)

    return capture, ret, frame, bbox, tracker, draw


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