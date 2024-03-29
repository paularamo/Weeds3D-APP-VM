#!/bin/bash
#
# RunBundler.sh
#   copyright (c) 2008-2013 Noah Snavely
#
# A script for preparing a set of image for use with the Bundler 
# structure-from-motion system.
#
# Usage: RunBundler.sh [config_file]
#
# config_file describes [optional] configuration options, including:
#
#   IMAGE_LIST=<list.txt> # file with input list of images / focal lengths
#   IMAGE_DIR=<dir> # directory containing the images you'd like to process
#   MATCH_WINDOW_RADIUS=<num> # only match images in a sliding 
#                             # window of size 2rad+1 
#   INIT_FOCAL=<num>   # value to use for initial focal length
#   FOCAL_WEIGHT=<num> # weight used to constrain focal length
#   TRUST_FOCAL=true   # tell bundler to trust the provided focal lengths
#   RAY_ANGLE_THRESHOLD=<num> # used to remove ill-conditioned points
#   USE_CERES=true # enables use of Ceres solver for bundle adjustment
#                  # (if this is enabled at compile time)
#   NUM_MATCHES_ADD_CAMERA=<num> # number of matches above which bundler
#                                # will definitely attempt to add a camera
#                                # (e.g., you might use 500)
#

start=$SECONDS

TARGET=$1

#Modificar el PATH donde estan la libreria bundler_sfm
BASE_PATH=/home/azureuser/libraries/bundler_sfm

if [ "$BASE_PATH" = "" ]
then
    echo "Especificar en (RunBundler.sh) la ruta de ejecutables de bundler_sfm.";
    exit;
fi

# Ejecutable para leer la distancia focal
EXTRACT_FOCAL=$BASE_PATH/bin/extract_focal2.pl

OS=`uname -o`

if [ $OS = "Cygwin" ]
then
    MATCHKEYS=$BASE_PATH/bin/KeyMatchFull.exe
    BUNDLER=$BASE_PATH/bin/Bundler.exe
else
    MATCHKEYS=$BASE_PATH/bin/KeyMatchFull
    BUNDLER=$BASE_PATH/bin/bundler
fi

TO_SIFT=$BASE_PATH/bin/ToSift.sh
TO_SIFT_LIST=$BASE_PATH/bin/ToSiftList.sh


# Default config options
IMAGE_DIR="."
MATCH_WINDOW_RADIUS="-1"  # infinite window
FOCAL_WEIGHT="0.0001"
RAY_ANGLE_THRESHOLD="2.0"

# Establecer la distancia focal.
#INIT_FOCAL="1626.7"

filename="${TARGET}"
INIT_FOCAL=$(cat "$filename")


# Read any user-provided config options
if [ $# -eq 1 ]
then
    echo "Using config file '$1'"
    source $1
else
    echo "Using default config options"
fi

if [ "$IMAGE_LIST" = "" ]
then
  # Prepare the list of images

  # Rename ".JPG" to ".jpg"
  for d in `ls -1 $IMAGE_DIR | egrep ".JPG$"`
  do 
      mv $IMAGE_DIR/$d $IMAGE_DIR/`echo $d | sed 's/\.JPG/\.jpg/'`
  done

  # Create the list of images
  find $IMAGE_DIR -maxdepth 1 | egrep ".jpg$" | sort > list_tmp.txt

  if [ "$INIT_FOCAL" = "" ]
  then
    # Extract focal lengths using Exif data
    $EXTRACT_FOCAL list_tmp.txt || exit 1
    cp prepare/list.txt .
  else
    # Use the provided focal length
    awk "{print \$1, 0, $INIT_FOCAL}" list_tmp.txt > list.txt
  fi

  IMAGE_LIST=list.txt
fi

# Run the ToSift script to generate a list of SIFT commands
echo "[- Extracting keypoints -]"
rm -f sift.txt
$TO_SIFT_LIST $IMAGE_LIST > sift.txt || exit 1

# Execute the SIFT commands
sudo sh sift.txt

# Match images (can take a while)
echo "[- Matching keypoints (this can take a while) -]"
awk '{print $1}' $IMAGE_LIST | sed 's/\.jpg$/\.key/' > list_keys.txt
sleep 1
echo $MATCHKEYS list_keys.txt matches.init.txt $MATCH_WINDOW_RADIUS
$MATCHKEYS list_keys.txt matches.init.txt $MATCH_WINDOW_RADIUS

# Generate the options file for running bundler 
mkdir -p bundle
rm -f options.txt

echo "--match_table matches.init.txt" >> options.txt
echo "--output bundle.out" >> options.txt
echo "--output_all bundle_" >> options.txt
echo "--output_dir bundle" >> options.txt
echo "--variable_focal_length" >> options.txt
echo "--use_focal_estimate" >> options.txt
echo "--constrain_focal" >> options.txt
echo "--constrain_focal_weight $FOCAL_WEIGHT" >> options.txt

if [ "$TRUST_FOCAL" != "" ]
then
    echo "--trust_focal" >> options.txt
fi

echo "--estimate_distortion" >> options.txt
echo "--ray_angle_threshold $RAY_ANGLE_THRESHOLD" >> options.txt

if [ "$NUM_MATCHES_ADD_CAMERA" != "" ]
then
    echo "--num_matches_add_camera $NUM_MATCHES_ADD_CAMERA" >> options.txt
fi

if [ "$USE_CERES" != "" ]
then
    echo "--use_ceres" >> options.txt
fi

echo "--run_bundle" >> options.txt

# Run Bundler!
echo "[- Running Bundler -]"
rm -f constraints.txt
rm -f pairwise_scores.txt
$BUNDLER $IMAGE_LIST --options_file options.txt > bundle/bundle.log

echo "[- Done -]"

echo "--run_PMVS" 

Bundle2PMVS=$BASE_PATH/bin/Bundle2PMVS 

$Bundle2PMVS list.txt bundle/bundle.out

sh pmvs/prep_pmvs.sh

PMVS2=/home/azureuser/libraries/pmvs-2/program/main/pmvs2

$PMVS2 pmvs/ pmvs_options.txt

echo "[- Done -]"

echo "Running time $(( SECONDS - start ))"


