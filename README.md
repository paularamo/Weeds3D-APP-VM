# Welcome to Weeds3D System Repository

This repository will show you how to run the scripts into a Ubuntu-Azure-VM for creating point clouds, using SfM Bundler approach for sparse point clouds and pmvs for dense point clouds. 

## References of this work

S. Agarwal, N. Snavely, I. Simon, S. M. Seitz and R. Szeliski, "Building Rome in a day," _2009 IEEE 12th International Conference on Computer Vision_, 2009, pp. 72-79, doi: 10.1109/ICCV.2009.5459148.

Ramos, Paula & Avendaño, Jonathan & Prieto, Flavio. (2018). Measurement of the ripening rate on coffee branches by using 3D images in outdoor environments. Computers in Industry. 99. 83-95. 10.1016/j.compind.2018.03.024. 

J. Avendano, P.J. Ramos, and F.A. Prieto. 2017. A system for classifying vegetative structures on coffee branches based on videos recorded in the field by a mobile device. _Expert Syst. Appl._ 88, C (December 2017), 178–192. DOI:https://doi.org/10.1016/j.eswa.2017.06.044

Xie X, Yang T, Li D, Li Z, Zhang Y. Hierarchical Clustering-Aligning Framework Based Fast Large-Scale 3D Reconstruction Using Aerial Imagery. _Remote Sensing_. 2019; 11(3):315. https://doi.org/10.3390/rs11030315

# Complete pipeline

The Weeds3DSys project is looking to have production systems working properly for improveing the weed quantification task for 

This project start with an APP to control and manage video collection process and metadata integration. Using  a real-time video from consumer-grade cameras (like GoPros) we are able to reconstruct 3D imagery of field plants.  This effort will facilitate  researchers throughout the Precision Sustainable Agriculture (http://precisionsustainableag.org) and Integrated weed management (https://growiwm.org) teams to measure weeds across broad  scales without having to do destructive measures. This will save scientists time and improve the  quality of data as well as enable greater insight into the spatial variability of weeds. The  technology is set to be deployed in over 25 states in the US next year (2022).

This open-sourced software platform uses multiple overlapping images from different angles to construct 3D high-resolution digital surface models. Using Structure from Motion (SfM), a 3D-reconstruction technique we are able to use low-cost technology, which delivers impressive levels of detail. It has great potential for use in drone, tractor, or handheld phenotyping tool applications in agricultural environments, However, large-scale SfM is a difficult task, as it requires high computational time.

## What do we need?

- Android Tablet
- Weeds3D APP
	- Control and configure the GoPro before start a video.
	- Create a tempo sound to walk 50bpm.
	- Assign the video name with Calib-option and farm-code.
	- Download videos to the tablet
	- Upload videos to Azure blob storage
- Camera GoPro Hero 8
- Field equipment
- Protocol description (https://docs.google.com/presentation/d/1YRfDMnI5FZt4JgCLNXavSdmFB9AKgPN5/edit?usp=sharing&ouid=108994276950112382958&rtpof=true&sd=true)
- Blob storage connected with the Android APP
- Ubuntu VM (Azure CALS-PSA subscription) 
	- Docker file: https://hub.docker.com/r/aaminin/3d_imaging
	- docker pull aaminin/3d_imaging
	- This docker is partially working

## Structure from Motion

Based on [2], [3], and [4] we have explored differente options for reduce the computational time than SfM technique requires. In the next image you could see these steps:

1) Video/metadata collection: Camara+Tablet+APP.
2) Blob Storage receives all videos and metadata.
3) Ubunutu Virtual Machine:
	- Download the video from BlobStorage
	- Split the video into frames and create undistorted images using the camera calibration file.
	- Create clusters with and especific CLUSTERSIZE with 30% of overlapping with the next cluster.
	- Run the Complete SfM pipeline [2] [3], in each cluster. This tasks is running in parallel for all clusters. Recording the video at 60fps, walking at 50 bpm, creating cluster of 20 images/cluster, and selecting 1 frame every 10 frames we are reducing the computation time in 90%.
	- Run the Semantic Segmentation Model over each cluster, also in parallel.
	- :warning: **Don't upgrade or update the VM**: It will damage the SfM intallation!
	- :warning: **Create a new environment!! For new scripts or libraries version**

![](https://lh4.googleusercontent.com/2LDdM7vl5IU3USp6xfXdvYsFoF2y8aAnZ9AmH8yiWsvGUCOIr6uuFkHarmtJgTwdoe_R0v4OisI7ejmyoOD_RFDmG2GX9BasAgoD2G75wb0Vm6zUpTuiVuMeMuA7V93JIaHbf8bx=s0)

## What we are expecting to see?

![](https://lh6.googleusercontent.com/5IRAd5rGZPTzngk4Lx-4hlbszb5qy5NkJgwVBSHCmJyD0OVmm1KnYt7VCr_66vSuVmlHwzfB8JnjXxGN2Cz4y83cGX69QlKEdhDGZtvHimQYtV7wDlZ-s74vmel1npmqTXtNCdL6=s0)

![](https://lh5.googleusercontent.com/yI6nZowzJ9TvRCtQ1Ki1n_XkeX0qrhjb9BDQXn5VFGUR3QeFRKn7AOJo9GmsYlUVqwdQ0AWu4lAFcYp7Aqxnnch1lpm2gDcxaYjW4bZMAK_3m0Wn6E8joGE78gGmbpCcRIhqPyIz=s0)

  

![](https://lh5.googleusercontent.com/TCjbk0Cq61hWBuTL_fENpq2HATu2Nlo6kVrs8ai1aYVH8xAacuxFaQJILA5xm5ZgL2ZIBI0tIsHaXpYx3qfcDPZPtK_3VNasdLkF14q1n189Dmk-WN_q9tSF0oBobX6R3ihDo2RY=s0)

![](https://lh4.googleusercontent.com/D_b6noe4mvmebcDW8HGp41dsg7Jrc3d5Fem7gRQ9-3PoW9ZEG5jN16rd-cZLgni2jKA-ZftjjSY-lh_o7TrXJ94z0MzHCR2XROFkqTu57v-iEJzFkUUdiQm8DcsS_RiFrAoQeaaF=s0)

  

![](https://lh3.googleusercontent.com/HAH8weRzeSHPd0quxX6_9sgLUxGXnXamoa71I5Q5EXZRfzBWB39fMAbBtcQ0_Pp1zc2u0ioTy_cKSAFjXd1xpwPh7mOrskXjCRD3hajIcrH_dXAXeDW_0ilw9HB-21m40mrjf8qb=s0)

![](https://lh6.googleusercontent.com/aVn7SuqHuZr4do5YoScN8Jtp4dWzzzBEmGJxWh4iS0dyzbm6Xpz0ypfr6yeRL6sO3Wt6rdMlNBmReJSLtqiZEeFxkpXHLJFlINgzUIPyAlBv1OaRChevlEquozMM8Xj1Z-22DcC4=s0)
