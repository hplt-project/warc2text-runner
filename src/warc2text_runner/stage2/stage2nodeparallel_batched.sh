#!/usr/bin/bash
NJOBS=$1
FPATHS=$2
BATCH_GB=$3
OUTDIR=$4

LOGDIR=logs_$(date +%Y-%m-%d-%H-%M-%S)
mkdir $LOGDIR

filter_done() {
  while read -r line; do
    fdone=`echo $line | sed -r "s@[0-9]+ +[^:]+:(.*)/html.zst@${OUTDIR}/\1/.done@"`
    if [ ! -f "$fdone" ]; then
      echo "$line"
    else
      echo "$line already processed, skipped" 1>&2
    fi
  done
}

cat $FPATHS | filter_done | python -m warc2text_runner.stage2.batch_htmls_prtpy $BATCH_GB | parallel --eta --joblog $LOGDIR/joblog -N 1 -j $NJOBS \
  "srun --quiet --colsep ' ' --nodes=1 --cpus-per-task=128 stage2local_batch.sh $OUTDIR {} &>$LOGDIR/{#}.out"
