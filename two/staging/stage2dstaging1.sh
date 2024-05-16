#!/bin/bash
MAXNODES=$1
LPATH='/scratch/project_465000498/two/html_staging/'

NAME=`hostname`
FIFO=~/`hostname`.fifo

mkfifo $FIFO  # create named pipe (queue); works well only within 1 node!

set -euo pipefail

# this will select messages about html.zst files downloaded from the pipe, form a local path to html.zst 
# and process with stage2nodeparallel
cat $FIFO | tee -a ${NAME}.download.log | \
        # save rclone logs to a file; a pipe cannot store anything, only transfer ; append to the existing logs in order to make this script restartable
	grep  --line-buffered -E "html.zst.*Copied" | \
	# select messages about html.zst downloaded, line buffering to process immediately 
	sed --unbuffered -r 's!^.*: (.*.zst).*$!'${LPATH}'/\1!' | \
	# extract local path to downloaded html.zst, --unbuffered to process immeditely 
	parallel --eta --total-jobs 0 --joblog $NAME.stage2.joblog -N 1 -j $MAXNODES \
	  "srun --quiet --nodes=1 --cpus-per-task=128 --account=project_465000498 --partition=standard  --time=0-07:00:00 stage2local.sh {} {//} 250 &>$NAME.{#}.stage2.out && rm {}"

