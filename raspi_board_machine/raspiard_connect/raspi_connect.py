#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 25.08.2021

@author: honepa
"""

from serial import Serial, SerialException
from time import sleep

PORTS = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2', '/dev/ttyUSB3', '/dev/ttyUSB4']

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

if __name__ == '__main__':
    """
    device = Serial(port = '/dev/ttyUSB0', baudrate = 9600, timeout = 2)
    device.write(str(10).encode())
    while(1):
        device.write(str(10).encode())
        print(device.read_until())
    """
    ramps = Arduino(1)
    print(ramps)
    ramps.port.write(str(5).encode())
    #sleep(4)
    print(1)
    while(ramps.port.read_until().decode() != '666\r\n'):
        #ramps.port.write(str(5).encode())
        print(ramps.port.read_until())
    print(2)
    #sleep(4)
    ramps.port.write(str(10).encode())
    print(3)

    while(ramps.port.read_until().decode() != '777\r\n'):
        print(ramps.port.read_until())
    print(4)

    ramps.port.write(str(11).encode())
    while(ramps.port.read_until().decode() != '7777\r\n'):
        print(ramps.port.read_until())
    print(5)
    #sleep(2)

    #sleep(2)
    ramps.port.write(str(20).encode())
    print(6)
    while(ramps.port.read_until().decode() != '666\r\n'):
        #ramps.port.write(str(5).encode())
        print("RUN")
    print("DONE!)")
    del ramps
