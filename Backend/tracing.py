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


if __name__ == '__main__':
    original = cv2.imread("tracing/index.png")
    traced = cv2.imread("tracing/indexTraced4.png")
    sought = [0, 0, 0]

    removeOutline(traced)
    validateImages(original, traced)

    diff = cv2.subtract(original, traced)

    diff_count = np.count_nonzero(np.all(diff != sought, 2))
    print(diff_count)

    traced_count = np.count_nonzero(np.all(traced == sought, 2))
    print(traced_count)



    # siftImage()
    cv2.imshow('Difference', diff)
    cv2.imshow('original', original)
    cv2.imshow('traced', traced)

    cv2.waitKey(0)
    cv2.destroyAllWindows()