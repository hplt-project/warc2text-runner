LANG=$1
TARGET_NUMLINES=$2
STAT_DIR=$3

NUM_LINES=`grep "^$LANG" $STAT_DIR/stats.tsv |cut -f 2`
#echo $NUM_LINES
python -c "print($TARGET_NUMLINES / $NUM_LINES)"
