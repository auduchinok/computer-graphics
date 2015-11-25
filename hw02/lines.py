# Eugene Auduchinok, 2015

from __future__ import division
import cv2
import itertools

img = cv2.imread('blank.png', 0)
rows, cols = img.shape

black_points = []
lines = []

for i in range(rows):
    for j in range(cols):
        if img.item(i, j) == 0:
            black_points.append((i, j))

img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

for p1, p2 in itertools.combinations(black_points, 2):
    lines.append((p1[1] - p2[1], p2[0] - p1[0], p1[0] * p2[1] - p2[0] * p1[1]))

for l1, l2 in itertools.combinations(lines, 2):
    c = l1[0] * l2[1] - l1[1] * l2[0]
    x = (l1[1] * l2[2] - l1[2] * l2[1]) / c
    y = (l1[2] * l2[0] - l1[0] * l2[2]) / c
    img[int(x), int(y)] = [0, 0, 255]

cv2.imshow('points', img)
cv2.waitKey(0)
