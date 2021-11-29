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
        path = pathlib.Path().resolve()
        original = cv2.imread(str(path) + "/tracing/Original/" + originalImage + ".png")
        traced = cv2.imread(str(path) + "/tracing/Traced/" + tracedImage + ".png")

        # original = cv2.imread("c:/Users/alvin/webcam-learning-tool/Backend/tracing/Original/index.png")
        # traced = cv2.imread("c:/Users/alvin/webcam-learning-tool/Backend/tracing/Traced/indexTraced3.png")
        # original = cv2.imread("tracing/Original/" + originalImage + ".png")
        # traced = cv2.imread("tracing/Traced/" + tracedImage + ".png")
        cv2.imshow("Original", original)
        validateImages(original, traced)
        cv2.imshow("Original Trace", traced)
        removeOutline(traced)
        diff = cv2.subtract(original, traced)

        original_count = np.count_nonzero(np.all(original == 0, 2))
        traced_count = np.count_nonzero(np.all(traced != 255, 2))
        diff_count = np.count_nonzero(np.all(diff != 0, 2))

        error_val = 10

        cv2.imshow("trace", traced)
        cv2.imshow("difference", diff)
        cv2.imshow("original", original)

        percentage = (1 - (diff_count / original_count)) * 100
        if traced_count / original_count < 0.5 or traced_count / original_count > 1.5:
            return qualityBracket(0), 0
        else:
            if ((1 - (diff_count / original_count)) * 100 + error_val) >= 100:
                return qualityBracket(100), 100
            else:
                return qualityBracket(percentage + error_val), round(percentage + error_val)
    except Exception as e:
        print("Unable to open file")
        print(e)

# Method to return a random png from different categories
def getOriginal(choice):
    path = str(pathlib.Path().resolve()) + "/Tracing/Original/"
    print(path)
    if choice == 0:
        path += getAny()
        return path
    elif choice == 1:
        path += getLetter()
        return path
    elif choice == 2:
        path += getNumber()
        return path
    elif choice == 3:
        path += getUpperCase()
        return path
    elif choice == 4:
        path += getLowerCase()
        return path
    elif choice == 5:
        path += getShape()
        return path
    else:
        path += getAny()
        return path

# Returns any of the png files
def getAny():
    files = os.listdir("tracing/Original")
    return files[randrange(len(files))]

# Returns a png that is a letter
def getLetter():
    letters = []
    for file in os.listdir("tracing/Original"):
        if file.__contains__("uc") or file.__contains__("lc"):
            letters.append(file)
    index = randrange(len(letters))
    print(letters[index])
    return letters[index]

# Returns png that is a digit
def getNumber():
    numbers = []
    for file in os.listdir("tracing/Original"):
        if any(i.isdigit() for i in file):
            numbers.append(file)
    index = randrange(len(numbers))
    print(numbers[index])
    return numbers[index]

# Returns png that is an upper case letter
def getUpperCase():
    letters = []
    for file in os.listdir("tracing/Original"):
        if file.__contains__("uc"):
            letters.append(file)
    index = randrange(len(letters))
    print(letters[index])
    return letters[index]

# Returns png that is a lower case letter
def getLowerCase():
    letters = []
    for file in os.listdir("tracing/Original"):
        if file.__contains__("lc"):
            letters.append(file)
    index = randrange(len(letters))
    print(letters[index])
    return letters[index]

# Returns png that is a shape
def getShape():
    shapes = []
    for file in os.listdir("tracing/Original"):
        if len(file) > 8:
            shapes.append(file)
    index = randrange(len(shapes))
    print(shapes[index])
    return shapes[index]


if __name__ == '__main__':
    # zero = cv2.imread("c:/Users/alvin/webcam-learning-tool/Backend/Tracing/Original/0.png")
    # cv2.imshow("0", zero)
    #print(trace("index", "indexTraced3"))
    path = getOriginal(2)
    print(path)
    imageTest = cv2.imread(path)
    cv2.imshow("test", imageTest)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
