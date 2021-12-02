import pathlib
from random import randrange

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
# Arguments are two string values for the image name
def trace(originalImage, tracedImage):
    try:
        path = generatePath()
        pathOriginal = os.path.join(path, "Original")
        pathOriginal = os.path.join(pathOriginal, originalImage)

        original = cv2.imread(pathOriginal + ".png")

        pathTrace = os.path.join(path, "Traced")
        pathTraced = os.path.join(pathTrace, tracedImage)
        traced = cv2.imread(pathTraced + ".png")

        #pathWhite = os.path.join(pathTrace, "canvas-image.png")
        #white = cv2.imread(pathWhite)

        #white = cv2.add(white,traced)
        #cv2.imshow("White", white)

        # original = cv2.imread("c:/Users/alvin/webcam-learning-tool/Backend/tracing/Original/index.png")
        # traced = cv2.imread("c:/Users/alvin/webcam-learning-tool/Backend/tracing/Traced/indexTraced3.png")
        # original = cv2.imread("tracing/Original/" + originalImage + ".png")
        # traced = cv2.imread("tracing/Traced/" + tracedImage + ".png")
        validateImages(original, traced)
        cv2.imshow("Original Trace", traced)
        #removeOutline(traced)
        diff = cv2.subtract(original, traced)

        original_count = np.sum(original == 0)
        traced_count = np.sum(traced != 255)
        diff_count = np.sum(diff != 0)

        print(original_count)
        print(traced_count)
        print(diff_count)
        error_val = 10

        cv2.imshow("trace", traced)
        cv2.imshow("difference", diff)
        cv2.imshow("original", original)


        percentage = (1 - (diff_count / original_count)) * 100 + error_val
        if traced_count / original_count < 0.5 or traced_count / original_count > 1.5:
            return qualityBracket(0), 0
        else:
            if percentage >= 100:
                return qualityBracket(100), 100
            else:
                return qualityBracket(percentage), round(percentage)
    except Exception as e:
        print("Unable to open file")
        print(e)

# Method to return a random png from different categories
def getOriginal(choice):
    path = os.path.join(generatePath(), "Original")
    if choice == 0:
        file = getAny(path)
        return os.path.join(path, file)
    elif choice == 1:
        file = getLetter(path)
        return os.path.join(path, file)
    elif choice == 2:
        file = getNumber(path)
        return os.path.join(path, file)
    elif choice == 3:
        file = getUpperCase(path)
        return os.path.join(path, file)
    elif choice == 4:
        file = getLowerCase(path)
        return os.path.join(path, file)
    elif choice == 5:
        file = getShape(path)
        return os.path.join(path, file)
    else:
        file = getAny(path)
        return os.path.join(path, file)

# Returns any of the png files
def getAny(path):
    files = os.listdir(path)
    return files[randrange(len(files))]

# Returns a png that is a letter
def getLetter(path):
    letters = []
    for file in os.listdir(path):
        if file.__contains__("uc") or file.__contains__("lc"):
            letters.append(file)
    index = randrange(len(letters))
    print(letters[index])
    return letters[index]

# Returns png that is a digit
def getNumber(path):
    numbers = []
    for file in os.listdir(path):
        if any(i.isdigit() for i in file):
            numbers.append(file)
    index = randrange(len(numbers))
    print(numbers[index])
    return numbers[index]

# Returns png that is an upper case letter
def getUpperCase(path):
    letters = []
    for file in os.listdir(path):
        if file.__contains__("uc"):
            letters.append(file)
    index = randrange(len(letters))
    print(letters[index])
    return letters[index]

# Returns png that is a lower case letter
def getLowerCase(path):
    letters = []
    for file in os.listdir(path):
        if file.__contains__("lc"):
            letters.append(file)
    index = randrange(len(letters))
    print(letters[index])
    return letters[index]

# Returns png that is a shape
def getShape(path):
    shapes = []
    for file in os.listdir(path):
        if len(file) > 8:
            shapes.append(file)
    index = randrange(len(shapes))
    print(shapes[index])
    return shapes[index]

def generatePath():
    path = pathlib.Path().resolve()
    if not str(path).__contains__("webcam-learning-tool"):
        path = os.path.join(path, "webcam-learning-tool")
    if not str(path).__contains__("Backend"):
        path = os.path.join(path, "Backend")
    if not str(path).__contains__("Tracing"):
        path = os.path.join(path, "Tracing")
    return path


if __name__ == '__main__':
    # zero = cv2.imread("c:/Users/alvin/webcam-learning-tool/Backend/Tracing/Original/0.png")
    # cv2.imshow("0", zero)
    # print(trace("a_uc", "canvas-image"))
    print(trace("index", "indexTraced3"))
    #path = getOriginal(1)
    #print(path)
    #imageTest = cv2.imread(path)
    #cv2.imshow("test", imageTest)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
