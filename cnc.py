import sys
from serial import Serial, SerialException

PORTS = ['/dev/ttyUSB0', '/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3',]
DESCR = b"Grbl 0.9j-XXY ['$' for help]\r\n"

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
                
            
    def __del__(self):
        try:
            self.cncport.close()
        except AttributeError:
            print('nothing to close!', file = sys.stderr)
            
    def go_z(self, amount = 0.0):
        self.cncport.write(b'G0Z%s\r\n' % bytes(str(amount), 'ascii'))
                
    def go_y(self, amount = 0.0):
        self.cncport.write(b'G0Y%s\r\n' % bytes(str(amount), 'ascii'))
                
    def go_x(self, amount = 0.0):
        self.cncport.write(b'G0X%s\r\n' % bytes(str(amount), 'ascii'))
                
if __name__ == '__main__':
    cnc = CNC()
    cnc.go_x(10)
    cnc.go_y(10)
    cnc.go_z(10)
    print(cnc.cncport.readlines())
    del cnc
    
    