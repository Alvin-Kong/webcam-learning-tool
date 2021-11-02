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
    validateImages(original, traced)

    diff = cv2.subtract(original, traced)

    original_count = np.count_nonzero(np.all(original != white, 2))
    traced_count = np.count_nonzero(np.all(traced != white, 2))
    diff_count = np.count_nonzero(np.all(diff != black, 2))


#    error_diff = cv2.subtract(error, traced)
#    error_count = np.count_nonzero(np.all(error_diff != black, 2))

    """
    added_image = cv2.addWeighted(error, 0.2, traced, 0.5, 0)
    cv2.imshow("combined", added_image)

    

    
    error_diff = cv2.subtract(error, traced)

    error_count = np.count_nonzero(np.all(error_diff != black, 2))
    print(error_count)

    original_count = np.count_nonzero(np.all(original != white, 2))
    print(original_count)

    original_error = np.count_nonzero(np.all(error != white, 2))
    print(original_error)

    traced_count = np.count_nonzero(np.all(traced != white, 2))
    print(traced_count)

    diff_count = np.count_nonzero(np.all(diff != black, 2))
    """

    error_val = 10
    if traced_count / original_count < 0.5 or traced_count / original_count > 1.5:
        print("INVALID")
    else:
        """
        error_percent = ((traced_count - error_count) / original_count) * 100
        print("ERROR PERCENT: " + str(error_percent))
        print((error_count / original_count + traced_count / original_count) * 100)
        print("CORRECT CALCULATION: " + str(((traced_count - error_count) / (original_count-error_count)) * 100))
        print(((traced_count - error_count) / traced_count) + (traced_count - error_count) / original_count * 100)
        """
        if ((1 - (diff_count / original_count)) * 100 + error_val) >= 100:
            print(100)
        else:
            print(((1 - (diff_count / original_count)) * 100 + error_val))

    # cv2.imshow('ErrorRange', error)
    # cv2.imshow('ErrorDifference', error_diff)
    cv2.imshow('Difference', diff)
    cv2.imshow('original', original)
    cv2.imshow('traced', traced)
    cv2.imshow('tracedOriginal', original_traced)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
