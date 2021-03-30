#!/bin/bash 
bundler_files=$(find $1/$2/ -name RunBundler.sh)
for f in $bundler_files
do
cd 
source /etc/bash.bashrc
(cd "$(dirname $f)"; nohup ./RunBundler.sh) & 
done
wait
