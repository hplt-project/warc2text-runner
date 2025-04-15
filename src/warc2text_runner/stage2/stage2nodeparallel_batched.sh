#!/usr/bin/bash
NJOBS=$1
FPATHS=$2
BATCH_GB=$3
OUTDIR=$4

filter_done() {
  while read -r line; do
    fdone=`echo $line | sed -r "s@.*lumio:(.*)/html.zst@${OUTDIR}/\1/.done@"`
    if [ ! -f "$fdone" ]; then
      echo "$line"
    else
      echo "$line already processed, skipped" 1>&2
    fi
  done
}

cat $FPATHS | filter_done | python -m warc2text_runner.stage2.batch_htmls $BATCH_GB | parallel --eta --joblog $FPATHS.joblog -N 1 -j $NJOBS \
  "{ stage2stagelumio.sh $OUTDIR {} && \
   srun --quiet --nodes=1 --cpus-per-task=128 --time=0-48:00:00 stage2local_batch.sh $OUTDIR {= s@lumio:@${OUTDIR}/@g =}; } &>$FPATHS.{#}.out"
