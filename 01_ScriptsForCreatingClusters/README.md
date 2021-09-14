# FILES USED FOR CREATING CLUSTERS AND CLUSTERED POINT CLOUDS 

## RunBundler.sh 
Default RunBundler.sh from home/azureuser/scripts/Weeds3D-APP-VM/01_ScriptsForCreatingClusters. The requirement is the focal lenght in pixels saved in a text file.
Environment: /etc/bash.bashrc
```
sudo RunBundler.sh <path/calibration/file/txt/extension>
```

## SelectUndistort.py 
This script creates a folder with selected and undistorted frames from a mp4 video. For selecting frames you should know the gap number inbetween frames.
```
usage: SelectUndistort.py [-h] [-fname FILENAME] [-dst DESTPATH]
                          [-calib CALIBFILE] [-imwidth IMGWIDTH]
                          [-imgap IMAGEGAP]
optional arguments:
  -h, --help            show this help message and exit
  -fname FILENAME, --filename FILENAME
                        path of file to extract frames
  -dst DESTPATH, --destpath DESTPATH
                        path of destination folder to store frames
  -calib CALIBFILE, --calibfile CALIBFILE
                        path of calibration file you want to use
  -imwidth IMGWIDTH, --imgwidth IMGWIDTH
                        image width
  -imgap IMAGEGAP, --imagegap IMAGEGAP
                        default gap between frames
```
## create_clusters.bash
Create packages of images from extracted images from SelectUndistort.py 
Environment: /etc/bash.bashrc
```
usage
./create_clusters.bash ~/path/to/clusters/ <CLUSTER_SIZE>
```

## run_bundler_clustering_files.sh 
Launch a parallel task to run the RunBundler over all created clusters. It should be copy first in the folder of interest.
Environment: /etc/bash.bashrc
```
usage 
./run_bundler_clustering_files.sh <root/dir/of/clusters> <CLUSTER_SIZE> 
```

## createSegMaps.py 
Create the labeled images running the Semantic Segmentation model in every cluster
```
usage: createSegMaps.py [-h] [-isize INPUTSIZE] [-ipath INPUTPATH]
                        [-opath OUTPUTPATH] [-model CURRENTMODEL]

optional arguments:
  -h, --help            show this help message and exit
  -isize INPUTSIZE, --inputsize INPUTSIZE
                        Model frozen with max resolution of 2048x2048 pixel.
                        Images resized to this before inference
  -ipath INPUTPATH, --inputpath INPUTPATH
                        path for the clustered images
  -opath OUTPUTPATH, --outputpath OUTPUTPATH
                        path for storing the output images
  -model CURRENTMODEL, --currentmodel CURRENTMODEL
                        Path for the deeplabmodel to do segmentation
```

## run_createSegs.sh
Launch a parallel task to run the createSegMaps.py over all created clusters. It should be copy first in the folder of interest.
```
usage 
./run_createSegs.sh <root/dir/of/clusters/CLUSTER_SIZE> 
```

# Calibration files and initial focal lenght

For running the SfM-Bundler you should be sure you have the calibration file (npz) of your camera. Take a look in this list. https://docs.google.com/spreadsheets/d/1NdrbOobBGW19_rdzE55aWZ0WH0yAbd0cyEQQgXfmc_c/edit?usp=sharing

With npz file you are able to calculate initial focal lenght, using this script <span style="color:red">some **"init_focal_lenght.py".** text</span>, and saving the result as text file in the same folder

```
   python3 /home/azureuser/scripts/Weeds3D-APP-VM/01_ScriptsForCreatingClusters/init_focal_lenght.py /home/azureuser/calibration_files/${CALIB}
```

For Example the CALIB for DELAWARE is GP51457925-CALIB-01-GX010001.npz 
```
   python3 /home/azureuser/scripts/Weeds3D-APP-VM/01_ScriptsForCreatingClusters/init_focal_lenght.py /home/azureuser/calibration_files/GP51457925-CALIB-01-GX010001.npz
```

# General Process to Create Clustered point clouds. (Manually)

0. Be sure you have all calibration files in this path /home/azureuser/calibration_files.

1. Select the npz file related with the first code of the video. 
    See this spreadsheet: https://docs.google.com/spreadsheets/d/1NdrbOobBGW19_rdzE55aWZ0WH0yAbd0cyEQQgXfmc_c/edit?usp=sharing

2. Download the video using sudo azcopy copy as follow:
```
   sudo azcopy copy "${SAS}" "/home/azureuser/data/videos/${STATE}/${VIDEOFILE}.mp4"
```
Example:
```   
   sudo azcopy copy "https://weedsmedia.blob.core.usgovcloudapi.net/weeds3d/DE-C4D-1S-CALIB-FIELD14SOY-GX010064.MP4?sv=2019-12-12&st=2021-09-08T20%3A36%3A58Z&se=2021-10-09T20%3A36%3A00Z&sr=b&sp=r&sig=Xkq6phKbLPQooAmw%2BwZq8k2Kcd3aNLfwpTG4Wf76G8A%3D "/home/azureuser/data/videos/DE/DE-C4D-1S-CALIB-FIELD14SOY-GX010064.mp4"
```

3. Go to active folder
```
   cd /home/azureuser/data/videos/${STATE}
```   
Example:
```   
   cd /home/azureuser/data/videos/DE
```
4. Active the environment for CV and python 3
```    
   source ~/.venv/python3-cv/bin/activate
```

5. Create folder named with the same video file name
```
   mkdir ${VIDEOFILE}
```
Example:
```   
   mkdir /home/azureuser/data/videos/DE
```
7. Split the video into frames
```
   sudo python3 /home/azureuser/scripts/Weeds3D-APP-VM/01_ScriptsForCreatingClusters/SelectUndistort.py -fname "/home/azureuser/data/videos/${STATE}/${VIDEOFILE}.mp4" -dst "/home/azureuser/data/videos/${STATE}/${VIDEOFILE}" -calib "/home/azureuser/calibration_files/${CALIB}.npz" -imgap ${SUBSAMPLE}
```
Example:
```   
   sudo python3 /home/azureuser/scripts/Weeds3D-APP-VM/01_ScriptsForCreatingClusters/SelectUndistort.py -fname "/home/azureuser/data/videos/DE/DE-C4D-1S-CALIB-FIELD14SOY-GX010064.mp4" -dst "/home/azureuser/data/videos/DE/DE-C4D-1S-CALIB-FIELD14SOY-GX010064" -calib "/home/azureuser/calibration_files/GP51471258-CALI-01-GX010002.npz" -imgap 10
```
8. Change environment
```
   source /etc/bash.bashrc
   sudo ldconfig
```   

9. Copy create_clusters.bash into the active folder (where the frames are)
```
   cp /home/azureuser/scripts/Weeds3D-APP-VM/01_ScriptsForCreatingClusters/create_clusters.bash "/home/azureuser/data/videos/${STATE}/${VIDEOFILE}"
```
Example:
```   
   cp /home/azureuser/scripts/Weeds3D-APP-VM/01_ScriptsForCreatingClusters/create_clusters.bash "/home/azureuser/data/videos/DE/DE-C4D-1S-CALIB-FIELD14SOY-GX010064"
```
10. Go to splited frames are (same folder mentioned before)
```
   cd /home/azureuser/data/videos/${STATE}/${VIDEOFILE}
```
11. Create the host folder for clusters
```
   mkdir clustering${CLUSTERSIZE}
```
12. Create the clusters: number of images per cluster is another input.
```   
   sudo bash create_clusters.bash "/home/azureuser/data/videos/${STATE}/${VIDEOFILE}/clustering" "/home/azureuser/data/videos/${STATE}/${VIDEOFILE}/" ${CLUSTERSIZE}
```
Example with clusters of 20 images with overlapping
```   
   sudo bash create_clusters.bash "/home/azureuser/data/videos/DE/DE-C4D-1S-CALIB-FIELD14SOY-GX010064/clustering" "/home/azureuser/data/videos/DE/DE-C4D-1S-CALIB-FIELD14SOY-GX010064/" 20
```
13. Clean storage space into this folder
```
   sudo rm *.jpg
```   

14. Copy the parallelization script into the active folder(where the frames are)
```    
   cp /home/azureuser/scripts/Weeds3D-APP-VM/01_ScriptsForCreatingClusters/run_bundler_clustering_files.sh "/home/azureuser/data/videos/${STATE}/${VIDEOFILE}"
```
15. Run the SfM in all clusters
```
   sudo ./run_bundler_clustering_files.sh /home/azureuser/data/videos/${STATE}/${VIDEOFILE}/clustering  ${CLUSTERSIZE} /home/azureuser/calibration_files/${CALIB}.txt
```   

In case you want to now timing in this step use this CLI
```   
   { time  ./run_bundler_clustering_files.sh <path/to/clusters> <cluster_size> ; } 2> ~/logs/'print($1$f)';"  
```

Example: 
```
   sudo { time ./run_bundler_clustering_files.sh /home/azureuser/data/cool-calibrators/DE-CD1-14A1-1-CALIB-CD1-14A1-1-GX010023/clustering 20 ; } 2> ~/logs/DE-CD1-14A1-1-CALIB-CD1-14A1-1-GX010023_20.log;
```

16. Copy the permissions_pmvs script into the active folder(where the frames are)
```
   cp /home/azureuser/scripts/Weeds3D-APP-VM/01_ScriptsForCreatingClusters/permissions_pmvs.sh "/home/azureuser/data/videos/${STATE}/${VIDEOFILE}"
```
17. Give permission for all "pmvs" subfolders in the clustering folder
```
   sudo ./permissions_pmvs.sh /home/azureuser/data/videos/${STATE}/${VIDEOFILE}/clustering  ${CLUSTERSIZE}
```
18. Select the proper environment to run Semantic Segmentation Model 
```
   source ~/.venv/tf_1/bin/activate
```
************************
  
9. run createSegMaps.py with proper arguments to create segmentation maps for clustered point clouds. 
  Example - createSegMaps.py -isize 3840 -ipath /home/azureuser/data/cool-calibrators/DE-CD1-14A1-1-CALIB-CD1-14A1-1-GX010023/clustering20 -opath /home/azureuser/data/cool-calibrators/DE-CD1-14A1-1-CALIB-CD1-14A1-1-GX010023/clustering20 -model /home/azureuser/segmentation/deeplabv3+/3_class_mobilenet_v3_small_small_v2.1/ 3_class_model_mobilenet_v3_small_v2.1_1080x1920.pb

# General Process to Create Clustered point clouds. (Automatically)

    >  sudo bash run.sh "${SAS}" "${STATE}" "${CALIB}" "${VIDEOFILE}" ${CLUSTERSIZE} ${SUBSAMPLE}
    
Example
    
    >  sudo bash run.sh "https://weedsmedia.blob.core.usgovcloudapi.net/weeds3d/DE-C4D-1S-CALIB-FIELD14SOY-GX010064.MP4?sv=2019-12-12&st=2021-09-08T20%3A36%3A58Z&se=2021-10-09T20%3A36%3A00Z&sr=b&sp=r&sig=Xkq6phKbLPQooAmw%2BwZq8k2Kcd3aNLfwpTG4Wf76G8A%3D" "DE" "GP51457925-CALIB-01-GX010001" "DE-C4D-1S-CALIB-FIELD14SOY-GX010064" 20 10


