#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 25.08.2021

@author: honepa
"""

from serial import Serial, SerialException
from time import sleep
from tkinter import Tk

PORTS = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2', '/dev/ttyUSB3', '/dev/ttyUSB4']

commands_work = {
    "connect"       : 5,
    "ready_init"    : '555\r\n',
    "ready_work"    : '666\r\n',
    "ready_ch_stppr": '777\r\n',
    "ready_ch_metr" : '7777\r\n',
    "ready_get_mm"  : '888\r\n'
}

commands = {
    "init"   : 10,
    "run"    : 20,
    "get_mm" : 30
}

commands_run = {
    "x" : 11,
    "y" : 12,
    "z" : 13
}

def event_w(event):
    ramps.go("x", 1)
def event_a(event):
    ramps.go("y", 1)
def event_s(event):
    ramps.go("x", -1)
def event_d(event):
    ramps.go("y", -1)


class Arduino():

    def __init__(self, x):
        self.port = None
        for port in PORTS:
            try:
                #print(port)
                self.port = Serial(port = port, baudrate = 9600, timeout = 2)
                #print(self.port.readlines())
                b = self.port.read()
                if b == x:
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
        print("write code for disconnect!")

    def go(self, num_step, num_mm):
        while(self.port.read_until().decode() != commands_work.get("ready_work")):
            #print(self.port.read_until())
            pass
        self.port.write(str(commands.get("run")).encode())
        while(self.port.read_until().decode() != commands_work.get("ready_ch_stppr")):
            #print(self.port.read_until())
            pass
        self.port.write(str(commands_run.get(num_step)).encode())
        while(self.port.read_until().decode() != commands_work.get("ready_ch_metr")):
            #print(self.port.read_until())
            pass
        self.port.write(str(num_mm).encode())

    def init_ino(self):
        print(1)
        while(self.port.read_until().decode() != commands_work.get("ready_work")):
            print(self.port.read_until())
        print(2)
        self.port.write(str(commands.get("init")).encode())
        print(3)
        while(self.port.read_until().decode() != commands_work.get("ready_init")):
            print(self.port.read_until())
        print(4)
    def get_mm(self):
        while(self.port.read_until().decode() != commands_work.get("ready_work")):
            pass
        self.port.write(str(30).encode())
        while True:
            print(self.port.read_until().decode())

        """
        print(self.port.read_until().decode())
        print(1)
        self.port.write(str(commands.get("666")).encode())
        while(self.port.read_until().decode() != commands_work.get("ready_work")):
            pass
        """

if __name__ == '__main__':
    """"
    root = Tk()
    ramps = Arduino(1)
    ramps.connect()
    root.bind('w', event_w)
    root.bind('a', event_a)
    root.bind('s', event_s)
    root.bind('d', event_d)
    root.mainloop()
    """
    #print(type(work_commands.get("connect")))
    ramps = Arduino(1)
    ramps.connect()
    """
    print(1)
    while(ramps.port.read_until().decode() != '666\r\n'):
        print(ramps.port.read_until())
    print(2)
    ramps.port.write(str(10).encode())
    #print(ramps.port.read_until())
    while(ramps.port.read_until().decode() != '555\r\n'):
        #print(ramps.port.read_until())
        pass
    print(3)
    while(ramps.port.read_until().decode() != '666\r\n'):
        print(ramps.port.read_until())
    """
    #ramps.init_ino()
    ramps.go("x", 80)
    ##ramps.get_mm()
    ramps.go("y", 50)
    ramps.go("x", -20)
    ramps.go("y", -30)
    ramps.go("z", 25)
    ramps.disconnect()
    del ramps
