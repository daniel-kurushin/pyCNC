import RPi.GPIO as GPIO
import config
from time import sleep

FRW =  1
BCK = -1
coor_x     = 0
coor_y     = 1
coor_z     = 2
coor_freza = 3
coordinates = [0, 0, 0, 0]

def x_step(direction, speed_x):
    d = 1 if direction == FRW else 0
    GPIO.output(config.x_St, 0)
    GPIO.output(config.x_Dr, d)
    sleep((round(round((pow(speed_x * 800, -1) * pow(10, 5))) / 2)) * 10**-6)
    GPIO.output(config.x_St, 1)
    GPIO.output(config.x_Dr, d)
    sleep((round(round((pow(speed_x * 800, -1) * pow(10, 5))) / 2)) * 10**-6) 
    coordinates[coor_x] += direction * 125

def y_step(direction, speed_y):
    d = 1 if direction == FRW else 0
    GPIO.output(config.y_St, 0)
    GPIO.output(config.y_Dr, d)
    sleep((round(round((pow(speed_y * 800, -1) * pow(10, 5))) / 2)) * 10**-6)
    GPIO.output(config.y_St, 1)
    GPIO.output(config.y_Dr, d)
    sleep((round(round((pow(speed_y * 800, -1) * pow(10, 5))) / 2)) * 10**-6) 
    coordinates[coor_y] += direction * 125

def z_step(direction, speed_z):
    d = 1 if direction == FRW else 0
    GPIO.output(config.z_St, 0)
    GPIO.output(config.z_Dr, d)
    sleep((round(round((pow(speed_z * 800, -1) * pow(10, 5))) / 2)) * 10**-6)
    GPIO.output(config.z_St, 1)
    GPIO.output(config.z_Dr, d)
    sleep((round(round((pow(speed_z* 800, -1) * pow(10, 5))) / 2)) * 10**-6) 
    coordinates[coor_z] += direction * 125

def x_go(mm, speed_x):
    steps = mm * config.X_STEPS_MM
    GPIO.output(config.x_En, 0)
    d = FRW if steps > 0 else BCK
    for i in range(abs(steps)):
        x_step(d, speed_x)
    GPIO.output(config.x_En, 1)
    
def y_go(mm, speed_y):
    steps = mm * config.Y_STEPS_MM
    GPIO.output(config.y_En, 0)
    d = FRW if steps > 0 else BCK
    for i in range(abs(steps)):
        y_step(d, speed_y)
    GPIO.output(config.y_En, 1)
    
def z_go(mm, speed_z):
    steps = mm * config.Z_STEPS_MM
    GPIO.output(config.z_En, 0)
    d = FRW if steps > 0 else BCK
    for i in range(abs(steps)):
        z_step(d, speed_z)
    GPIO.output(config.z_En, 1)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(True)
GPIO.setup([config.X_END, config.Y_END, config.Z_END, config.F_END], GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup([config.x_St, config.x_Dr, config.x_En], GPIO.OUT, initial=GPIO.LOW)
GPIO.output(config.x_En, 1)

GPIO.setup([config.y_St, config.y_Dr, config.y_En], GPIO.OUT, initial=GPIO.LOW)
GPIO.output(config.y_En, 1)

GPIO.setup([config.z_St, config.z_Dr, config.z_En], GPIO.OUT, initial=GPIO.LOW)
GPIO.output(config.z_En, 1)

mm = -500
speed_z = 1
while(GPIO.input(config.X_END)):
    x_go(-10, 1)
print(coordinates[coor_z])

GPIO.cleanup()

