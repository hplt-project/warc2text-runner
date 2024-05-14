#!/bin/bash
RPATH=$1
LPATH=$2
NJOBS=$3

NAME=$(basename $RPATH)
FIFO=${NAME}.fifo

set -euo pipefail
mkfifo $FIFO  # create named pipe (queue); works well only within 1 node!

# this will select messages about html.zst files downloaded from the pipe, form a local path to html.zst 
# and process with stage2nodeparallel
echo Calculating the number of files to process. Please wait ...
NFILES=`rclone ls nird-c:/nird/home/nikolare/hplt/two/html/archivebot_partial --include html.zst|wc -l`
echo In total $NFILES should be downloaded. Please start downloading.
cat $FIFO | parallel --eta --total-jobs $NFILES -j2 "sleep 20; echo {}" 
