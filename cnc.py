import sys
from serial import Serial, SerialException

PORTS = ['/dev/ttyUSB0', '/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3',]

class CNC():
    def __init__(self):
        self.cncport = None
        for port in PORTS:
            try:
                print(port)
                self.cncport = Serial(port = port, baudrate = 115200, timeout = 2)
                print(self.cncport.readlines())
                break
            except SerialException as e:
                pass
        if self.cncport == None:
            raise SerialException('Port not found')
                
            
    def __del__(self):
        try:
            self.cncport.close()
        except AttributeError:
            print('nothing to close!', file = sys.stderr)
                
if __name__ == '__main__':
    cnc = CNC()
    del cnc
    