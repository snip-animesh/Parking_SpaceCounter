import cv2
import pickle
import cvzone
import numpy as np

# Video feed
cap = cv2.VideoCapture("Resources/carPark.mp4")

with open("CarParkPos", 'rb') as f:
    posList = pickle.load(f)

WIDTH, HEIGHT = 105, 45
kernel = np.ones((3, 3), np.uint8)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
CAR_PIXEL = 800
bgWidth , bgHeight = 1280 , 720


def check_parking_space(imgPro,imgBG):
    spaceCounter = 0

    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y + HEIGHT, x:x + WIDTH]
        # cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)

        if count < CAR_PIXEL:
            color = GREEN
            thickness = 5
            spaceCounter += 1
        else:
            color = RED
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + WIDTH, pos[1] + HEIGHT), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + HEIGHT - 5), scale=1,
                           thickness=2, offset=0)

    cvzone.putTextRect(img, f'Free: {str(spaceCounter)}/{len(posList)}', (100, 50), scale=2,
                       thickness=3, offset=10, colorR=RED)
    # Putting counted value on background image
    cv2.putText(imgBG, str(spaceCounter), (1101, 235), cv2.FONT_ITALIC,1,RED,thickness=3)
    cv2.putText(imgBG, str(len(posList)), (1101, 175), cv2.FONT_ITALIC,1,GREEN,thickness=3)


while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):  # if current frame == total num of frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # setting current frame to 0

    success, img = cap.read()


    # importing background Image
    imgBackground = cv2.imread('Resources/background.png')
    # resize the image
    imgBackground = cv2.resize(imgBackground,(bgWidth,bgHeight),interpolation=cv2.INTER_LINEAR)

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)

    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    check_parking_space(imgDilate,imgBackground)

    # Placing CCTV footage to background image
    imgResize = cv2.resize(img, (695,341)) # width & height
    imgBackground[178:519,47:742] = imgResize # height & width

    cv2.imshow("User Interface", imgBackground)
    # cv2.imshow("ImageDilate", imgDilate)
    K = cv2.waitKey(10)
    if K == ord('q'):
        break

