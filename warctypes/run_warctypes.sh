WARCDIR=$1
SAMPLESIZE=$2
OUTDIR=$3

mkdir -p $OUTDIR

find $WARCDIR -name "*.warc.gz" |sort -R|head -${SAMPLESIZE}|parallel --joblog $OUTDIR/joblog --eta --verbose "./warcrectypes.sh {} | python ./warcrectypes.py contenttypes \'-\' ${OUTDIR}/{#}_contenttypes.tsv && ./warcrectypes.sh {} | python ./warcrectypes.py rectypes \'-\' ${OUTDIR}/{#}_rectypes.tsv"
python summarize_warctypes.py $OUTDIR