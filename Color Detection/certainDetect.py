import cv2
import numpy as np
import imutils
import time

boundaries = [
    ([50, 15, 150], [80, 40, 200]),  # Red
    ([0, 215, 255], [160, 255, 255]),  # Yellow
    ([25, 146, 190], [62, 174, 250]),  # Orange
]

hsvbound = []

for (lower, upper) in boundaries:
    lowerhsv = cv2.cvtColor(np.uint8([[[lower[0], lower[1], lower[2]]]]), cv2.COLOR_BGR2HSV)
    lowhue = lowerhsv[0][0][0]
    upperhsv = cv2.cvtColor(np.uint8([[[upper[0], upper[1], upper[2]]]]), cv2.COLOR_BGR2HSV)
    upperhue = upperhsv[0][0][0]
    lowbound = [lowhue - 10, 100, 100]
    upperbound = [upperhue + 10, 255, 255]
    hsvbound.append((lowbound, upperbound))

cap = cv2.VideoCapture(0)
counter = 0
while 1:
    ret, frame = cap.read()
    if ret:
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        rlower = np.array(hsvbound[0][0], dtype="uint8")
        rupper = np.array(hsvbound[0][1], dtype="uint8")
        ylower = np.array(hsvbound[1][0], dtype="uint8")
        yupper = np.array(hsvbound[1][1], dtype="uint8")
        olower = np.array(hsvbound[2][0], dtype="uint8")
        oupper = np.array(hsvbound[2][1], dtype="uint8")

        if counter == 0:
            mask = cv2.inRange(image, ylower, yupper)
            cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                print("X : ", x)
                print("Y : ", y)
                print("R : ", radius)
                M = cv2.moments(c)
                if M["m00"] != 0:
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
        cv2.imshow("Masks", mask)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        if key == ord("e"):
            cv2.imwrite("test.jpg", mask)
cap.release()
cv2.destroyAllWindows()
