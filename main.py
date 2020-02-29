#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 19:10:39 2020

@author: dan
"""

from tkinter import *
from tkinter import filedialog as fd

class CNCWindow(Tk):
    def __configure(self):
        self.bind('<Escape>', lambda x : self.destroy())        

        self.X = IntVar(self, value = 0)
        self.Y = IntVar(self, value = 0)
        self.Z = IntVar(self, value = 0)
        self.R = IntVar(self, value = 0)
        self.P = IntVar(self, value = 0)
        
        self.topFrame = Frame(self, height=20, bg='green')        
        self.mainFrame = LabelFrame(self, text = 'Управление CNC', bg='yellow')
        self.settFrame = LabelFrame(self.mainFrame, width=300,  text = 'Параметры станка', bg='green')
        self.workFrame = LabelFrame(self.mainFrame, height=500, text = 'Рабочая область',  bg='cyan')
        self.contFrame = LabelFrame(self.mainFrame, width=300,  text = 'Управление',       bg='blue')
        
        self.xPosScroll = Scale(self.workFrame, orient=HORIZONTAL, from_ = 0, to = 255, showvalue = 1, variable = self.X)
        self.yPosScroll = Scale(self.workFrame, orient=VERTICAL,   from_ = 0, to = 255, showvalue = 1, variable = self.Y)
        self.zPosScroll = Scale(self.contFrame, orient=VERTICAL,   from_ = 0, to = 255, showvalue = 1, variable = self.Z)
        self.canvas     = Canvas(self.workFrame, width=640, height=480, bg='white')

        
        self.topFrame.pack(side  = TOP, expand=0, fill=X)
        self.mainFrame.pack(side = BOTTOM, expand=1, fill=BOTH)
        self.settFrame.pack(side = LEFT,  expand=0, fill=Y)
        self.contFrame.pack(side = RIGHT, expand=0, fill=Y)
        self.workFrame.pack(side = LEFT,  expand=1, fill=BOTH)
        self.xPosScroll.pack(side = TOP,  expand=0, fill=X)
        self.yPosScroll.pack(side = RIGHT,expand=0, fill=Y)
        self.zPosScroll.pack(side = LEFT, expand=1, fill=Y)
        self.canvas.pack(side = LEFT, expand = 1, fill=BOTH)
    
    def __init__(self):
        super().__init__()
        self.__configure()
        
if __name__ == "__main__":
    from sys import argv
    cnc = CNCWindow()
    cnc.mainloop()