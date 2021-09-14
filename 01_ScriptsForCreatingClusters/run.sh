#!/bin/bash
#
# run.sh

# Script(s) made by Paula Ramos pjramg@gmail.com https://www.linkedin.com/in/paula-ramos-41097319/

#innputs:
#1: SAS token of the mp4 file
#2: State
#3: Calib file
#4: name of the frames folder

#sudo run.sh https://weedsmedia.blob.core.usgovcloudapi.net/weeds3d/DE-C3D-1-CALIB-DE-C3D-1-GX010029.MP4?sv=2019-12-12&st=2021-09-08T18%3A47%3A01Z&se=2021-10-09T18%3A47%3A00Z&sr=b&sp=r&sig=gbcF4xCd%2BZlU7utefTFta1YXcqxwtFPVPO2y46kyYo4%3D DE GP51457925-CALIB-01-GX010001 DE-C3D-1-CALIB-DE-C3D-1-GX010029
#sudo run.sh https://weedsmedia.blob.core.usgovcloudapi.net/weeds3d/DE-C4D-1S-CALIB-FIELD14SOY-GX010064.MP4?sv=2019-12-12&st=2021-09-08T20%3A36%3A58Z&se=2021-10-09T20%3A36%3A00Z&sr=b&sp=r&sig=Xkq6phKbLPQooAmw%2BwZq8k2Kcd3aNLfwpTG4Wf76G8A%3D DE GP51457925-CALIB-01-GX010001 d/DE-C4D-1S-CALIB-FIELD14SOY-GX010064


SAS=$1
STATE=$2
CALIB=$3
VIDEOFILE=$4
CLUSTERSIZE=$5
SUBSAMPLE=$6

#SAS example
#https://weedsmedia.blob.core.usgovcloudapi.net/weeds3d/DE-C3D-1-CALIB-DE-C3D-1-GX010029.MP4?sv=2019-12-12&st=2021-09-08T18%3A47%3A01Z&se=2021-10-09T18%3A47%3A00Z&sr=b&sp=r&sig=gbcF4xCd%2BZlU7utefTFta1YXcqxwtFPVPO2y46kyYo4%3D" "/home/azureuser/data/videos/DE/DE-C3D-1-CALIB-DE-C3D-1-GX010029.mp4"

#Copy the mp4 to the VM
sudo azcopy copy "${SAS}" "/home/azureuser/data/videos/${STATE}/${VIDEOFILE}.mp4" 

#Go to the active folder
cd /home/azureuser/data/videos/${STATE}

#Active the environment for CV and python 3
source ~/.venv/python3-cv/bin/activate

mkdir ${VIDEOFILE}

#Split the video into frames
sudo python3 /home/azureuser/scripts/Weeds3D-APP-VM/01_ScriptsForCreatingClusters/SelectUndistort.py -fname "/home/azureuser/data/videos/${STATE}/${VIDEOFILE}.mp4" -dst "/home/azureuser/data/videos/${STATE}/${VIDEOFILE}" -calib "/home/azureuser/calibration_files/${CALIB}.npz" -imgap ${SUBSAMPLE}

#Change environment
source /etc/bash.bashrc
sudo ldconfig

#Copy create_clusters.bash into the active folder (where the frames are)
cp /home/azureuser/scripts/Weeds3D-APP-VM/01_ScriptsForCreatingClusters/create_clusters.bash "/home/azureuser/data/videos/${STATE}/${VIDEOFILE}"

#Go to splited frames are (same folder mentioned before)
cd /home/azureuser/data/videos/${STATE}/${VIDEOFILE}

mkdir clustering${CLUSTERSIZE}

#Create the clusters: number of images per cluster is another input.
sudo bash create_clusters.bash "/home/azureuser/data/videos/${STATE}/${VIDEOFILE}/clustering" "/home/azureuser/data/videos/${STATE}/${VIDEOFILE}/" ${CLUSTERSIZE}
#sudo bash create_clusters.bash /home/azureuser/data/videos/DE/DE-C3D-1-CALIB-DE-C3D-1-GX010029/clustering /home/azureuser/data/videos/DE/DE-C3D-1-CALIB-DE-C3D-1-GX010029/ 20

#Clean storage space
sudo rm *.jpg

#Copy the parallelization script into the active folder(where the frames are)
cp /home/azureuser/scripts/Weeds3D-APP-VM/01_ScriptsForCreatingClusters/run_bundler_clustering_files.sh "/home/azureuser/data/videos/${STATE}/${VIDEOFILE}"

#Run the SfM in all clusters
sudo ./run_bundler_clustering_files.sh /home/azureuser/data/videos/${STATE}/${VIDEOFILE}/clustering  ${CLUSTERSIZE} /home/azureuser/calibration_files/${CALIB}.txt

#Copy the permissions_pmvs script into the active folder(where the frames are)
cp /home/azureuser/scripts/Weeds3D-APP-VM/01_ScriptsForCreatingClusters/permissions_pmvs.sh "/home/azureuser/data/videos/${STATE}/${VIDEOFILE}"

#Give permission for all "pmvs" subfolders in the clustering folder
sudo ./permissions_pmvs.sh /home/azureuser/data/videos/${STATE}/${VIDEOFILE}/clustering  ${CLUSTERSIZE}




