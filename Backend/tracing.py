from copy import copy
import cv2
import numpy as np


def removeOutline():
    gray = cv2.cvtColor(traced, cv2.COLOR_BGR2GRAY)
    threshold_level = 30
    mask = gray < threshold_level
    traced[mask] = (255, 255, 255)


def validateImages(original, tracedImage):
    if original.shape == tracedImage.shape:
        print("same size")


def siftImage():
    sift = cv2.SIFT_create()

    kp_1, desc_1 = sift.detectAndCompute(original, None)
    kp_2, desc_2 = sift.detectAndCompute(traced, None)

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
    better = cv2.drawMatches(original, kp_1, traced, kp_2, points, None)
    print(len(points))

    if len(kp_1) <= len(kp_2):
        key_points = len(kp_1)
    else:
        key_points = len(kp_2)

    print("How good of a match: " + str(len(points) / key_points * 100))

    cv2.imshow("better", better)


if __name__ == '__main__':
    original = cv2.imread("tracing/index.png")
    traced = cv2.imread("tracing/duplicate.png")

    if original.shape == traced.shape:
        diff = cv2.subtract(original, traced)
        cv2.imshow('Difference', diff)
        print(len(diff))

    validateImages(original, traced)

    siftImage()

    removeOutline()

    #siftImage()

    cv2.imshow('original', original)
    cv2.imshow('traced', traced)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
