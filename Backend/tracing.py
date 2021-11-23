import pathlib

import cv2
import numpy as np
import os


# Function to remove the black outline from the traced over image
def removeOutline(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold_level = 50
    mask = gray < threshold_level
    image[np.where(mask)] = 255


# Function to clean up PNG files within the directory
def reformatImage():
    for file in os.listdir("tracing"):
        if file.endswith(".png"):
            image = cv2.imread("tracing/" + file)
            image[np.where(image != 255)] = 0
            cv2.imshow(file, image)
            cv2.imwrite("tracing/" + file, image)


# Ensures that the two images are the same size, for better comparison
def validateImages(originalImage, tracedImage):
    if originalImage.shape != tracedImage.shape:
        return False


# Function that determines the overall quality of trace, according to percentage brackets
def qualityBracket(percentage):
    if 0 <= percentage <= 50:
        return 0
    elif 50 < percentage < 70:
        return 1
    else:
        return 2

# Function that is called from the API that will compare two png files within the directory
def trace(originalImage, tracedImage):
    try:
        path = pathlib.Path().resolve()
        original = cv2.imread(str(path) + "/tracing/Original/" + originalImage + ".png")
        traced = cv2.imread(str(path) + "/tracing/Traced/" + tracedImage + ".png")

        # original = cv2.imread("c:/Users/alvin/webcam-learning-tool/Backend/tracing/Original/index.png")
        # traced = cv2.imread("c:/Users/alvin/webcam-learning-tool/Backend/tracing/Traced/indexTraced3.png")
        #original = cv2.imread("tracing/Original/" + originalImage + ".png")
        #traced = cv2.imread("tracing/Traced/" + tracedImage + ".png")
        validateImages(original, traced)
        cv2.imshow("Original Trace", traced)
        removeOutline(traced)
        diff = cv2.subtract(original, traced)

        original_count = np.count_nonzero(np.all(original == 0, 2))
        traced_count = np.count_nonzero(np.all(traced != 255, 2))
        diff_count = np.count_nonzero(np.all(diff != 0, 2))

        error_val = 10

        cv2.imshow("trace", traced)
        cv2.imshow("original", original)

        percentage = (1 - (diff_count / original_count)) * 100
        if traced_count / original_count < 0.5 or traced_count / original_count > 1.5:
            print("HELLO")
        else:
            if ((1 - (diff_count / original_count)) * 100 + error_val) >= 100:
                return qualityBracket(100), 100
            else:
                return qualityBracket(percentage + error_val), percentage + error_val
    except:
        print("FALSE")


if __name__ == '__main__':
    #zero = cv2.imread("c:/Users/alvin/webcam-learning-tool/Backend/Tracing/Original/0.png")
    #cv2.imshow("0", zero)
    print(trace("index", "indexTraced3"))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

