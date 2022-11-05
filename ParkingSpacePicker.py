import cv2
import pickle

# img = cv2.imread('Resources/carParkImg.png')

# width and height of one parking slot
WIDTH, HEIGHT = 105, 45

try:
    with open("CarParkPos", 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []


def mouse_click(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    elif events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + WIDTH and y1 < y < y1 + HEIGHT:
                posList.pop(i)
    with open("CarParkPos", "wb") as f:
        pickle.dump(posList, f)


while True:
    img = cv2.imread('Resources/carParkImg.png')
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + WIDTH, pos[1] + HEIGHT), (255, 0, 255), 2)
    cv2.imshow('Image', img)
    # to detect mouse click
    cv2.setMouseCallback("Image", mouse_click)
    q = cv2.waitKey(1)
    if q == ord("q"):
        break
