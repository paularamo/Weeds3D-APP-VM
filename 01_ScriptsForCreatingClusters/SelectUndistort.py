#!/usr/bin/env python3
import cv2, sys
import numpy as np
import time
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-fname", "--filename", default = '/home/azureuser/sfm_core/calibration/ball1meter-b1-gx010173.mp4', help = "path of file to extract frames")
parser.add_argument("-dst", "--destpath", default = '/home/azureuser/sfm_core/calibration/ball1meter-b1-gx010173', help = "path of destination folder to store frames")
parser.add_argument("-calib", "--calibfile",default = '/home/azureuser/sfm_core/calibration/gp24667519-calib-02-gx010170.npz', help="path of calibration file you want to use")
parser.add_argument("-imwidth", "--imgwidth", default=2160, help="image width")
parser.add_argument("-imgap", "--imagegap", default=10, help="default gap between frames")
args = parser.parse_args()

#filename = '/home/azureuser/sfm_core/calibration/ball1meter-b1-gx010173.mp4'
#dst_folder='/home/azureuser/sfm_core/calibration/ball1meter-b1-gx010173'
filename = args.filename
dst_folder =  args.destpath

if not os.path.exists(dst_folder):
    os.makedirs(dst_folder)

# n_boards=500
#image resolution
image_size=(int(args.imgwidth*(16/9)), int(args.imgwidth))
target_image_size = (1920, 1080)
#image_size = (3840, 2160)

def selectframe(current_frame, gap):
    print('-----------------------------------------------------------------')
    resto = current_frame % gap
    if resto == 0:
	    return True
    else:
            return False

def ImageCollect(filename):
    #collect calibration images
    print('-----------------------------------------------------------------')
    print('loading video...')

    #load the file given to the function
    video = cv2.VideoCapture(filename)
    #checks to see if a the video was properly imported
    status = video.isOpened()

    if status == True:

        #collect metadata about the file.
        fps = video.get(cv2.CAP_PROP_FPS)
        frameduration = 1/(fps/1000)
        width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        size = (int(width), int(height))

        total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        print('total frames' + str(total_frames))
        #initializes the frame counter and collected_image counter
        current_frame = 0
        collected_images = 0

        #video loop.  press spacebar to collect images.  esc terminates the function.
        while current_frame < total_frames:
            success, image = video.read()
            if success==1: 
                width = image.shape[1]
                height = image.shape[0]
                size = (int(width), int(height))
                current_frame = video.get(cv2.CAP_PROP_POS_FRAMES)
               # try:
                 #k   cv2.imshow('video', image)
                #kexcept:
                    #continue
                k = cv2.waitKey(int(frameduration)) #you can change the playback speed here
                if selectframe(current_frame, int(args.imagegap)):
                    collected_images += 1
                    # if not os.path.exists(dst_folder+'/stream_image' + str(collected_images) + '.png'):
                    #     cv2.imwrite(dst_folder+'/stream_image' + str(collected_images) + '.jpg', image) #'calibration_image'
                    dst = cv2.undistort(image, intrinsic_matrix, distCoeff, None)
                    dst = cv2.resize(dst, target_image_size)
                    if collected_images>12 and collected_images<(total_frames//10)-12 and not os.path.exists(dst_folder+'/undistorted'+str(collected_images).zfill(4) +'.jpg'):
                        cv2.imwrite(dst_folder+'/undistortedimg' + str(collected_images-12).zfill(4) + '.jpg', dst) #'calibration_image'
                    print(str(collected_images) + ' images collected.')
            else:
                continue
            if k == 27:
                break

        #clean up
        video.release()
        cv2.destroyAllWindows()
    else:
        print('error: could not load video')
        sys.exit()

start = time.time()
print('loading data files')
#npz_calib_file = np.load('/home/azureuser/sfm_core/calibration/gp24667519-calib-02-gx010170.npz')
npz_calib_file = np.load(args.calibfile)
lst = npz_calib_file.files
distCoeff = npz_calib_file['distCoeff']
intrinsic_matrix = npz_calib_file['intrinsic_matrix']
for item in lst:
	print(item)
	print(npz_calib_file[item])

npz_calib_file.close()

print('Finished loading files')
print(' ')
print('Starting to undistort the video....')

print("Starting Image Collection....")
print("Step 1: Image Collection")
print(" ")
ImageCollect(filename)
duration = (time.time()-float(start))/60

print(' ')
print('Finished undistorting the images')
print('This took:' + str(duration) + ' minutes')
