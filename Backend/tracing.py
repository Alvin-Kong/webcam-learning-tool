from copy import copy
import cv2
import numpy as np

if __name__ == '__main__':
    original = cv2.imread("/Users/reedb/OneDrive/Desktop/index.png")
    traced = cv2.imread("/Users/reedb/OneDrive/Desktop/indexTraced.png")
    tracedOriginal = copy(traced)
    gray = cv2.cvtColor(traced, cv2.COLOR_BGR2GRAY)

    threshold_level = 30
    coords = np.column_stack(np.where(gray < threshold_level))

    print(coords)

    mask = gray < threshold_level

    traced[mask] = (255, 255, 255)

    cv2.imshow('original', original)
    cv2.imshow('traced', traced)
    cv2.imshow('tracedOriginal', tracedOriginal)

    cv2.waitKey(0)





