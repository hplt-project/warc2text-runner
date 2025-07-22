#!/bin/sh
# Statistics for Releases 2 and 3, after deduplication or cleaning
GZ_DIR=$1
STATS_DIR=$2
NJOBS=$3

mkdir $STATS_DIR
find $GZ_DIR -name '*.jsonl.zst'|parallel --joblog $STATS_DIR/text_stats.log --eta --jobs=$NJOBS 'python mrstats.py map {}' > $STATS_DIR/text_stats.csv
python mrstats.py reduce $STATS_DIR
