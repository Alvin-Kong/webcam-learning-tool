import pathlib
from random import randrange

import cv2
import numpy as np
import os
import base64


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


#  Main tracing algorithm, given the template file path, and imageURL data
def trace(template, b64):
    try:
        path = generatePath()
        original = cv2.imread(template)

        pathTrace = os.path.join(path, "Traced")
        pathTraced = os.path.join(pathTrace, "img.png")

        string_to_64 = b64.encode("ascii")
        base = base64.decodebytes(string_to_64)

        tracedImage = open(pathTraced, 'wb')
        tracedImage.write(base)
        tracedImage.close()

        traced = cv2.imread(pathTraced, cv2.IMREAD_UNCHANGED)

        mask = traced[:, :, 3] == 0
        traced[mask] = [255, 255, 255, 255]
        traced = cv2.cvtColor(traced, cv2.COLOR_BGRA2BGR)

        validateImages(original, traced)
        diff = cv2.subtract(original, traced)

        original_count = np.sum(original == 0)
        traced_count = np.sum(traced != 255)
        diff_count = np.sum(diff != 0)
        error_val = 10

        percentage = (1 - (diff_count / original_count)) * 100 + error_val
        if traced_count / original_count < 0.5 or traced_count / original_count > 1.5:
            return qualityBracket(0), 0
        else:
            if percentage >= 100:
                return qualityBracket(100), 100
            else:
                return qualityBracket(percentage), round(percentage)
    except Exception as e:
        print(e)


# Method to return a random png from different categories
def getOriginal(choice):
    path = os.path.join(generatePath(), "Original")
    if choice == "0":
        file = getAny(path)
        return os.path.join(path, file)
    elif choice == "1":
        file = getLetter(path)
        return os.path.join(path, file)
    elif choice == "2":
        file = getNumber(path)
        return os.path.join(path, file)
    elif choice == "3":
        file = getUpperCase(path)
        return os.path.join(path, file)
    elif choice == "4":
        file = getLowerCase(path)
        return os.path.join(path, file)
    elif choice == "5":
        file = getShape(path)
        return os.path.join(path, file)
    else:
        file = getAny(path)
        return os.path.join(path, file)


# Returns any of the png files
def getAny(path):
    images = []
    for file in os.listdir(path):
        if file.endswith(".png"):
            images.append(file)
    return images[randrange(len(images))]


# Returns a png that is a letter
def getLetter(path):
    letters = []
    for file in os.listdir(path):
        if file.endswith(".png") and file.__contains__("uc") or file.__contains__("lc"):
            letters.append(file)
    index = randrange(len(letters))
    return letters[index]


# Returns png that is a digit
def getNumber(path):
    numbers = []
    for file in os.listdir(path):
        if file.endswith(".png") and any(i.isdigit() for i in file):
            numbers.append(file)
    index = randrange(len(numbers))
    return numbers[index]


# Returns png that is an upper case letter
def getUpperCase(path):
    letters = []
    for file in os.listdir(path):
        if file.endswith(".png") and file.__contains__("uc"):
            letters.append(file)
    index = randrange(len(letters))
    return letters[index]


# Returns png that is a lower case letter
def getLowerCase(path):
    letters = []
    for file in os.listdir(path):
        if file.endswith(".png") and file.__contains__("lc"):
            letters.append(file)
    index = randrange(len(letters))
    return letters[index]


# Returns png that is a shape
def getShape(path):
    shapes = []
    for file in os.listdir(path):
        if file.endswith(".png") and len(file) > 8:
            shapes.append(file)
    index = randrange(len(shapes))
    return shapes[index]


# Dynamically generates the file path to the project folder
def generatePath():
    path = pathlib.Path().resolve()
    if not str(path).__contains__("webcam-learning-tool"):
        path = os.path.join(path, "webcam-learning-tool")
    if not str(path).__contains__("Backend"):
        path = os.path.join(path, "Backend")
    if not str(path).__contains__("Tracing"):
        path = os.path.join(path, "Tracing")
    return path
