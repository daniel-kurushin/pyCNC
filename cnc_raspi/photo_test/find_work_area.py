import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from glob import glob
from time import time, sleep

def perimeter(box):
	A = ((box[1][0] - box[0][0])**2 + (box[1][1] - box[0][1])**2)**0.5
	B = ((box[2][0] - box[1][0])**2 + (box[2][1] - box[1][1])**2)**0.5
	C = ((box[3][0] - box[2][0])**2 + (box[3][1] - box[2][1])**2)**0.5
	D = ((box[3][0] - box[0][0])**2 + (box[3][1] - box[0][1])**2)**0.5
	return A + B + C + D

def correcting_perspective(img):
	pt_A = [212,  284 ] 
	pt_B = [212,  2097] 
	pt_C = [3294, 2033]
	pt_D = [3208, 207 ]

	input_pts = np.float32([pt_A, pt_B, pt_C, pt_D])
	output_pts = np.float32([[210, 204],
    	                    [210, 2097], 
        	                [3296, 2097], 
            	            [3296, 204]])
	M = cv.getPerspectiveTransform(input_pts,output_pts)
	out = cv.warpPerspective(img,M,(img.shape[1],img.shape[0]),flags=cv.INTER_LINEAR)
	return out[204:2097, 210:3296]

def convert_cam_0_to_mm(coor):
	out = list()
	for i in range(len(coor)):
		l = list()
		l.append(300 - coor[i][0] / 10.287)
		l.append(coor[i][1] / 10.517)
		out.append(l)
		del l
	return out 

if __name__ == '__main__':
	'''
	imgs_path = glob('/home/duhanin/Изображения/cnc/cnc_test_1/test_ten/out_*')
	print(imgs_path)
	img_orig = cv.imread('/home/duhanin/Изображения/cnc/cnc_test_1/test_ten/out_0_912.jpeg')
	#img_orig = cv.imread('/tmp/out_0_640_480.jpeg')
	for img_path in imgs_path:
		img_orig = cv.imread(img_path)
		out = correcting_perspective(img_orig)
		cv.imwrite('/home/duhanin/Изображения/cnc/cnc_test_1/test_ten/perspective_' +str(img_path.split('/')[-1].split('.')[0]) + '_' + str(int(time())%1000) + '.jpg', out)
	#out = correcting_perspective(img_orig)
	#cv.imwrite('/tmp/out_linear.jpg', out)
	#imgs_path = ['/tmp/out.jpg']
	#imgs_path = glob('/home/duhanin/Изображения/cnc/cnc_test_1/test_ten/perspective_')
	'''
	imgs_path = ['/home/duhanin/Изображения/cnc/cnc_test_1/test_ten/perspective_out_0_525_979.jpg']
	for img_path in imgs_path:
		hsv_min = np.array((0, 54, 5), np.uint8)
		hsv_max = np.array((187, 255, 253), np.uint8)

		img = cv.imread(img_path)

		hsv = cv.cvtColor( img, cv.COLOR_BGR2HSV ) # меняем цветовую модель с BGR на HSV
		thresh = cv.inRange( hsv, hsv_min, hsv_max ) # применяем цветовой фильтр
		contours0, hierarche = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
		req_perimeter = 660
	#req_perimeter = int(img_path.split('.')[0].split('/')[-1])
	#print(req_perimeter)
		for cnt in contours0:
			rect = cv.minAreaRect(cnt)
			box = cv.boxPoints(rect)
			box = np.int0(box)
			perimeter_ = perimeter(box) / 10.286
			if ((perimeter_ < req_perimeter + 50) and (perimeter_ > req_perimeter - 50)):
		#if 1:
			#print(req_perimeter)
				cv.drawContours(img,[box],0,(255,0,0),2) # рисуем прямоугольник
				plt.imshow(img),plt.show()
				print(img_path)
				print(box)
				print(convert_cam_0_to_mm(box))
				cv.imwrite('/home/duhanin/Изображения/cnc/cnc_test_1/test_ten/find_plate_'+str(img_path.split('/')[-1].split('.')[0]) + '_' + str(int(time())%1000) + '.jpg',img)
