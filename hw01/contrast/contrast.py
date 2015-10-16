# Eugene Auduchinok, 2015

import cv2
import numpy as np


img = cv2.imread('low-contrast.png', 0)
rows, cols = img.shape

min, max, _, _ = cv2.minMaxLoc(img)
diff = max - min
multiplier = 255 / diff

for i in range(rows):
    for j in range(cols):
        img.itemset((i, j), (img.item(i, j) - min) * multiplier)

cv2.imshow('increase-contrast', img)
cv2.waitKey(0)

# Do I need to use this method?
# Windows are closed automatically on OSX + IntelliJ
# cv2.destroyAllWindows()