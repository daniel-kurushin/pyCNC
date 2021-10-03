#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 25.08.2021

@author: honepa
"""

from serial import Serial, SerialException
from time import sleep
import cv2 as cv
import datetime

PORTS = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2', '/dev/ttyUSB3', '/dev/ttyUSB4']

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

def camera_screen(coor):
    ret, frame = cv.VideoCapture(0).read()
    now = datetime.datetime.now()
    screen_name = 'img/test/' + '_'.join([ str(coor) for coor in coor]) + "_" + str(now.day) + "_" + str(now.month) + "_" + str(now.hour) + ":" + str(now.minute) + '.jpeg'
    cv.imwrite(screen_name, frame)
    print("Screen saved in " + screen_name)

class Arduino():

    def __init__(self, x):
        self.port = None
        for port in PORTS:
            try:
                #print(port)
                self.port = Serial(port = port, baudrate = 115200, timeout = 2)
                #print(self.port.readlines())
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
        #print(11)
        self.port.write(str(commands.get("run")).encode())
        while(self.port.read_until().decode() != commands_work.get("ready_ch_stppr")):
            pass
        #print(12)
        self.port.write(str(commands_run.get("return_coor")).encode())
        #print(13)
        while(self.port.read_until().decode() != commands_work.get("ready_ch_metr")):
            pass
        #print(1)
        self.port.write(str(commands_work.get("first_num")).encode())
        data = self.port.read_until().decode()
        data = data[:-2]
        data = float(data)
        coor.append(data)
        #print(2)
        self.port.write(str(commands_work.get("second_num")).encode())
        data = self.port.read_until().decode()
        data = data[:-2]
        data = float(data)
        coor.append(data)
        #print(3)
        self.port.write(str(commands_work.get("third_num")).encode())
        data = self.port.read_until().decode()
        data = data[:-2]
        data = float(data)
        coor.append(data)
        #print(4)
        if 2 > 0:
            self.port.write(str(commands_work.get("the_end")).encode())
        #print(5)
        return coor
    def wrt(self, data):
        self.port.write(data.encode())


if __name__ == '__main__':
    #print(type(work_commands.get("connect")))
    #now = datetime.datetime.now()
    #fileName = "/run/run_" + str(now.day) + "_" + str(now.month) + "_" + str(now.hour) + ":" + str(now.minute) + ".txt"
    #file = open(fileName, 'w')
    ramps = Arduino(1)
    ramps.connect()
    ramps.init_ino()
    print("servo_run")
    ramps.wrt("20 17 180")
    print("servo stop")
    sleep(1)
    print("servo run")
    ramps.wrt("20 17 0")
    print("servo run")
    #sleep(3)
    ramps.disconnect()
    del ramps
    #sleep(10)
    """
    data = str()
    i = 0
    j = 0
    dir = 0
    mm_zero = ramps.get_mm()
    while(i < 60):
        while(j < 60):
            mm = mm_zero - ramps.get_mm()
            data = str(j) + " " + str(i) + " " + str(mm)
            print(data)
            file.write(data + '\n')
            if dir == 0:
                ramps.go("x", 2)
            elif dir == 1:
                ramps.go("x", -2)
            j = j + 2
        if dir == 0:
            dir = 1
        elif dir == 1:
            dir = 0
        ramps.go("y", -2)
        i = i + 2
        j = 0
    file.close()
    ramps.disconnect()
    del ramps

    for i in range(30):
        for j in range(30):
            mm = ramps.get_mm()
            print(mm)
            #coor = ramps.get_now_coor()
            #print(coor)
            data = str(j) + " " + str(i) + " " + str(mm)
            file.write(data + '\n')
            if i % 2 == 0:
                ramps.go("x", 1)
            else:
                ramps.go("x", -1)
        ramps.go("y", -1)
    """
    #file.close()
    #ramps.go("x", 40)
    #mm = ramps.get_mm()
    #print(mm)
    #print(type(mm))
    #coor = ramps.get_now_coor()
    #print(coor)
    #ramps.go("y", 50)
    #ramps.go("x", -20)
    #ramps.go("y", -30)
    #ramps.go("z", 25)
    #sleep(2)

    #ramps.disconnect()
    #del ramps
