import cv2
import sys

if __name__ == '__main__':

    # Declare video capture device (webcam)
    capture = cv2.VideoCapture(0)

    # Check video capture device works
    if not capture.isOpened():
        print 
        "Could not open video capture device"
        sys.exit()

    # Declare the type of tracking used
    tracker = cv2.TrackerKCF_create()

    # Read the first frame and initialize the boundary box for the tracker
    ret, frame = capture.read()
    bbox = cv2.selectROI(frame, False)
    tracker.init(frame, bbox)

    # Function to draw a rectangle to define the boundary box
    def drawObjectBox(frame, bbox):
        x = int(bbox[0])
        y = int(bbox[1])
        width = int(bbox[2])
        height = int(bbox[3])
        p1 = (x, y)
        p2 = (x + width, y + height)
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

    #Function to get the center of boundary box
    def getCenter(frame, bbox):
        x = int(bbox[0])
        y = int(bbox[1])
        width = int(bbox[2])
        height = int(bbox[3])
        xCenter = x + (width / 2)
        yCenter = y + (height /2)
        cv2.putText(frame, "Center: " + str(int(xCenter)) + ", " + str(int(yCenter)), (0, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    # Loop to maintain video capture device input and display
    while(capture.isOpened()):
        timer = cv2.getTickCount()
        ret, frame = capture.read()
        
        # ret will return 'True' if video caputre is good and 'False' if video capture is bad
        if not ret:
            break
        
        # Update the tracker every frame
        ret, bbox = tracker.update(frame)
        
        # Print the position of the boundary box
        #print(bbox)

        # Display 'Tracking' if tracking is successful and 'Lost' if tracking is unsuccessful
        if ret:
            drawObjectBox(frame, bbox)
            cv2.putText(frame, "Tracking", (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        else:
            cv2.putText(frame, "Lost", (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # Calculate and display frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        cv2.putText(frame, "FPS : " + str(int(fps)), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        # Display the center of the boundary box
        getCenter(frame, bbox)

        # Change video capture input to grayscale
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Display video capture
        #cv2.imshow('object-tracker', gray)
        cv2.imshow('object-tracker', frame)

        # Press 'esc' key to exit
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Kill all video capture processes and displays
    capture.release()
    cv2.destroyAllWindows()