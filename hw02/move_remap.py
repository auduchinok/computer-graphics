# Eugene Auduchinok, 2015

from __future__ import division
import cv2
import numpy as np
import sys

try:
    img_path = sys.argv[1]
    img = cv2.imread(img_path)
    rows, cols = img.shape[:2]
except:
    print "error: no image path given"
    sys.exit()

try:
    x0, y0, x1, y1 = map(int, sys.argv[2:6])   # original window
    x2, y2, x3, y3 = map(int, sys.argv[6:10])  # new window
except:
    print "error: not enough coordinates given"
    sys.exit()

scale_x = (x3 - x2) / (x1 - x0)
scale_y = (y3 - y2) / (y1 - y0)

map_x = np.zeros((rows, cols), np.float32)
map_y = np.zeros((rows, cols), np.float32)

for y in range(rows):
    for x in range(cols):
        map_x.itemset((y, x), (x - x2) * scale_x + x0)
        map_y.itemset((y, x), (y - y2) * scale_y + y0)

img = cv2.remap(img, map_x, map_y, cv2.INTER_CUBIC)

cv2.imshow('transformed', img)
cv2.waitKey(0)
