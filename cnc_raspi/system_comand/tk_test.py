"""
import tkinter
from PIL import ImageTk, Image
#480*320
cnc = tkinter.Tk()

cnc.title("CNC Фрезерный станок")
cnc.geometry("480x320")

x_end = tkinter.Frame(cnc)
x_end.config(bg="red")

x_end.place(height=cnc.winfo_screenheight(), width=10, x=0, y=0)

y_end = tkinter.Frame(cnc)
y_end.config(bg="red")

y_end.place(height=10, width=cnc.winfo_screenwidth(), x=0, y=0)

cnc.mainloop()
"""
from tkinter import *
from tkinter import filedialog as fd

class CNCWindow(Tk):
    def __configure(self):
        self.bind('<Escape>', lambda x : self.destroy())
        self.title("CNC Фрезерный станок")
        self.geometry("480x320")

        self.mpos = (DoubleVar(self, value = 0, name = 'Маш. Х'), 
                     DoubleVar(self, value = 0, name = 'Маш. Y'), 
                     DoubleVar(self, value = 0, name = 'Маш. Z'))

        self.topFrame = Frame(self)        
        self.mainFrame = LabelFrame(self)
        self.settFrame = LabelFrame(self.mainFrame, width = 100,  text = 'Параметры'  )
        self.statFrame = LabelFrame(self.mainFrame, width= 100,    text = 'Состояние:' )
        self.contFrame = LabelFrame(self.mainFrame,   text = 'Управление' )
        self.cncMoveFrame = LabelFrame(self.contFrame,text = 'Перемещение')

        self.topFrame.pack(side  = TOP, expand=0, fill=X)
        self.mainFrame.pack(side = BOTTOM, expand=1, fill=BOTH)
        self.settFrame.pack(side = LEFT,  expand=0, fill=Y)
        self.statFrame.pack(side = LEFT,  expand=1, fill=BOTH)
        self.contFrame.pack(side = RIGHT, expand=0, fill=Y)
        self.cncMoveFrame.pack(side = TOP, fill = X)

        self.statFrame.config(bg="#9FEE00") 
        
        self.canvas     = Canvas(self.statFrame, width = 100, bg="#9FEE00")
        self.canvas.create_text(50,50, text= "Готов \nтрудится на \nблаго \nкожаных \nмешков!",fill="black",font=('Helvetica 10 bold'))
        self.canvas.pack()


        self.selectFileBtn = Button(self.contFrame, text = 'Выбор файла', bg = "#37DC74")
        self.RunBtn = Button(self.contFrame, text = 'Запуск Работы')
        self.RunBtn.config(bg = "#FF4540")
        self.cncStopBtn = Button(self.contFrame, text = 'Стоп', bg = "#F60018")
        self.RunCutterBtn = Button(self.contFrame, text = 'Старт Фреза', bg = "#37DC74")
        self.StopCutterBtn = Button(self.contFrame, text = 'Стоп Фреза', bg = "#FF4540")
        for button in [ self.selectFileBtn, 
                        self.RunBtn, 
                        self.cncStopBtn,
                        self.RunCutterBtn,
                        self.StopCutterBtn]:
            button.pack(side = TOP, pady = 3, fill = X)

        #contframe
        self.decxBtn = Button(self.cncMoveFrame, text = '←')
        self.incxBtn = Button(self.cncMoveFrame, text = '→')
        self.decyBtn = Button(self.cncMoveFrame, text = '↑')
        self.incyBtn = Button(self.cncMoveFrame, text = '↓')
        self.deczBtn = Button(self.cncMoveFrame, text = '↑')
        self.inczBtn = Button(self.cncMoveFrame, text = '↓')
        self.homeBtn = Button(self.cncMoveFrame, text = '⌂')
        
        self.decxBtn.grid(row = 1, column = 0)
        self.incxBtn.grid(row = 1, column = 2)
        self.decyBtn.grid(row = 0, column = 1)
        self.incyBtn.grid(row = 2, column = 1)
        self.deczBtn.grid(row = 0, column = 3)
        self.inczBtn.grid(row = 2, column = 3)
        self.homeBtn.grid(row = 1, column = 1)

        for pos in [ self.mpos]:
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