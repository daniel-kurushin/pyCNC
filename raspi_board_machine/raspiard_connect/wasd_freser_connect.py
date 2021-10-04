#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 25.08.2021

@author: honepa
"""

from serial import Serial, SerialException
from time import sleep
from tkinter import Tk
import cv2 as cv
import datetime
import numpy as np

PORTS = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2', '/dev/ttyUSB3', '/dev/ttyUSB4']

plate_angle = 1

commands_work = {
    "ramps_code"    : '1\r\n',
    "connect"       : 5,
    "ready_init"    : '555\r\n',
    "ready_work"    : '666\r\n',
    "ready_ch_stppr": '777\r\n',
    "ready_ch_metr" : '7777\r\n',
    "ready_get_mm"  : '888\r\n',
    "first_num"     : 42,
    "second_num"    : 43,
    "third_num"     : 44,
    "the_end"       : 73
}

commands = {
    "run"        : 20,
    "disconnect" : 40 #10 - init 30 - get_now_coor - dont work in arduino freser
}

commands_run = {
    "x"           : 11,
    "y"           : 12,
    "z"           : 13,
    "init"        : 14,
    "return_mm"   : 15,
    "return_coor" : 16,
    "lazer_servo" : 17,
    "plate_servo" : 18
}

def event_w(event):
    ramps.go("x", 1)
def event_a(event):
    ramps.go("y", 1)
def event_s(event):
    ramps.go("x", -1)
def event_d(event):
    ramps.go("y", -1)

def event_c(event):
    coor = ramps.get_now_coor()
    camera_screen(coor)

def event_v(event):
    camera_video()

def event_m(event):
    mm = ramps.get_mm()
    print(mm)

def event_k(event):
    coor = ramps.get_now_coor()
    print(coor)
    print("Plate servo: " + str(plate_angle))

def event_e(event):
    ramps.go("z", 1)

def event_f(event):
    ramps.go("z", -1)

def event_r(event):
    global plate_angle
    if plate_angle < 181 and plate_angle > 0:
        plate_angle += 1
        ramps.go("plate_servo", plate_angle)

def event_g(event):
    global plate_angle
    if plate_angle < 181 and plate_angle > 0:
        plate_angle += 1
        ramps.go("plate_servo", plate_angle)

def event_t(event):
    ramps.go("lazer_servo", 1)
    sleep(0.5)
    ramps.go("lazer_servo", 180)
    sleep(0.5)

def event_i(event):
    ramps.init_ino()

def event_q(event):
    ramps.disconnect()
    root.destroy()

def camera_screen(coor):
    ret, frame = cv.VideoCapture(0).read()
    now = datetime.datetime.now()
    screen_name = 'img/test/' + '_'.join([ str(coor) for coor in coor]) + "_" + str(now.day) + "_" + str(now.month) + "_" + str(now.hour) + ":" + str(now.minute) + '.jpeg'
    cv.imwrite(screen_name, frame)
    print("Screen saved in " + screen_name)

def camera_video():
    cap = cv.VideoCapture(0)

    while(True):
        ret, frame = cap.read()
        cv.imshow('Video', frame)
        if cv.waitKey(1) & 0xFF == ord('x'):
            break

    cap.release()
    cv.destroyAllWindows()

class Arduino():

    def __init__(self, x):
        self.port = None
        for port in PORTS:
            try:
                self.port = Serial(port = port, baudrate = 115200, timeout = 2)
                b = self.port.read_until()
                if b == commands_work.get("ramps_code"):
                    break
            except SerialException as e:
                print(port, 'failed')

        if self.port == None:
            raise SerialException('Port is not found')

    def __del__(self):
        try:
            self.port.close()
        except AttributeError:
            print('nicht close', file = sys.stderr)

    def __str__(self):
        return str(self.port)

    def connect(self):
        try:
            self.port.write(str(commands_work.get("connect")).encode())
        except:
            print("Don't connect")

    def disconnect(self):
        print(1)
        while(self.port.read_until().decode() != commands_work.get("ready_work")):
            pass
        print(2)
        self.port.write(str(commands.get("disconnect")).encode())
        print("disconnect")

    def go(self, num_step, num_mm):
        while(self.port.read_until().decode() != commands_work.get("ready_work")):
            pass
        self.port.write(str(commands.get("run")).encode())
        while(self.port.read_until().decode() != commands_work.get("ready_ch_stppr")):
            pass
        self.port.write(str(commands_run.get(num_step)).encode())
        while(self.port.read_until().decode() != commands_work.get("ready_ch_metr")):
            pass
        self.port.write(str(num_mm).encode())

    def init_ino(self):
        while(self.port.read_until().decode() != commands_work.get("ready_work")):
            pass
        self.port.write(str(commands.get("run")).encode())
        while(self.port.read_until().decode() != commands_work.get("ready_ch_stppr")):
            pass
        self.port.write(str(commands_run.get("init")).encode())
        while(self.port.read_until().decode() != commands_work.get("ready_ch_metr")):
            pass
        self.port.write(str(42).encode())

    def get_mm(self):
        while(self.port.read_until().decode() != commands_work.get("ready_work")):
            pass
        self.port.write(str(commands.get("run")).encode())
        while(self.port.read_until().decode() != commands_work.get("ready_ch_stppr")):
            pass
        self.port.write(str(commands_run.get("return_mm")).encode())
        while(self.port.read_until().decode() != commands_work.get("ready_ch_metr")):
            pass
        self.port.write(str(commands_work.get("first_num")).encode())
        while self.port.read_until().decode() != commands_work.get("ready_ch_metr"):
            data = self.port.read_until().decode()
        data = data[:-2]
        data = float(data)
        if data > 0:
            self.port.write(str(commands_work.get("the_end")).encode())
        return data

    def get_now_coor(self):
        coor = list()
        while(self.port.read_until().decode() != commands_work.get("ready_work")):
            pass
        self.port.write(str(commands.get("run")).encode())
        while(self.port.read_until().decode() != commands_work.get("ready_ch_stppr")):
            pass
        self.port.write(str(commands_run.get("return_coor")).encode())
        while(self.port.read_until().decode() != commands_work.get("ready_ch_metr")):
            pass
        self.port.write(str(commands_work.get("first_num")).encode())
        data = self.port.read_until().decode()
        data = data[:-2]
        data = float(data)
        coor.append(data)
        self.port.write(str(commands_work.get("second_num")).encode())
        data = self.port.read_until().decode()
        data = data[:-2]
        data = float(data)
        coor.append(data)
        self.port.write(str(commands_work.get("third_num")).encode())
        data = self.port.read_until().decode()
        data = data[:-2]
        data = float(data)
        coor.append(data)
        if 2 > 0:
            self.port.write(str(commands_work.get("the_end")).encode())
        return coor


if __name__ == '__main__':

    root = Tk()
    ramps = Arduino(1)
    ramps.connect()
    ramps.init_ino()
    print("READY")
    root.bind('w', lambda event : event_w(event)) #x + 1
    root.bind('a', lambda event : event_a(event)) #y + 1
    root.bind('s', lambda event : event_s(event)) #x - 1
    root.bind('d', lambda event : event_d(event)) #y + 1
    root.bind('c', event_c) #camera_screen
    root.bind('v', event_v) #camera_video
    root.bind('m', event_m) #distanse
    root.bind('k', event_k) #coor
    root.bind('e', lambda event : event_e(event)) #z + 1
    root.bind('f', lambda event : event_f(event)) #z - 1
    root.bind('r', lambda event : event_r(event)) #rotate plate +
    root.bind('g', lambda event : event_g(event)) #rotate plate-
    root.bind('t', event_t) #rotate lazer
    root.bind('i', event_i) #init
    root.bind('q', event_q) #quit
    root.mainloop()
