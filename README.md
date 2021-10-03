# webcam-learning-tool
A learning tool that allows the user to utilize their webcams to draw and annotate on an open canvas.

Install Python (either 3.x or 2.7.x)

Setting Up OpenCV
1. Install OpenCV, Numpy, Matplotlib
   pip install opencv-contrib-python
   (Installing opencv-contrib-python should install Numpy and Matplotlib along with OpenCV)
   (If Numpy and Matplotlib does not install, you will need to install it separately)

Runtime
1. After running the program, the application will take a single frame from your webcam. From the provided frame, click and drag a square around the object you want to track, this will become the boundary box.
2. Press 'Enter' after the boundary box is created. The application will be live, providing live feed from the webcam with the application tracking the object. The FPS (frames per second), tracking status, and mode will be shown in the top left corner of the window. If the tracked object moves out of the camera frame, the "Tracking" status will change to "Lost". The "Stoppped" status indicates that the system is not drawing.
3. Press 'Spacebar' to start "drawing". When drawing mode is enabled, the position of the center of the boundary box will be displayed on the top left corner.
