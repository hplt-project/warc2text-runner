#!/usr/bin/bash
NJOBS=$1
FPATHS=$2
BATCH_GB=$3
OUTDIR=$4

cat $FPATHS | python -m warc2text_runner.stage2.batch_htmls $BATCH_GB | parallel --eta --joblog $FPATHS.joblog -N 1 -j $NJOBS \
  "srun --quiet --nodes=1 --time=0-48:00:00 stage2local_batch.sh $OUTDIR {} &>$FPATHS.{#}.out"
