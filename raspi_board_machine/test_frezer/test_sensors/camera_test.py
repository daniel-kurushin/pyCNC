import cv2 as cv

ret, frame = cv.VideoCapture(0).read()

cv.imwrite('test.jpeg', frame)