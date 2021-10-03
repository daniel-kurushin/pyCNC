#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 17:35:40 2021

@author: honepa
"""

import json
from serial import Serial, SerialException

arduino_in = { "state" : "ready", "cmd"   : "ready", "data"  : '0'}
pars = dict()
pars = {'state': 'ready', 'cmd': 'ready', 'data': 0}
k = json.dumps(arduino_in, indent = 0)
print(bytes(k, "ascii"))

arduino = Serial(port = '/dev/ttyUSB1', baudrate = 9600, timeout = 2)
arduino.write(bytes(k, "ascii"))
"""
counter = 0
while counter < 3:
    data = arduino.read().decode()
    if len(data) > 1:
        counter = counter + 1
    print(data)
"""
