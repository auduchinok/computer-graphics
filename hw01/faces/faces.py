import numpy as np
import cv2
import sys

if len(sys.argv) < 2:
    print "faces: no image provided\n" + \
          "usage: faces.py <filename>"
    exit()

img = cv2.imread(sys.argv[1])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

face_cascade = cv2.CascadeClassifier('faces.xml')
eye_cascade = cv2.CascadeClassifier('eyes.xml')

faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    face = img[y:y + h, x:x + w]
    face_gray = gray[y:y + h, x:x + w]

    eyes = eye_cascade.detectMultiScale(face_gray)
    for (x, y, w, h) in eyes:
        cv2.rectangle(face, (x, y), (x + w, y + h), (0, 255, 0), 2)

if len(faces) > 0:
    cv2.imshow('faces', img)
    cv2.waitKey(0)
else:
    print "No face found"
