#!/bin/sh
# Statistics for Release 2, just after stage2 (WP2)
GZ_DIR=$1
STATS_DIR=$2
NJOBS=$3

mkdir -p $STATS_DIR
find -L $GZ_DIR -name 'text.*'|parallel --resume-failed --joblog $STATS_DIR/text_stats.log --eta --jobs=$NJOBS 'python mrstats.py map {} {//}/lang.zst --collection="$(basename $(dirname {//}))" ' > $STATS_DIR/text_stats.csv
python mrstats.py reduce $STATS_DIR
