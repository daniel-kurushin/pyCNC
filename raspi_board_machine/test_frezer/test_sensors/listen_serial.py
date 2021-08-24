#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 23.08.2021

@author: honepa
"""

from serial import Serial, SerialException
import argparse
from time import sleep

parser = argparse.ArgumentParser(description = 'Listen Serial port')
parser.add_argument("--p", help = "Name of port")
parser.add_argument("--b", type = int, help = "Baudrate, const = 9600")

args = parser.parse_args()

port = args.p
baudrate = args.b

device = Serial(port = port, baudrate = baudrate, timeout = 2)

while True:
    data = device.read_until()
    print(data)
    
