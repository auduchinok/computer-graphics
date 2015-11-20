import cv2
import numpy as np
import sys

try:
    img_path = sys.argv[1]
    img = cv2.imread(img_path)
    rows, cols, _ = img.shape
except:
    print "error: no image path given"
    sys.exit()

try:
    x0, y0, x1, y1 = map(int, sys.argv[2:6])   # original window
    x2, y2, x3, y3 = map(int, sys.argv[6:10])  # new window
except:
    print "error: not enough coordinates given"
    sys.exit()

orig_width  = float(x1 - x0)
orig_height = float(y1 - y0)

transform_matrix = np.float32([
    [(x3 - x2) / orig_width, 0,  (x1 * x2 - x0 * x3) / orig_width],
    [0, (y3 - y2) / orig_height, (y1 * y2 - y0 * y3) / orig_height]])

transformed = cv2.warpAffine(img, transform_matrix, (cols, rows))
cv2.imshow('transformed', transformed)
cv2.waitKey(0)