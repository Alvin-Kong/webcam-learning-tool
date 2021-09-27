from copy import copy
import cv2
import numpy as np

if __name__ == '__main__':
    img = cv2.imread("/Users/reedb/OneDrive/Desktop/index.png")
    orig = copy(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    threshold_level = 10
    coords = np.column_stack(np.where(gray < threshold_level))

    print(coords)

    mask = gray < threshold_level


    img[mask] = (204, 119, 0)

    cv2.imshow('image', img)
    cv2.imshow('original', orig)

    cv2.waitKey(0)
