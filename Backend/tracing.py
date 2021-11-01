from copy import copy
import cv2
import numpy as np


def removeOutline(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold_level = 30
    mask = gray < threshold_level
    image[mask] = (255, 255, 255)


def validateImages(originalImage, tracedImage):
    if originalImage.shape == tracedImage.shape:
        print("same size")


"""
def siftImage(originalImage, testImage):
    sift = cv2.SIFT_create()

    kp_1, desc_1 = sift.detectAndCompute(originalImage, None)
    kp_2, desc_2 = sift.detectAndCompute(testImage, None)

    print(len(kp_1))
    print(len(kp_2))
    print()

    index_parameters = dict(algorithm=0, trees=5)
    search_parameters = dict()
    flann = cv2.FlannBasedMatcher(index_parameters, search_parameters)

    matches = flann.knnMatch(desc_1, desc_2, k=2)
    points = []
    for r, c in matches:
        if r.distance < 0.60 * c.distance:
            points.append(r)
    better = cv2.drawMatches(originalImage, kp_1, testImage, kp_2, points, None)
    print(len(points))

    if len(kp_1) <= len(kp_2):
        key_points = len(kp_1)
    else:
        key_points = len(kp_2)

    print("How good of a match: " + str(len(points) / key_points * 100))

    cv2.imshow("better", better)
"""

if __name__ == '__main__':
    original = cv2.imread("tracing/index.png")
    traced = cv2.imread("tracing/indexTraced5.png")
    original_traced = copy(traced)
    error = cv2.imread("tracing/range.png")

    black = [0, 0, 0]
    white = [255, 255, 255]

    removeOutline(traced)

    added_image = cv2.addWeighted(error, 0.4, traced, 0.1, 0)
    cv2.imwrite('combined.png', added_image)

    cv2.imshow("combined", added_image)

    validateImages(original, traced)

    diff = cv2.subtract(original, traced)
    error_diff = cv2.subtract(error, traced)

    error_count = np.count_nonzero(np.all(error_diff != black, 2))
    print(error_count)

    traced_count = np.count_nonzero(np.all(traced != white, 2))
    print(traced_count)

    print(((traced_count - error_count) / traced_count) * 100)

    cv2.imshow('ErrorRange', error)
    cv2.imshow('ErrorDifference', error_diff)
    cv2.imshow('Difference', diff)
    cv2.imshow('original', original)
    cv2.imshow('traced', traced)
    cv2.imshow('tracedOriginal', original_traced)


    cv2.waitKey(0)
    cv2.destroyAllWindows()
