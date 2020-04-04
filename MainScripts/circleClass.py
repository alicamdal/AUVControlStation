import numpy as np
import cv2


class Circle:

    def __init__(self):
        pass

    def detect(self,frame):
        if frame is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            w,h = gray.shape[::-1]
            circle = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1.2,100)
            print(circle)
            if circle is not None:
                circles = np.round(circle[0, :]).astype("int")
                for (x,y,r) in circles:
                    X = x
                    Y = y
                    R = r
                return X,Y,R
            else:
                return None