import cv2
from glob import glob
image_paths=[]
# initialized a list of images
for i in range(26):
	image_paths.append(f'/tmp/cnc_full/[{1000000 * i}, 3200000, 0, 0].jpeg')	
#image_paths.sort()
image_paths.append('/tmp/cnc_full/[25500000, 3200000, 0, 0].jpeg')
for i in range(26):
	image_paths.append(f'/tmp/cnc_full/[{1000000 * i}, 4200000, 0, 0].jpeg')
for i in range(26):
	image_paths.append(f'/tmp/cnc_full/[{1000000 * i}, 5200000, 0, 0].jpeg')
imgs = []
#image_paths.append('/tmp/travel/IMG_20230204_125248.jpg')
#image_paths.append('/tmp/travel/IMG_20230204_124709.jpg')
for i in range(len(image_paths)):
    imgs.append(cv2.imread(image_paths[i]))
    imgs[i]=cv2.resize(imgs[i],(0,0),fx=0.4,fy=0.4)
    # this is optional if your input images isn't too large
    # you don't need to scale down the image
    # in my case the input images are of dimensions 3000x1200
    # and due to this the resultant image won't fit the screen
    # scaling down the images 
  
stitchy=cv2.Stitcher.create()
(dummy,output)=stitchy.stitch(imgs)
  
if dummy != cv2.STITCHER_OK:
  # checking if the stitching procedure is successful
  # .stitch() function returns a true value if stitching is 
  # done successfully
    print("stitching ain't successful")
else: 
    print('Your Panorama is ready!!!')
  
# final output
#cv2.imshow('final result',output)
cv2.imwrite('out_cnc_full.jpg', output)
#cv2.waitKey(0)
