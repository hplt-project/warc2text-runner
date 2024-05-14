#!/bin/bash
RPATH=$1
LPATH=$2
MAXNODES=$3

NAME=$(basename $RPATH)
FIFO=${NAME}.fifo

set -euo pipefail
mkfifo $FIFO  # create named pipe (queue); works well only within 1 node!

echo Calculating the number of files to process for the progress bar. Please wait ...
NFILES=`rclone ls $RPATH --include html.zst|wc -l`
echo In total $NFILES should be downloaded. Please start downloading.

# this will select messages about html.zst files downloaded from the pipe, form a local path to html.zst 
# and process with stage2nodeparallel
cat $FIFO | tee ${NAME}.download.log | \
        # save rclone logs to a file; a pipe cannot store anything, only transfer 
	grep  --line-buffered -E "html.zst.*Copied" | \
	# select messages about html.zst downloaded, line buffering to process immediately 
	sed --unbuffered -r 's!^.*: (.*.zst).*$!'${LPATH}'/'${NAME}'/\1!' | \
	# extract local path to downloaded html.zst, --unbuffered to process immeditely 
	parallel --eta --total-jobs $NFILES --joblog $NAME.stage2.joblog -N 1 -j $MAXNODES \
	  "srun --quiet --nodes=1 --cpus-per-task=128 --account=project_465000498 --partition=standard  --time=0-07:00:00 stage2local.sh {} {//} 250 &>$NAME.{#}.stage2.out && rm {}"

