import cv2, sys
import numpy as np


print 'Loading data files'

npz_calib_file = np.load('calibration_data.npz')
lst = npz_calib_file.files

distCoeff = npz_calib_file['distCoeff']
intrinsic_matrix = npz_calib_file['intrinsic_matrix']
focalLength = npz_calib_file["focalLength"]

for item in lst:
	print(item)
	print(npz_calib_file[item])

npz_calib_file.close()

print('Finished loading files')
print(' ')
print('Starting to undistort the video....')

print('fovx, fovy, focalLength, principalPoint, aspectRatio ', cv2.calibrationMatrixValues(intrinsic_matrix, (3840, 2160), 6.17, 4.63))

# print('fovx, fovy, focalLength, principalPoint, aspectRatio ', cv2.calibrationMatrixValues(intrinsic_matrix, (1920, 1080), 6.17, 4.63)) #Change the image size (1920,1080)
