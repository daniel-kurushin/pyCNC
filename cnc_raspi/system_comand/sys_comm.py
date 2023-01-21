from serial import Serial
from time import sleep

SYNHRO = 255
END    = 253
delta  = 30

def arduino_send(data):
    ser.write(SYNHRO.to_bytes(2, byteorder='big',signed=0))
    ser.write(SYNHRO.to_bytes(2, byteorder='big',signed=0))
    ser.write(len(data).to_bytes(2, byteorder='big',signed=0))
    for i in data:
        ser.write(i.to_bytes(2, byteorder='big',signed=1))
    ser.write(END.to_bytes(2, byteorder='big',signed=0))

def arduino_read():
    arduino_status  = str(ser.read_until('<').decode('ascii'))
    #print(arduino_status)
    if len(arduino_status) < 0:
    	indices = [i for i in range(len(''.join(arduino_status.split('\r')).split('\n'))) if ''.join(arduino_status.split('\r')).split('\n')[i] == '<']
    	arduino_status = [int(''.join(arduino_status.split('\r')).split('\n')[i]) for i in range(indices[-2] + 1, indices[-1])]
    	if arduino_status[-3] != 1:
    		print("endstop X")
    	if arduino_status[-2] != 1:
    		print("endstop Y")
    	if arduino_status[-1] != 1:
    		print("endstop Z")
    return arduino_status


if __name__ == "__main__":
    ser = Serial('/dev/ttyUSB0', baudrate=9600, timeout=0.01)
    sleep(15)
    data = [500,0,0,125]
    arduino_send(data)
    sleep(15)
    arduino_read()
    ser.close()
