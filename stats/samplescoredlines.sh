ZST_DIR=$1
RES_DIR=$2
NJOBS=$3
PROB=$4

mkdir -p $RES_DIR
find -L $ZST_DIR -name '*.zst'|parallel --joblog $RES_DIR/joblog --eta --jobs=$NJOBS --line-buffer "zstdcat {} | perl -ne 'print if (rand() < '$PROB')' | bash $(dirname $0)/jsonl2scoredlines.sh" > $RES_DIR/scoredsample.tsv

