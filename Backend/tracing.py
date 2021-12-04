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


#  b64
def trace(template, b64):
    try:
        print(template)
        path = generatePath()
        pathOriginal = os.path.join(path, "Original")
        pathOriginal2 = os.path.join(pathOriginal, template)

        original = cv2.imread(template)

        pathTrace = os.path.join(path, "Traced")
        pathTraced = os.path.join(pathTrace, "img.png")

        string_to_64 = b64.encode("ascii")
        base = base64.decodebytes(string_to_64)
        print()
        print(base)
        tracedImage = open(pathTraced, 'wb')
        tracedImage.write(base)
        tracedImage.close()

        traced = cv2.imread(pathTraced, cv2.IMREAD_UNCHANGED)

        print(type(traced))

        # make mask of where the transparent bits are
        mask = traced[:, :, 3] == 0
        # replace areas of transparency with white and not transparent
        traced[mask] = [255, 255, 255, 255]

        # new image without alpha channel...
        traced = cv2.cvtColor(traced, cv2.COLOR_BGRA2BGR)

        # original = cv2.imread("c:/Users/alvin/webcam-learning-tool/Backend/tracing/Original/index.png")
        # traced = cv2.imread("c:/Users/alvin/webcam-learning-tool/Backend/tracing/Traced/indexTraced3.png")
        # original = cv2.imread("tracing/Original/" + originalImage + ".png")
        # traced = cv2.imread("tracing/Traced/" + tracedImage + ".png")
        validateImages(original, traced)

        # removeOutline(traced)
        diff = cv2.subtract(original, traced)

        original_count = np.sum(original == 0)
        traced_count = np.sum(traced != 255)
        diff_count = np.sum(diff != 0)

        print(original_count)
        print(traced_count)
        print(diff_count)
        error_val = 10

        added_image = cv2.addWeighted(original, 0.4, traced, 0.1, 0)
        cv2.imshow("overlay", added_image)

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
        print(e)


# Function that is called from the API that will compare two png files within the directory
# Arguments are two string values for the image name
def trace_old(originalImage, tracedImage):
    try:
        path = generatePath()
        pathOriginal = os.path.join(path, "Original")
        pathOriginal2 = os.path.join(pathOriginal, originalImage)

        original = cv2.imread(pathOriginal2 + ".png")

        pathTrace = os.path.join(path, "Traced")
        pathTraced = os.path.join(pathTrace, tracedImage)

        print(pathTraced)
        print()
        print(b64)
        tracedImage = open(pathTraced + "1.png", 'wb')
        tracedImage.write(b64)
        tracedImage.close()
        print("REACHED")
        newTest = cv2.imread(pathTraced + "1.png", cv2.IMREAD_UNCHANGED)
        print(type(newTest))
        cv2.imshow("TEST", newTest)

        print(pathTrace + "canvas-image.png")
        traced = cv2.imread(pathTrace + "\canvas-image.png", cv2.IMREAD_UNCHANGED)

        print(type(traced))

        # make mask of where the transparent bits are
        mask = traced[:, :, 3] == 0
        # replace areas of transparency with white and not transparent
        traced[mask] = [255, 255, 255, 255]

        # new image without alpha channel...
        traced = cv2.cvtColor(traced, cv2.COLOR_BGRA2BGR)

        # make mask of where the transparent bits are
        mask = newTest[:, :, 3] == 0
        # replace areas of transparency with white and not transparent
        newTest[mask] = [255, 255, 255, 255]

        # new image without alpha channel...
        newTest = cv2.cvtColor(newTest, cv2.COLOR_BGRA2BGR)
        cv2.imshow("TEST", newTest)

        # original = cv2.imread("c:/Users/alvin/webcam-learning-tool/Backend/tracing/Original/index.png")
        # traced = cv2.imread("c:/Users/alvin/webcam-learning-tool/Backend/tracing/Traced/indexTraced3.png")
        # original = cv2.imread("tracing/Original/" + originalImage + ".png")
        # traced = cv2.imread("tracing/Traced/" + tracedImage + ".png")
        validateImages(original, traced)

        # removeOutline(traced)
        diff = cv2.subtract(original, traced)

        original_count = np.sum(original == 0)
        traced_count = np.sum(traced != 255)
        diff_count = np.sum(diff != 0)

        print(original_count)
        print(traced_count)
        print(diff_count)
        error_val = 0

        added_image = cv2.addWeighted(original, 0.4, traced, 0.1, 0)
        cv2.imshow("overlay", added_image)

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
    print(letters[index])
    return letters[index]


# Returns png that is a digit
def getNumber(path):
    numbers = []
    for file in os.listdir(path):
        if file.endswith(".png") and any(i.isdigit() for i in file):
            numbers.append(file)
    index = randrange(len(numbers))
    print(numbers[index])
    return numbers[index]


# Returns png that is an upper case letter
def getUpperCase(path):
    letters = []
    for file in os.listdir(path):
        if file.endswith(".png") and file.__contains__("uc"):
            letters.append(file)
    index = randrange(len(letters))
    print(letters[index])
    return letters[index]


# Returns png that is a lower case letter
def getLowerCase(path):
    letters = []
    for file in os.listdir(path):
        if file.endswith(".png") and file.__contains__("lc"):
            letters.append(file)
    index = randrange(len(letters))
    print(letters[index])
    return letters[index]


# Returns png that is a shape
def getShape(path):
    shapes = []
    for file in os.listdir(path):
        if file.endswith(".png") and len(file) > 8:
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
    # b64 = "OnrsAABAZwNWQW5HjxkAABjIdisAAKCbDqsgtlsBAADf2ymE2G4FAAA8rWEIsd0KAAB4XUZcWfEAAAC6KlgNucuIL0fXCwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADCL"
    #b64 = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII="
    b64 = "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"
    string_to_64 = b64.encode("ascii")
    base = base64.decodebytes(string_to_64)
    # print(trace("triangle", "img", base))
    print(trace("triangle", base))

    # for i in range(10):
    # print(getOriginal(3))
    # path = getOriginal(1)
    # print(path)
    # imageTest = cv2.imread(path)
    # cv2.imshow("test", imageTest)

    #img = cv2.imread("/Users/reedb/PycharmProjects/webcam-learning-tool/Backend/Tracing/Original/r_uc.png")
    #cv2.imshow("assdasd", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
