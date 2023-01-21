#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 19:10:39 2020

@author: dan
"""

from tkinter import *
from tkinter import filedialog as fd

XX, YY, ZZ = 0, 1, 2

class CNCWindow(Tk):
    def __configure(self):
        self.bind('<Escape>', lambda x : self.destroy())        

        self.pos = (DoubleVar(self, value = 0, name = 'Уст. Х'), 
                    DoubleVar(self, value = 0, name = 'Уст. Y'), 
                    DoubleVar(self, value = 0, name = 'Уст. Z'))
        self.R = DoubleVar(self, value = 0)
        self.P = DoubleVar(self, value = 0)
        
        self.mpos = (DoubleVar(self, value = 0, name = 'Маш. Х'), 
                     DoubleVar(self, value = 0, name = 'Маш. Y'), 
                     DoubleVar(self, value = 0, name = 'Маш. Z'))
        self.wpos = (DoubleVar(self, value = 0, name = 'Мир. Х'), 
                     DoubleVar(self, value = 0, name = 'Мир. Y'), 
                     DoubleVar(self, value = 0, name = 'Мир. Z'))
        
        self.topFrame = Frame(self, height=20)        
        self.mainFrame = LabelFrame(self, text = 'Управление CNC')
        self.settFrame = LabelFrame(self.mainFrame, width=300,  text = 'Параметры станка')
        self.workFrame = LabelFrame(self.mainFrame, height=500, text = 'Рабочая область' )
        self.contFrame = LabelFrame(self.mainFrame, width=300,  text = 'Управление'      )
        
        self.xPosScroll = Scale(self.workFrame, orient=HORIZONTAL, from_ = 0, to = 255, showvalue = 1, variable = self.pos[XX])
        self.yPosScroll = Scale(self.workFrame, orient=VERTICAL,   from_ = 0, to = 255, showvalue = 1, variable = self.pos[YY])
        
        self.zPosScroll = Scale(self.contFrame, orient=VERTICAL,   from_ = 0, to = 255, showvalue = 1, variable = self.pos[ZZ])
        self.canvas     = Canvas(self.workFrame, width=640, height=480, bg='white')

        self.setTopLeftCornerBtn = Button(self.contFrame, text = 'Верхний левый угол')
        self.setBottomRigthCornerBtn = Button(self.contFrame, text = 'Нижний правый угол')
        self.cncStopBtn = Button(self.contFrame, text = 'Стоп')
        self.cncSafeZBtn = Button(self.contFrame, text = 'Безопасный Z')
        self.cncHomeXYBtn = Button(self.contFrame, text = 'Установить X и Y в 0')
        self.cncMoveFrame = LabelFrame(self.contFrame, text = 'Перемещение')
        
        self.topFrame.pack(side  = TOP, expand=0, fill=X)
        self.mainFrame.pack(side = BOTTOM, expand=1, fill=BOTH)
        self.settFrame.pack(side = LEFT,  expand=0, fill=Y)
        self.contFrame.pack(side = RIGHT, expand=0, fill=Y)
        self.workFrame.pack(side = LEFT,  expand=1, fill=BOTH)
        self.xPosScroll.pack(side = TOP,  expand=0, fill=X)
        self.yPosScroll.pack(side = RIGHT,expand=0, fill=Y)
        self.zPosScroll.pack(side = LEFT, expand=1, fill=Y)
        self.canvas.pack(side = LEFT, expand = 1, fill=BOTH)
        for button in [ self.setTopLeftCornerBtn, 
                        self.setBottomRigthCornerBtn, 
                        self.cncStopBtn,
                        self.cncSafeZBtn,
                        self.cncHomeXYBtn]:
            button.pack(side = TOP, pady = 3, fill = X)
        self.cncMoveFrame .pack(side = TOP, fill = X)
        self.decxBtn = Button(self.cncMoveFrame, text = '←')
        self.incxBtn = Button(self.cncMoveFrame, text = '→')
        self.decyBtn = Button(self.cncMoveFrame, text = '↑')
        self.incyBtn = Button(self.cncMoveFrame, text = '↓')
        self.deczBtn = Button(self.cncMoveFrame, text = '↑')
        self.inczBtn = Button(self.cncMoveFrame, text = '↓')
        
        self.decxBtn.grid(row = 1, column = 0)
        self.incxBtn.grid(row = 1, column = 2)
        self.decyBtn.grid(row = 0, column = 1)
        self.incyBtn.grid(row = 2, column = 1)
        self.deczBtn.grid(row = 0, column = 3)
        self.inczBtn.grid(row = 2, column = 3)
        
        for pos in [ self.mpos, self.wpos ]:
            for v in pos:
                f = LabelFrame(self.settFrame, text = str(v))
                f.pack(side = TOP, expand = 0, fill = Y)
                Entry(f, textvariable = v).pack(side = TOP, expand = 0, fill = Y)
    
    def __init__(self):
        super().__init__()
        self.__configure()
        
if __name__ == "__main__":
    from sys import argv
    cnc = CNCWindow()
    cnc.mainloop()