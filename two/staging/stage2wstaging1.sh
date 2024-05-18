#!/bin/bash
DATACENTER=$1
FPATHS=$2
LPATH=$3
MAXNODES=$4

LOGDIR=${DATACENTER}_logs
mkdir -p $LOGDIR

FIFO=${LOGDIR}/.fifo
mkfifo $FIFO  # create named pipe (queue); works well only within 1 node!

set -euo pipefail
echo Calculating the number of files to process for the progress bar. Please wait ...
NFILES=`grep html.zst $FPATHS | wc -l`
echo $NFILES html.zst files are expected to be downloaded and processed in total. Please start downloading.

# this will select messages about html.zst files downloaded from the pipe, form a local path to html.zst 
# and process with stage2nodeparallel
cat $FIFO | \
        # save rclone logs to a file; a pipe cannot store anything, only transfer ; append to the existing logs in order to make this script restartable
	grep  --line-buffered -E "html.zst.*Copied" | \
	# select messages about html.zst downloaded, line buffering to process immediately 
	sed --unbuffered -r 's!^.*: (.*.zst).*$!'${LPATH}'/\1!' | \
	# extract local path to downloaded html.zst, --unbuffered to process immeditely 
	parallel --eta --total-jobs $NFILES --joblog ${LOGDIR}/stage2.joblog -N 1 -j $MAXNODES \
	  "srun --quiet --nodes=1 --cpus-per-task=128 --account=project_465000498 --partition=standard  --time=0-07:00:00 stage2local.sh {} {//} 250 &>${LOGDIR}/{#}.stage2.out "

