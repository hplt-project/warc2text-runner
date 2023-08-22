GZ_DIR=$1
STATS_DIR=$2
NJOBS=$3

mkdir -p $STATS_DIR
echo "path text_newlines text_wcwords text_chars text_bytes" >$STATS_DIR/text_stats.csv
find -L $GZ_DIR -name 'scored*.zst'|parallel --joblog $STATS_DIR/text_stats.log --eta --jobs=$NJOBS "echo {}|tr '\n' ' '; zstdcat {}|jq -r .text|wc --lines --words --chars --bytes" >>$STATS_DIR/text_stats.csv
echo "path docs" >$STATS_DIR/doc_stats.csv
find -L $GZ_DIR -name 'scored*.zst'|parallel --joblog $STATS_DIR/doc_stats.log --eta --jobs=$NJOBS "echo {}|tr '\n' ' '; zstdcat {}|wc --lines" >>STATS_DIR/doc_stats.csv
python reduce_stats.py $STATS_DIR
python plot_lang_stats.py $STATS_DIR
