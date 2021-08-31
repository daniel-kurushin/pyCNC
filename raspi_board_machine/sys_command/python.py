#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 17:35:40 2021

@author: honepa
"""

arduino_in = {
        "state" : "ready",
        "cmd"   : "ready",
        "data"  : 0
        }
pars = dict()
pars = {'state': 'ready', 'cmd': 'ready', 'data': 0}
print(pars.get('state'))