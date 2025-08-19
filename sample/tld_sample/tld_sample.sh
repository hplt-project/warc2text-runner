#!/bin/bash
set -euo pipefail

stream_file(){
  local FIN=$1
  set -euo pipefail
  #echo "Streaming $FIN" 1>&2
  if [[ $FIN =~ ^s3: ]]; then
    s3cmd get $FIN -
  else
    rclone cat $FIN
  fi
}

stream_tlds(){
  local FIN=${1}/metadata.zst
  set -euo pipefail
  stream_file $FIN | zstdcat | jq -cr .u | perl -MURI -ne '$u = URI->new($_); @h = split /\./, $u->host; print $h[-1],"\n"' | jq -Rc '{"tld":.}'
}

tld_stats2(){
  set -euo pipefail
  local DIN=${1}
  #echo "tld_stats2 $DIN" 1>&2
  stream_tlds ${1} | jq -c '{ "text":"", "collection":.tld}' | python ../../stats/mrstats.py --lang=$(basename $(dirname $(dirname $DIN/f))) map -
}

export -f stream_file
export -f stream_tlds
export -f tld_stats2


TASKDIR=$1
NJOBS=$2

STATS_DIR=$TASKDIR/stats
mkdir -p $STATS_DIR
#time cat $TASKDIR/paths | parallel --joblog $STATS_DIR/tld_stats.joblog --eta --jobs=$NJOBS "tld_stats2 {//}" > $STATS_DIR/text_stats.csv
#time python ../../stats/mrstats.py reduce $STATS_DIR

sample(){
  set -euo pipefail
  stream_tlds $2 | python paste_sample_weighted.py 15000000 $1 -strat_field tld - $2/metadata.zst $2/html.zst -- --separator='@' | zstd >$3
}
export -f sample

SAMPLE_DIR=$TASKDIR/sample
TMPDIR=$TASKDIR/tmp
mkdir -p $SAMPLE_DIR $TMPDIR

time cat $TASKDIR/paths | parallel --resume-failed --line-buffer --joblog $SAMPLE_DIR/sample.joblog --eta --jobs=$NJOBS "sample $TASKDIR/tld_weights.tsv {//} $TMPDIR/sample_{#}.zst 2>$TMPDIR/{#}.err"

