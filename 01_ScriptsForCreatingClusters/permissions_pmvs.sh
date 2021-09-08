#!/bin/bash
pmvs_folder=$(find $1$2/ -name pmvs)
for f in $pmvs_folder
do
cd
(cd "$(dirname $f)"; sudo chmod 775 pmvs) &
done
wait

