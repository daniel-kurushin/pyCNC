"""
TODO:
1) sum time by onece
2) averenge END's for best init
"""
import RPi.GPIO as GPIO
import config
from time import sleep
import cv2 as cv

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

def cnc_init():
    count = 0
    while((GPIO.input(config.X_END)) and (count < 270)):
        x_go(-100, 1)
        count += 1
    x_go(500, 1)
    count = 0
    while((GPIO.input(config.X_END)) and (count < 500)):
        x_go(-1, 0.05)
        count += 1
    while(not (GPIO.input(config.X_END))):
        x_go(1, 0.1)
    coordinates[coor_x] = 0
    
    count = 0
    while((GPIO.input(config.Y_END)) and (count < 270)):
        y_go(-100, 1)
        count += 1
    y_go(500, 1)
    count = 0
    while((GPIO.input(config.Y_END)) and (count < 500)):
        y_go(-1, 0.05)
        count += 1
    while(not (GPIO.input(config.Y_END))):
        y_go(1, 0.1)
    coordinates[coor_y] = 0
    
    count = 0
    while((GPIO.input(config.Z_END)) and (count < 270)):
        z_go(-100, 1)
        count += 1
    z_go(500, 1)
    count = 0
    while((GPIO.input(config.Z_END)) and (count < 500)):
        z_go(-1, 0.05)
        count += 1
    while(not (GPIO.input(config.Z_END))):
        z_go(1, 0.1)
    coordinates[coor_z] = 0
    
def zero_freza():
    count = 0
    while((GPIO.input(config.Z_END)) and (count < 270)):
        z_go(-100, 1)
        count += 1
    z_go(500, 1)
    count = 0
    while((GPIO.input(config.Z_END)) and (count < 500)):
        z_go(-1, 0.05)
        count += 1
    while(not (GPIO.input(config.Z_END))):
        z_go(1, 0.1)
    coordinates[coor_z] = 0
    f = 100
    while((int(round(f / 100))) and (coordinates[coor_z] < 8000000)):
        z_go(1, 0.25)
        f = 0
        for i in range(100):
            f += GPIO.input(config.F_END) 
    coordinates[coor_freza] = coordinates[coor_z]
    
    count = 0
    while((GPIO.input(config.Z_END)) and (count < 270)):
        z_go(-100, 1)
        count += 1
    z_go(500, 1)
    count = 0
    while((GPIO.input(config.Z_END)) and (count < 500)):
        z_go(-1, 0.05)
        count += 1
    while(not (GPIO.input(config.Z_END))):
        z_go(1, 0.1)
    coordinates[coor_z] = 0

def camera_screen(coordinates):
    ret, frame = cv.VideoCapture(0).read()
    screen_name = f'/tmp/cnc/{str(coordinates)}.jpeg'
    cv.imwrite(screen_name, frame)
    print("Screen saved in " + screen_name)

def go_to_coor(x, y):
    dx = x - int(coordinates[coor_x] / 1000)
    dy = y - int(coordinates[coor_y] / 1000)
    x_go(dx, 1)
    y_go(dy, 1)

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(True)
    GPIO.setup([config.X_END, config.Y_END, config.Z_END, config.F_END], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.setup([config.x_St, config.x_Dr, config.x_En], GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(config.x_En, 1)
    
    GPIO.setup([config.y_St, config.y_Dr, config.y_En], GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(config.y_En, 1)
    
    GPIO.setup([config.z_St, config.z_Dr, config.z_En], GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(config.z_En, 1)
    
#    gcode = [[0, 3200],[3000, 3200],[6000, 3200],[9000, 3200],[12000, 3200],[15000, 3200],[18000, 3200],[21000, 3200],[24000, 3200],[25500, 3200],[25500, 5500],[24000, 5500],[21000,5500],[18000, 5500],[15000, 5500],[12000, 5500], [9000, 5500],[6000, 5500],[3000, 5500],[0, 5500],[0, 7800],[3000, 7800],[6000, 7800],[9000, 7800],[12000, 7800],[15000, 7800],[18000, 7800],[21000, 7800],[24000, 7800],[25500, 7800],[25500, 10100],[24000, 10100],[21000,10100], [18000, 10100], [15000, 10100], [12000, 10100], [9000, 10100], [6000, 10100],[3000, 10100], [0, 10100], [0, 12400], [3000, 12400], [6000, 12400], [9000, 12400], [12000,12400], [15000, 12400], [18000, 12400], [21000, 12400], [24000, 12400], [25500, 12400],[25500, 14700], [24000, 14700], [21000, 14700], [18000, 14700], [15000, 14700], [12000,14700],[9000, 14700], [6000, 14700], [3000, 14700], [0, 14700], [0, 17000], [3000, 17000], [6000,17000], [9000, 17000], [12000, 17000], [15000, 17000], [18000, 17000], [21000, 17000],[24000, 17000], [25500, 17000], [25500, 17500], [24000, 17500], [21000, 17500], [18000,17500],[15000, 17500], [12000, 17500], [9000, 17500], [6000, 17500], [3000, 17500], [0, 17500]]
    gcode = [[0, 3200], [1000, 3200]]
    cnc_init()
    
    #camera_screen(coordinates)
    
    for i in range(len(gcode)):
        go_to_coor(gcode[i][coor_x], gcode[i][coor_y])
        camera_screen(coordinates)
        #print(coordinates)
    
    GPIO.cleanup()


