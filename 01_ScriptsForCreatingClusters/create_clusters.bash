#/usr/bin/env bash
IMAGES=($(ls *.jpg | cat))
#TARGET='/home/azureuser/SfM_Core/calibration/BALL1METER-B1-GX010173/clusters/'
#SOURCE='/home/azureuser/SfM_Core/calibration/BALL1METER-B1-GX010173/'
TARGET=$1
SOURCE=$2
CLUSTER_SIZE=$3
OVERLAP=1
idx=0
dir_num=1

#with overlap
idx=0
dir_num=1
count=0
while [ $idx -le ${#IMAGES[@]} ]
do
mkdir -p "${TARGET}${CLUSTER_SIZE}/${dir_num}"
while [ $count -lt $CLUSTER_SIZE ]
do
#printf "%s %s %d" "${SOURCE}${IMAGES[$idx]}" "${TARGET}${dir_num}/${IMAGES[$idx]}" "$idx"
cp "${SOURCE}${IMAGES[$idx]}" "${TARGET}${CLUSTER_SIZE}/${dir_num}/${IMAGES[$idx]}" 
cp -r "/home/azureuser/scripts/Weeds3D-APP-VM/01_ScriptsForCreatingClusters/RunBundler.sh" "${TARGET}${CLUSTER_SIZE}/${dir_num}/RunBundler.sh"
let "idx+=1"
let "count+=1"
done;
let "idx-=`python -c "from math import ceil; print(int(ceil($CLUSTER_SIZE/3.0)))"`"
let "count=0"
let "dir_num+=1"
done;
