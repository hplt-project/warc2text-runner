ID=$1
OUTDIR=$2
INDIR=$3
WARCS=${@:4}

FILTERDIR=$(realpath $(dirname $0)/..)
LOGDIR=${OUTDIR%/}_logs

mkdir -p $LOGDIR $OUTDIR || exit 1
cd $INDIR
echo "warc2text --robotspass ${OUTDIR}/${ID}/robotstxt -f html,metadata --jsonl --compress zstd --compress-level 9 --skip-text-extraction --classifier skip --url-filters ${FILTERDIR}/url-filter-list.optimised -o ${OUTDIR}/${ID} $WARCS 2>${LOGDIR}/${ID}.stderr" >${LOGDIR}/${ID}.stdout 
