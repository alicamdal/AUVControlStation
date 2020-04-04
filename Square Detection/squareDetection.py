import cv2 as cv
import numpy as np
import time


def angle_cos(p0, p1, p2):
    d1, d2 = (p0 - p1).astype('float'), (p2 - p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2)))


def find_squares(img):
    img = cv.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv.split(img):
        for thrs in range(0, 255, 26):
            if thrs == 0:
                bin = cv.Canny(gray, 0, 50, apertureSize=5)
                bin = cv.dilate(bin, None)
            else:
                _retval, bin = cv.threshold(gray, thrs, 255, cv.THRESH_BINARY)
            contours, _hierarchy = cv.findContours(bin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv.arcLength(cnt, True)
                cnt = cv.approxPolyDP(cnt, 0.02 * cnt_len, True)
                if len(cnt) == 4 and cv.contourArea(cnt) > 1000 and cv.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    flag = False
                    for i in cnt:
                        if i[0] == 0 or i[0] == 1:
                            flag = True
                    max_cos = np.max([angle_cos(cnt[i], cnt[(i + 1) % 4], cnt[(i + 2) % 4]) for i in range(4)])
                    if max_cos < 0.1 and flag == False:
                        squares.append(cnt)
    return squares


if __name__ == '__main__':
    cap = cv.VideoCapture(0)

    while 1:
        zaman = time.time()
        ret, frame = cap.read()
        if ret:
            squares = find_squares(frame)
            square = np.array(squares)
            x = 0
            y = 0
            if len(square) != 0:
                print(square[0])
                # x = square[0][0][0] sol üst
                # y = square[0][0][1]
                # x = square[0][1][0] sol alt
                # y = square[0][1][1]
                # x = square[0][2][0] sağ alt
                # y = square[0][2][1]
                # x = square[0][3][0] sağ üst
                # y = square[0][3][1]
                y = (square[0][1][1] + square[0][3][1]) // 2
                x = (square[0][1][0] + square[0][3][0]) // 2
                print(y)
                print(x)

            cv.drawContours(frame, squares, -1, (0, 255, 0), 3)
            cv.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), 2)

            print("Loop Takes {0} seconds.".format(time.time() - zaman))
            cv.imshow('squares', frame)
            ch = cv.waitKey(1)
            if ch == ord("q"):
                break

    cv.destroyAllWindows()
    cap.release()
