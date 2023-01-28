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

def arduino_read(old_status):
	try:
		arduino_status  = str(ser.read_until('<').decode('ascii'))
		if len(arduino_status) > 1:
			indices = [i for i in range(len(''.join(arduino_status.split('\r')).split('\n'))) if ''.join(arduino_status.split('\r')).split('\n')[i] == '<']
			arduino_status = [float(''.join(arduino_status.split('\r')).split('\n')[i]) for i in range(indices[-2] + 1, indices[-1])]
    		return arduino_status
    	else:
    		return old_status
    except:
    	return old_status
    #print(arduino_status)


if __name__ == "__main__":
    ser = Serial('/dev/ttyUSB0', baudrate=9600, timeout=0.01)
    sleep(15)
    data = [500,0,0,125]
    arduino_send(data)
    sleep(15)
    arduino_read()
    status = [0, 0, 666, 0, 0, 0, 0]
    for i in range(100):
		data = [50, 0, 0, 0]
		arduino_send(data)
		status1 = ser.readlines()
		status = read(status)
		while(not ((status[3] >= 4999000) and (status[3] <= 5000999))):
				  sleep(0.1)
				  status = read(status)
		data = [-50, 0, 0, 0]
		arduino_send(data)
		status1 = ser.readlines()
		sleep(0.4)
		status = read(status)
		while(not ((status[3] >= -10) and (status[3] <= 1000))):
			sleep(0.1)
     		status = read(status)
     	if i % 10 == 0:
			print(i)
    ser.close()
