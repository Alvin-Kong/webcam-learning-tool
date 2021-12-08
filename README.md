# webcam-learning-tool
A learning tool that allows the user to utilize their webcams to draw and annotate on an open canvas.

Install Python (either 3.x or 2.7.x)

Setting Up API
1. Install OpenCV, Numpy, Matplotlib

   "pip install opencv-contrib-python"
   
   (Installing opencv-contrib-python should install Numpy and Matplotlib along with OpenCV)
   
   (If Numpy and Matplotlib does not install, you will need to install it separately)
   
2. Install Flask and Flask_CORS

   "pip install flask requests flask_cors"

Runtime
1. After running "api.py" located in the Backend folder, the application will take a single frame from your webcam. From the provided frame, click and drag a square around the object you want to track, this will become the boundary box.
2. Press 'Enter' after the boundary box is created. The application will be live, providing live feed from the webcam with the application tracking the object. If the tracked object moves out of the camera frame, the "Tracking" status will change to "Lost". The "Stoppped" status indicates that the system is not drawing.
   - If the tracked object is lost, then the application will need to be closed and started up again.
3. Open "HomePage.html" located in the Frontend folder to load the main page of the application.
4. Press 'M' to activate the webcam drawing cursor, press 'Enter' to start webcam drawing, and press 'Spacebar' to stop webcam drawing.
