import cv2
import numpy as np
from random import randint

size = 800
img = np.zeros((size, size, 3), np.uint8)
img.fill(255)

points = set()
taken = set()

while len(points) < 4:
    x, y = randint(0, size / 2) + size / 4, randint(0, size / 2) + size / 4
    if (x, y) not in taken:
        points.add((x, y))
        for i in range(-1, 2):
            for j in range(-1, 2):
                taken.add((x + i, y + j))

for (x, y) in points:
    img[x, y] = 0

cv2.imwrite("blank.png", img)
