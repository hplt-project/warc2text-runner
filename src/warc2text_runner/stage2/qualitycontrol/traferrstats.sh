GZ_DIR=$1
STATS_DIR=$2
NJOBS=$3

mkdir $STATS_DIR
find $GZ_DIR -name 'text.*'|parallel --joblog $STATS_DIR/text_stats.log --eta --jobs=$NJOBS 'python traferrstats.py map {} {//}/lang.zst --collection="$(basename $(dirname {//}))" ' > $STATS_DIR/text_stats.csv
python -m warc2text_runner.stage2.qualitycontrol.traferrstats reduce $STATS_DIR
