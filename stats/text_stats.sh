GZ_DIR=$1
STATS_DIR=$2
NJOBS=$3

mkdir $STATS_DIR
find $GZ_DIR -name 'url.gz'|parallel --joblog $STATS_DIR/doc_stats.log --eta --jobs=$NJOBS "echo {}|tr '\n' ' '; zcat {}|wc" > $STATS_DIR/doc_stats.csv
find $GZ_DIR -name 'text.gz'|parallel --joblog $STATS_DIR/text_stats.log --eta --jobs=$NJOBS "echo {}|tr '\n' ' '; zcat {}|base64 -d|wc" > $STATS_DIR/text_stats.csv

