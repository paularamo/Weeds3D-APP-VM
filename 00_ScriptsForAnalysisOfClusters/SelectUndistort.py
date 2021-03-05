# select and undistort
import cv2, sys
import numpy as np
import time
import os

filename = 'D:/00_NCSU/00_Resources/00_Datasets/PartTimePSA/Videos/alpha_10_02_2020/GH010136.MP4'
#Input the number of board images to use for calibration (recommended: ~20)
dst_folder='D:/00_NCSU/00_Resources/00_Datasets/PartTimePSA/ImageSeq/'+\
    'alpha_10_02_2020/GH010136'
if not os.path.exists(dst_folder):
    os.makedirs(dst_folder)

# n_boards=500
#Image resolution
image_size = (1920, 1080)

def selectframe(current_frame, gap):
    print('-----------------------------------------------------------------')
    resto = current_frame % gap
    if resto == 0:
	    return True
    else:
            return False

def ImageCollect(filename):
    #Collect Calibration Images
    print('-----------------------------------------------------------------')
    print('Loading video...')

    #Load the file given to the function
    video = cv2.VideoCapture(filename)
    #Checks to see if a the video was properly imported
    status = video.isOpened()

    if status == True:
        
        #Collect metadata about the file.
        FPS = video.get(cv2.CAP_PROP_FPS)
        FrameDuration = 1/(FPS/1000)
        width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        size = (int(width), int(height))

        total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        print('total frames' + str(total_frames))
        #Initializes the frame counter and collected_image counter
        current_frame = 0
        collected_images = 0

        #Video loop.  Press spacebar to collect images.  ESC terminates the function.
        while current_frame < total_frames:
            success, image = video.read()
            if success==1: 
                width = image.shape[1]
                height = image.shape[0]
                size = (int(width), int(height))
                current_frame = video.get(cv2.CAP_PROP_POS_FRAMES)
                try:
                    cv2.imshow('Video', image)
                except:
                    continue
                k = cv2.waitKey(int(FrameDuration)) #You can change the playback speed here
                if selectframe(current_frame, 10):
                    collected_images += 1
                    # if not os.path.exists(dst_folder+'/Stream_Image' + str(collected_images) + '.png'):
                    #     cv2.imwrite(dst_folder+'/Stream_Image' + str(collected_images) + '.jpg', image) #'Calibration_Image'
                    dst = cv2.undistort(image, intrinsic_matrix, distCoeff, None)
                    if not os.path.exists(dst_folder+'/Undistorted'+str(collected_images).zfill(4) +'.jpg'):
                        cv2.imwrite(dst_folder+'/UndistortedImg' + str(collected_images).zfill(4) + '.jpg', dst) #'Calibration_Image'
                    print(str(collected_images) + ' images collected.')
            else: 
                continue
            if k == 27:
                break
    
        #Clean up
        video.release()
        cv2.destroyAllWindows()
    else:
        print('Error: Could not load video')
        sys.exit()

start = time.time()
print('Loading data files')
npz_calib_file = np.load('D:/00_NCSU/00_Resources/00_Datasets/PartTimePSA/Calib/calibration_data_ml.npz')
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