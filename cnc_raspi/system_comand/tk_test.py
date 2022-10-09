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

XX, YY, ZZ = 0, 1, 2

class CNCWindow(Tk):
    def __configure(self):
        self.bind('<Escape>', lambda x : self.destroy())
        self.title("CNC Фрезерный станок")
        self.geometry("480x320")     

    def __init__(self):
        super().__init__()
        self.__configure()
        
if __name__ == "__main__":
    from sys import argv
    cnc = CNCWindow()
    cnc.mainloop()