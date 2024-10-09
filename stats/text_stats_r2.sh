GZ_DIR=$1
STATS_DIR=$2
NJOBS=$3

mkdir $STATS_DIR
find $GZ_DIR -name 'text.*'|parallel --joblog $STATS_DIR/text_stats.log --eta --jobs=$NJOBS 'python mrstats_r2_stage2out.py map t {} {//}/lang.zst --collection="$(basename $(dirname {//}))" ' > $STATS_DIR/text_stats.csv
#python reduce_stats.py $STATS_DIR
#python plot_lang_stats.py $STATS_DIR
