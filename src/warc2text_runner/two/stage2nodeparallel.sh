#!/usr/bin/bash
# Runs stage2 in parallel on $1 nodes for a list of html.zst files listed in the file $2.  If $2 is empty, reads from stdin.
# 1 input file = 1 job occupies a whole node, different lines (HTMLs) are processed in parallel.
# Logs to $2.joblog (.joblog if $2 is empty). stdout/stderr for each job is written to $FPATH.<JOBID>.out
# For efficient utilization of the node, the uncompressed file size should be much larger than 250 * 30 MB = 7.5 GB

NJOBS=$1
FPATHS=$2
cat $FPATHS | parallel --eta --joblog $FPATHS.joblog -N 1 -j $NJOBS \
  "srun --quiet --nodes=1 --cpus-per-task=128 --account=project_465000498 --partition=standard  --time=0-23:00:00 stage2local_batch.sh {} &>$FPATHS.{#}.out"
