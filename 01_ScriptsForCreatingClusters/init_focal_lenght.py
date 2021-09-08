#!/usr/bin/env python3
#!/home/azureuser/.venv/python3-cv/lib/python3.6/site-packages

import sys
sys.path.append("/home/azureuser/.venv/python3-cv/lib/python3.6/site-packages")

import cv2
import numpy as np
import time
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-calib", "--calibfile",default = '/home/azureuser/sfm_core/calibration/gp24667519-calib-02-gx010170.npz', help="path of calibration file you want to use")
args = parser.parse_args()

#image_size=(int(args.imgwidth*(16/9)), int(args.imgwidth))
target_image_size = (1920, 1080)
#image_size = (3840, 2160)

start = time.time()
print('loading data files')
npz_calib_file = np.load(args.calibfile)
lst = npz_calib_file.files
distCoeff = npz_calib_file['distCoeff']
intrinsic_matrix = npz_calib_file['intrinsic_matrix']
focal_length = npz_calib_file['focalLength']
focal_length_px = float(focal_length) * target_image_size[0] / 6.17

print(target_image_size[0])

print('------------------------------------------------------------')
print(args.calibfile)


for item in lst:
	print(lst)
	print(item)
	print(npz_calib_file[item])

print('------------------------------------------------------------')

fl_filename = args.calibfile[:-4] + '.txt'
with open(fl_filename, 'w+') as f:
	f.write(str(focal_length_px))
	print("Saving a text file")
	print("-------------------------------------------------------------")


npz_calib_file.close()

print('This took:' + str(duration) + ' minutes')
