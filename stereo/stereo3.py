import cv2
import numpy as np
from find_obj import filter_matches


def open_img(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    size = (img.shape[1] / 4, img.shape[0] / 4)
    img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
    return img


img1 = open_img('1.jpg')
img2 = open_img('2.jpg')

pts1 = np.float32([[511, 426], [513, 509], [350, 514], [350, 429]])
pts2 = np.float32([[356, 420], [351, 509], [186, 494], [192, 409]])
pts = np.float32([[150, 0, 0], [150, 80, 0], [0, 80, 0], [0, 0, 0]])

# pts1 = np.float32([[448, 397], [551, 393], [549, 457], [447, 460]])
# pts2 = np.float32([[408, 386], [512, 386], [510, 448], [408, 448]])
# pts = np.float32([[15, -60, 2], [15, 60, 2], [-15, 60, 2], [-15, -60, 2]])

camera_m = np.float32([[2.11380990e+03, 0.00000000e+00, 1.59992792e+03],
                       [0.00000000e+00, 2.12181431e+03, 1.14094052e+03],
                       [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

dist_coeffs = np.float32([2.95659820e-02, -5.23079648e-01, -1.25224404e-03, -5.96602108e-03, 1.91077620e+00])

# _, r1, t1 = cv2.solvePnP(pts, pts1, camera_m, dist_coeffs)
# _, r2, t2 = cv2.solvePnP(pts, pts2, camera_m, dist_coeffs)

imageSize = (img1.shape[1] * 4, img1.shape[0] * 4)
r, t = cv2.stereoCalibrate([pts], [pts1], [pts2], imageSize)[-4:-2]
pm1, pm2 = cv2.stereoRectify(camera_m, dist_coeffs, camera_m, dist_coeffs, imageSize, r, t)[2:4]

sift = cv2.SIFT()
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

bf = cv2.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)

# good = []
# for m, n in matches:
#     if m.distance < 0.75 * n.distance:
#         good.append([m])
# img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, flags=2)

kp_pairs = filter_matches(kp1, kp2, matches)[2]

x1, y1, x2, y2 = [], [], [], []

for pt1, pt2 in kp_pairs:
    x1.append(pt1.pt[0])
    y1.append(pt1.pt[1])
    x2.append(pt2.pt[0])
    y2.append(pt2.pt[1])

pts3 = np.float32([x1, y1])
pts4 = np.float32([x2, y2])

# explore_match('find_obj', img1, img2, kp_pairs)  # cv2 shows image

# for m in good:
#     color = tuple([sp.random.randint(0, 255) for _ in xrange(3)])
#     cv2.line(weighted, (int(kp1[m.queryIdx].pt[0]), int(kp1[m.queryIdx].pt[1])),
#              (int(kp2[m.trainIdx].pt[0]), int(kp2[m.trainIdx].pt[1])), color)

triangulated = cv2.triangulatePoints(pm1, pm2, pts3, pts4)

h = []
for i in range(len(triangulated[0])):
    h.append([triangulated[0][i], triangulated[1][i], triangulated[2][i], triangulated[3][i]])

# points = cv2.convertPointsFromHomogeneous(np.array(h))

with file('out.txt', 'w') as out:
    for point in h:
        # pt = point[0]
        out.write("{0};{1};{2}\n".format(point[0], point[1], point[2]))

# RMS: 0.540091619994
# camera matrix:
# [[  2.11380990e+03   0.00000000e+00   1.59992792e+03]
#  [  0.00000000e+00   2.12181431e+03   1.14094052e+03]
#  [  0.00000000e+00   0.00000000e+00   1.00000000e+00]]
# distortion coefficients:  [  2.95659820e-02  -5.23079648e-01  -1.25224404e-03  -5.96602108e-03
#  1.91077620e+00]
