# For this project I have imported a pre-defined repository containing the
# handDetector class from GitHub named as handTrackingModule.py as htm
# and made changes to it according to my requirements
# Most of the methods and functions used in this code are defined in htm file

import cv2
import numpy as np
import handTrackingModule as htm
import time
import autopy
import pyautogui

widthCam = 380
heightCam = 320
frameReduction = int(widthCam * 0.1)
smoothen = 8
ptime = 0
prev_locx, prev_locy = 0, 0
cur_locx, cur_locy = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3,widthCam )
cap.set(4, heightCam)
detector = htm.handDetector(maxHands=1)
widthScr, heightScr = autopy.screen.size()
# print(widthScr, heightScr)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    # lmList is the list on landmarks on hands extracted by mediapipe
    if len(lmList)!=0:
        # coordinates for index finger, index finger tip =8
        x1, y1 = lmList[8][1:]
        # coordinates for thumb finger, thumb finger tip =4
        x2, y2 =lmList[4][1:]
        # print(x1, y1, x2, y2)
        # coordinates for middle finger, middle finger tip =12
        x4, y4 = lmList[12][1:]

        # to check which fingers are up we call a method of fingersUp from handTrackingModule
        fingers = detector.fingersUp()
        # print(fingers)

        # fingers[1] represent thumb and fingers [2] represent middle finder

        # MOVING ACTION OF MOUSE CURSOR ON THE SCREEN
        # For moving the cursor we use index finger, middle and thumb finger = 0 here
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] ==0:
            cv2.rectangle(img,(frameReduction, frameReduction), (widthCam - frameReduction, heightCam - frameReduction), (255, 255, 255), 1)
            x3 = np.interp(x1, (frameReduction, widthCam - frameReduction), (0, widthScr))
            y3 = np.interp(y1, (frameReduction, heightCam - frameReduction), (0, heightScr))

            # smoothening the values of mouse click
            cur_locx = prev_locx + (x3 - prev_locx)/smoothen
            cur_locy = prev_locy + (y3 - prev_locy) / smoothen

            if abs(cur_locx - prev_locx) < 1.5 and abs(cur_locy - prev_locy) < 1.5:
                continue  # skip update if finger movement is too small

            autopy.mouse.move(widthScr - cur_locx, cur_locy)
            cv2.circle(img, (x1, y1), 9, (255, 0, 255), cv2.FILLED)
            prev_locx, prev_locy = cur_locx, cur_locy

        # CLICKING ACTION OF MOUSE CURSOR ON THE SCREEN
        #For clicking, we bring together both thumb finger and index finger
        if fingers[1] == 1:
            # calculating straight line between the thumb and index finger
            rough_dist = np.hypot(x2 - x1, y2 - y1)
            if rough_dist < 60:
                length, img, lineinfo = detector.findDistance(8, 4, img, draw=True)
                if length < 18:
                    cv2.circle(img, (lineinfo[4], lineinfo[5]), 8, (0, 255, 0), cv2.FILLED)
                    # green circle indicates that the cursor is clicking is
                    # Clicking part
                    autopy.mouse.click()
                    time.sleep(0.1)


        # SCROLLING ACTION
        # When both index and middle fingers are up AND close together
        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineinfo = detector.findDistance(8, 12, img)

            if length <15:
                cv2.circle(img, (lineinfo[4], lineinfo[5]), 8, (0, 255, 0), cv2.FILLED)
                y_diff = y1 - y4
                if y_diff > 8:
                    pyautogui.scroll(-50)  # scroll down
                time.sleep(0.1)


    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime

    # to print frame rate on the screen, uncomment
    # cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)

    cv2.imshow("Video", img)
    key = cv2.waitKey(5)
    # the captured video window closes on pressing the escape key
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()