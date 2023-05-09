import cv2 as cv
import numpy as np
import sys

def get_frames(id):
    cam = cv.VideoCapture(id)
    assert cam.isOpened()
    cam.set(3, 1920)
    cam.set(4, 1080)
    out = np.zeros((int(cam.get(4)*2),int(cam.get(3)*2), 3))
    for i in range(10):
        out[::2 ,  ::2] = cam.read()[1]
        out[::2 , 1::2] = cam.read()[1]
        out[1::2,  ::2] = cam.read()[1]
        out[1::2, 1::2] = cam.read()[1]
    return out

if __name__ == '__main__':
    try:
        id = int(sys.argv[1])
        w = int(sys.argv[2])
        h = int(sys.argv[3])
    except IndexError:
        id = 0
        w = 640
        h = 480
    img = get_frames(id)
    print(f'/tmp/out_{id}_{w}_{h}.jpeg written')
    cv.imwrite(f'/tmp/out_{id}_{w}_{h}.jpeg', img)

