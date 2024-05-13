#!/usr/bin/bash
FPATHS=$1
cat $FPATHS | parallel --eta --joblog $FPATHS.joblog -N 1 -j 100 \
  "srun --quiet --nodes=1 --cpus-per-task=128 --account=project_465000498 --partition=standard  --time=0-07:00:00 stage2local.sh {} {//} 250 &>$FPATHS.{#}.out"
