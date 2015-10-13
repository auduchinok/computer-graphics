# Eugene Auduchinok, 2015

import cv2

# use numpy for faster array access
# via .item and .itemset methods
# import numpy as np
# didn't get it to work

# load image as array of tuple-based pixels
# second param is for grayscale mode (optional)
img = cv2.imread('low-contrast.png', 0)
rows, cols = img.shape

# for BGR-color mode
# row, cols, channels = img.shape

# simple access approach (BGR-color mode)
# img[10, 10] = [100, 150, 200]
# print img[10, 10]

# better access approach (BGR-color mode)
# item(row, column, channel)
# img.itemset((10,10,0), 123)
# print img.item(10,10,0)

# task specific
min, max, _, _ = cv2.minMaxLoc(img)
diff = max - min
multiplier = 255 / diff

for i in range(rows):
    for j in range(cols):
        img.itemset((i, j), (img.item(i, j) - min) * multiplier)

# show window with title
cv2.imshow('increase-contrast', img)
cv2.waitKey(0)

# Do I need to use this as in tutorials?
# Windows are closed automatically on OSX + IntelliJ
# cv2.destroyAllWindows()


