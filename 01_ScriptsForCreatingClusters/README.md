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

# General Process to Create Clustered point clouds. (Manually)
1. Run SelectUndistort.py on the proper video with proper arguments. 
2. Run create_clusters.bash from within the folder with extracted undistorted frames (you might need to copy the script there) 
3. run run_bundler_clustering_files.sh with proper arguments. 
To time the cluster creation use this{ time  ./run_bundler_clustering_files.sh <path/to/clusters> <cluster_size> ; } 2> <logfile>;  
4. run createSegMaps.py with proper arguments to create segmentation maps for clustered point clouds. 
