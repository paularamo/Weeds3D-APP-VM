# Before using the GoPro Camera!  
  
Please before use the GoPro camera you should run the calibration process.  
## Take a calibration video  
  
1. Locate the camera on a tripod or monopod.  
2. Mark six points on the floor (shown in the next images). The first point is to 50cm from the camera, the second line is to 100cm and the last line is to 150 cm from the camera. Maybe you could use an extra hand to locate the points better, all time the chess board should be in the image.  
3. Open the APP and create a farm with the name of the camera you have and the world CALIB. Go to the "Camera info" option to know this name.  
4. Make a calibration video using the APP.  
5. Be aware that you should move the chess board during the video, and also stop into the key positions. See the next images for better understanding. In total you should have 42 key locations to stop during the video. This video could take in between 2 or 3 minutes, so no worries take your time.
6. 
![](https://lh4.googleusercontent.com/0ILO1N3ssOxX9lPkBFoTaPGwYkkAXswDGZ7uye7Lyt0K2CmlVMThv6dJcNvYDe6_yrWTdp25yVLghKl0yOa-deRzBai_xDcIIt6z29EQvsmrOnCMGiWdfGjjldfwENxk4Qs8QM4e=s0)

  

![](https://lh5.googleusercontent.com/b2F8FqtE55gyfkirW4C59QfnLy2SwC2x5U0-7_1fgTtt4JpgxjhRN81FPlRs2q-RfYKPr0b5h_7eQlJVgOKKfY9spk3jR0tjC64G8sAQlmkPbIDr4M20JjRn5cochxemgLre5b63=s0)

![](https://lh6.googleusercontent.com/o_qNPGIPWnpNd4LqR2_712MKi1oIn6jbhHVc67pPcm_r-jrYuFBIbkstxQ1d8Hl1cMAqbyOhKJDkflard3CD8ayaNrGHaHMnxloNAOm4pdoCBa8_yEDhyC42uBgv2BleCCYpG0xl=s0)

## Video processing


The goal is to get a npz file with intrinsic matrix, distortion coefficients and focal length in mm per camera. As requirements you should have OpenCV > 3.0.0, python 3 and NumPy 1.18.0.  
  
Run the python scripts included in the code section. **GoPro_calib...py** will make an interface with your keyboard which is used to select the key locations of the chess board and select that frame as an input into the calibration process.
