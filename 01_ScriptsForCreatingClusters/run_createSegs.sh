#!/bin/bash 
inputpaths=$(find $1/ -mindepth 1 -maxdepth 1 -type d)
for ipath in $inputpaths
do
source ~/.venv/tf_1/bin/activate
(python /home/azureuser/scripts/Weeds3D-APP-VM/01_ScriptsForCreatingClusters/createSegMaps.py -ipath $ipath -opath $ipath) & 
done
wait
