#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 12:57:46 2019

@author: dan
"""

import cv2 as cv

def read_resize(fname, width = 640, height = 480):
    try:
        open(fname,'rb')
        img = cv.imread(fname,0)
        x, y = img.shape
        if x / y > 1.33:
            k = width / x
            img = cv.resize(img, (width, int(k * y)))
        else:
            k = height / y
            img = cv.resize(img, (int(k * y), height))
        return img
    except AttributeError:
        raise ValueError('"%s" is not an image.' % fname)
    except IOError:
        raise ValueError('"%s" is not a file.' %fname)\
        
def get_contours(fname, A = 100, B = 200, width = 640, height = 480):
    img = read_resize(fname, width = 640, height = 480)
    contours, _ = cv.findContours(cv.Canny(img,A,B), cv.RETR_LIST, cv.CHAIN_APPROX_TC89_KCOS)
    return contours

if __name__ == '__main__':
    for im in ['img/4.png','/etc/passwd','nofile']:
        try:
            print(get_contours(im, 100, 200))
        except Exception as e:
            print(e)
