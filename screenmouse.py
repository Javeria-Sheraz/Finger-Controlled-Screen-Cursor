import cv2
import numpy as np
import mediapipe as mp
import math
import time
import autopy
import pyautogui

##########FUNCTIONS#########
def findPosition(image, results, handNo = 0, DRAW = True):
    lmList = []
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        h, w, c = image.shape
        for id, lm in enumerate(myHand.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
            # UNCOMMENT THSI IF YOU WANT CIRCLES DRAWN ON LANDMARKS OF YOUR HANDS
            # if DRAW:
            #     cv2.circle(image, (cx, cy), 4, (255, 0, 0), cv2.FILLED)
    return lmList

def fingersUp(lmlist):
    fingers = []
    tipsIdx = [4, 8, 12, 16, 20]
    if len(lmlist) == 0:
        return []
    #CONDITION TO DETECT THUMB
    #As the thumb moves sideways on the screen we compare its index of tips (x coordinate [1]) with the previous tips index
    if lmlist[tipsIdx[0]][1] < lmlist[tipsIdx[0] - 1][1]:
        fingers.append(1)
    else:
        fingers.append(0)
    # Working: Left a finger(tip) is, the smaller its x-number becomes
    # CONDITION TO DETECT OTHER FINGERS
    for id in range(1, 5):
        if lmlist[tipsIdx[id]][2] < lmlist[tipsIdx[id] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)
            # Higher a finger is, the smaller its y-number becomes. This checks the tip and two indexes below it
    return fingers

def findDistance(lmlist, p1, p2, image, draw=True):
        x1, y1 = lmlist[p1][1:]
        x2, y2 = lmlist[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        if draw:
            # drawing lines to connecting hand landmarks
            cv2.line(image, (x1, y1), (x2, y2), (230, 230, 230), 2)
            # drawing circles to map the landmarks on hand
            cv2.circle(image, (x1, y1), 4, (255, 0, 0), cv2.FILLED)
            cv2.circle(image, (x2, y2), 4, (255, 0, 0), cv2.FILLED)
            cv2.circle(image, (cx, cy), 4, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
        return length, image, [x1, y1, x2, y2, cx, cy]

############################

widthCam = 360
heightCam = 400
frameReduction = int(widthCam * 0.1)
smoothen = 7
prev_locx, prev_locy = 0, 0
cur_locx, cur_locy = 0, 0

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,widthCam )
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, heightCam)
widthScr, heightScr = autopy.screen.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()


while True:
    success, img = cam.read()
    img = cv2.flip(img, 1)
    if success:
        convertedImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results= hands.process(convertedImg)

    # lmList is the list of landmarks on hands extracted by mediapipe
    lmList = findPosition(img, results)
    if len(lmList) != 0:
        # coordinates for thumb finger, thumb finger tip =8
        x1 = lmList[4][1]
        y1 = lmList[4][2]
        # coordinates for index finger, index finger tip =4
        x2 = lmList[8][1]
        y2 = lmList[8][2]
        # coordinates for middle finger, middle fingertip =12
        x3 = lmList[12][1]
        y3 = lmList[12][2]

        fingers = fingersUp(lmList)

        # CURSOR MOVING ACTION OF MOUSE ON THE SCREEN
        if fingers[1] == 1 and fingers[2] == 0:
            cv2.rectangle(img, (frameReduction, frameReduction),
                          (widthCam - frameReduction, heightCam - frameReduction), (255, 255, 255), 1)
            x4 = np.interp(x2, (frameReduction, widthCam - frameReduction), (0, widthScr))
            y4 = np.interp(y2, (frameReduction, heightCam - frameReduction), (0, heightScr))
            # smoothening the values of mouse click
            cur_locx = prev_locx + (x4 - prev_locx) / smoothen
            cur_locy = prev_locy + (y4 - prev_locy) / smoothen

        if abs(cur_locx - prev_locx) > 1.5 and abs(cur_locy - prev_locy) > 1.5:
            autopy.mouse.move(cur_locx, cur_locy)
            cv2.circle(img, (x2, y2), 7, (28, 28, 28), cv2.FILLED)
            cv2.putText(img, "Moving cursor", (img.shape[1] - 300, img.shape[0] - 13), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255, 255, 255), 6)
            cv2.putText(img, "Moving cursor", (img.shape[1] - 300, img.shape[0] - 13), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 0, 0), 2)
        prev_locx, prev_locy = cur_locx, cur_locy

        # CLICKING ACTION OF MOUSE CURSOR ON THE SCREEN
        # For clicking, we bring together both thumb finger and index finger
        if fingers[1] == 1:
            rough_dist = np.hypot(x1 - x2, y1 - y2)
            if rough_dist < 40:
                length, img, lineinfo = findDistance(lmList, 8, 4, img, draw=True)
                cv2.putText(img, "Pinch to click", (img.shape[1] - 300, img.shape[0] - 13), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255, 255, 255), 6)
                cv2.putText(img, "Pinch to click", (img.shape[1] - 300, img.shape[0] - 13), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 0, 0), 2)
                if length < 18:
                    cv2.circle(img, (lineinfo[4], lineinfo[5]), 7, (0, 255, 0), cv2.FILLED)
                    # CLICKING PART (green circle indicates that the cursor is clicking is)
                    autopy.mouse.click()
                    time.sleep(0.2)

        # SCROLLING DOWN ACTION
        # When both index and middle fingers are up AND close together
        if fingers[0] ==0 and fingers[1] == 1 and fingers[2] == 1:
            length, img, lineinfo = findDistance(lmList, 8, 12, img)
            cv2.putText(img, "Put together to scroll", (img.shape[1] - 300, img.shape[0] - 13), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255, 255, 255), 6)
            cv2.putText(img, "Put together to scroll", (img.shape[1] - 300, img.shape[0] - 13), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 0, 0), 2)
            if length < 25:
                cv2.circle(img, (lineinfo[4], lineinfo[5]), 7, (0, 255, 0), cv2.FILLED)
                y_diff = y2 - y3
                if y_diff > 8:
                    pyautogui.scroll(-50)  # scroll down
                time.sleep(0.05)

    cv2.imshow("CONTROL YOUR SCREEN CURSOR WITH FINGERS", img)
    key = cv2.waitKey(5)
    # the captured video window closes on pressing the escape key
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()
