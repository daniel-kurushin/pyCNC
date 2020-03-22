import sys
import re
import numpy as np
from serial import Serial, SerialException
from time import sleep
from sys import stderr

PORTS = ['/dev/ttyUSB0', '/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3',]
DESCR = b"Grbl 0.9j-XXY ['$' for help]\r\n"
OK = b'ok'

class NotACNCPortException(SerialException):
    pass

class CNC():
    def __init__(self):
        self.cncport = None
        for port in PORTS:
            try:
                print(port)
                self.cncport = Serial(port = port, baudrate = 115200, timeout = 2)
                if DESCR not in self.cncport.readlines():
                    raise NotACNCPortException
                break
            except SerialException as e:
                pass
        if self.cncport == None:
            raise SerialException('Port not found')
                
            
    def get_status(self):
        try:
            self.cncport.write(b'?\n')
            mpos_wpos = self.cncport.readline()
            status = self.cncport.readline()
            assert OK in status
            mx, my, mz, wx, wy, wz = [ float(x) / 10 for x in re.findall(r'\d+\.\d+', mpos_wpos.decode()) ]
            return (mx, my, mz), (wx, wy, wz)
        except SerialException as e:
            raise e
        except AssertionError as e:
            print(status, file = stderr)
            raise e
            
    def __delta(self, a = (0,0,0), b = (0,0,0)):
        return np.linalg.norm(np.array(a)-np.array(b))
            
    def __del__(self):
        try:
            self.cncport.close()
        except AttributeError:
            print('nothing to close!', file = sys.stderr)
            
    def go(self, pos = (0, 0, 0), absolute = 1):
        bx, by, bz = [ bytes(str(x * 10), 'ascii') for x in pos ]
        self.cncport.write(b'G0X%sY%sZ%s\n' % (bx, by, bz))
        status = self.cncport.readline()
        assert OK in status
        mpos, wpos = self.get_status()
        while self.__delta(pos, wpos) > 0.001:
            mpos, wpos = self.get_status()
            sleep(0.01)
            
    def go_z(self, amount = 0.0):
        self.cncport.write(b'G0Z%s\n' % bytes(str(amount), 'ascii'))
        assert OK in self.cncport.readline()
        for x in range(100):
            print(self.get_status())
                
    def go_y(self, amount = 0.0):
        self.cncport.write(b'G0Y%s\n' % bytes(str(amount), 'ascii'))
                
    def go_x(self, amount = 0.0):
        self.cncport.write(b'G0X%s\n' % bytes(str(amount), 'ascii'))
                
if __name__ == '__main__':
    cnc = CNC()
    cnc.go((1,1,1))
    cnc.go((1,0,1))
    cnc.go((1,1,0))
    cnc.go((0,0,0))
    del cnc
    
    