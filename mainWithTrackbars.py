
"""This code is just to pic the values of thresholds and imgMedian value"""

import cv2
import pickle

# Video feed

cap = cv2.VideoCapture("Resources/carPark.mp4")

with open("CarParkPos", 'rb') as f:
    posList = pickle.load(f)

WIDTH, HEIGHT = 105, 45


def empty(a):
    pass


cv2.namedWindow("Vals")
cv2.resizeWindow("Vals", 640, 240)
cv2.createTrackbar("Val1", "Vals", 25, 50, empty)
cv2.createTrackbar("Val2", "Vals", 16, 50, empty)
cv2.createTrackbar("Val3", "Vals", 5, 50, empty)

while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):  # if current frame == total num of frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # setting current frame to 0

    success, img = cap.read()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)

    val1 = cv2.getTrackbarPos("Val1", "Vals")
    val2 = cv2.getTrackbarPos("Val2", "Vals")
    val3 = cv2.getTrackbarPos("Val3", "Vals")
    if val1 % 2 == 0: val1 += 1
    if val3 % 2 == 0: val3 += 1

    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, val1, val2)
    imgMedian=cv2.medianBlur(imgThreshold,val3)

    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + WIDTH, pos[1] + HEIGHT), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.imshow("ImageThres", imgThreshold)
    cv2.imshow("ImageMedian", imgMedian)
    cv2.waitKey(10)
