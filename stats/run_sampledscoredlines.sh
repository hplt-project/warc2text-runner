ZST_DIR=$1
RES_DIR=$2
TARGET_NUMLINES=$3
NJOBS=$4
STAT_DIR=$5

for langdir in $ZST_DIR/*; do  
    lang=$(basename $langdir)
    PROB=`$(dirname $0)/get_sample_prob.sh $lang $TARGET_NUMLINES $STAT_DIR || echo 0.0001`
    bash $(dirname $0)/samplescoredlines.sh $langdir $RES_DIR/$lang $NJOBS $PROB
done
