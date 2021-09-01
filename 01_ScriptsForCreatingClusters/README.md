# FILES USED FOR CREATING CLUSTERS AND CLUSTERED POINT CLOUDS 

## RunBundler.sh 
Default RunBundler.sh from bundler_sfm library (changes made are only the focal length TODO - focal length conversion depending on the requirement) 

## SelectUndistort.py 
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

## create_clusters.bash
Copy to directory of extracted images from SelectUndistort 
usage
./create_clusters.bash ~/path/to/clusters/ <CLUSTER_SIZE>

Fixed:  ./create_clusters.bash ~/path/to/clusters/ ~/path/to/clusters/ <CLUSTER_SIZE>


## run_bundler_clustering_files.sh 
Run from anywhere 
usage 
./run_bundler_clustering_files.sh <root/dir/of/clusters> <CLUSTER_SIZE> 


## createSegMaps.py 
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

## run_createSegs.sh
Run from anywhere 
usage 
./run_createSegs.sh <root/dir/of/clusters/CLUSTER_SIZE> 

# Calibration files and initial focal lenght

For running the SfM-Bundler you should be sure you have the calibration file (npz) of your camera. Take a look in this list. https://docs.google.com/spreadsheets/d/1NdrbOobBGW19_rdzE55aWZ0WH0yAbd0cyEQQgXfmc_c/edit?usp=sharing

With npz file you are able to calculate initial focal lenght, using this script.

Try to find your State in this script, if this file or state is not there please add this such as another case in this script. 

# General Process to Create Clustered point clouds. (Manually)
0. Be sure you have all calibration files in this path /home/azureuser/SfM_Core/calibration.

1. Select the npz file related with the first code of the video. 
    See this spreadsheet: https://docs.google.com/spreadsheets/d/1NdrbOobBGW19_rdzE55aWZ0WH0yAbd0cyEQQgXfmc_c/edit?usp=sharing

2. Download the video using sudo azcopy copy as follow:

    sudo azcopy copy "https://weedsmedia.blob.core.usgovcloudapi.net/weeds3d/calibration_files/GP51471258-CALIB-01-GX010002.mp4?sv=2019-12-12&st=2021-06-04T18%3A21%3A44Z&se=2021-06-05T18%3A21%3A44Z&sr=b&sp=r&sig=oEFRAy5LHzBMnT64r0tw5twIhhHarrEonF1IB5L5RCY%3D" "/home/azureuser/data/videos/GP51471258-CALI-01-GX010002/GP51471258-CALI-01-GX010002.mp4" --recursive
    
3. Move to /home/azureuser/scripts/Weeds3D-APP-VM/01_ScriptsForCreatingClusters/
    
4. Select the proper environment: source ~/.venv/python3-cv/bin/activate

5. Run SelectUndistort.py on the proper video with proper arguments. 

python3 SelectUndistort.py -fname "/home/azureuser/data/videos/GP51471258-CALI-01-GX010002.mp4" -dst "/home/azureuser/data/videos/GP51471258-CALI-01-GX010002" -calib /home/azureuser/SfM_Core/calibration/GP51471258-CALI-01-GX010002.npz -imwidth IMGWIDTH -imgap IMAGEGAP

Note: Be sure the -dst opction has a proper folder there.

If you have doubts please use python3 SelectUndistort.py [-h]

6. copy create_cluster.bash into the same destination folder of the step 5.

sudo ./create_clusters.bash /home/azureuser/data/cool-calibrators/DE-CD1-14A1-1-CALIB-CD1-14A1-1-GX010023/clustering /home/azureuser/data/cool-calibrators/DE-CD1-14A1-1-CALIB-CD1-14A1-1-GX010023/  20

XXXXXX. source /etc/bash.bashrc
XXXXXX. sudo ldconfig
XXXXXX. sudo rm -rf l*.* m*.* n*.* o*.* p*.* s*.* c*.* *.gz bundle pmvs
XXXXXX. sudo bash RunBundler.sh /home/azureuser/calibration_files/GP51471258-CALIB-01-GX010002.txt




7. Run from anywhere usage time ./run_bundler_clustering_files.sh <root/dir/of/clusters> <CLUSTER_SIZE>. CLUSTER_SIZE will be 40
Example - sudo ./run_bundler_clustering_files.sh /home/azureuser/data/cool-calibrators/DE-CD1-14A1-1-CALIB-CD1-14A1-1-GX010023/clustering 20 

To time the cluster creation use this "{ time  ./run_bundler_clustering_files.sh <path/to/clusters> <cluster_size> ; } 2> ~/logs/'print($1$f)';"  
Example - sudo { time ./run_bundler_clustering_files.sh /home/azureuser/data/cool-calibrators/DE-CD1-14A1-1-CALIB-CD1-14A1-1-GX010023/clustering 20 ; } 2> ~/logs/DE-CD1-14A1-1-CALIB-CD1-14A1-1-GX010023_20.log;

8. Select the proper environment: source ~/.venv/tf_1/bin/activate
  
9. run createSegMaps.py with proper arguments to create segmentation maps for clustered point clouds. 
  Example - createSegMaps.py -isize 3840 -ipath /home/azureuser/data/cool-calibrators/DE-CD1-14A1-1-CALIB-CD1-14A1-1-GX010023/clustering20 -opath /home/azureuser/data/cool-calibrators/DE-CD1-14A1-1-CALIB-CD1-14A1-1-GX010023/clustering20 -model /home/azureuser/segmentation/deeplabv3+/3_class_mobilenet_v3_small_small_v2.1/ 3_class_model_mobilenet_v3_small_v2.1_1080x1920.pb


