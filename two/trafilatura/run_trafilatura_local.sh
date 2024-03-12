FIN=$1
OUTDIR=$2
NJOBS=$3
BLOCKSIZE=100M

mkdir -p $OUTDIR
zstdcat $FIN |parallel --block $BLOCKSIZE -j $NJOBS --joblog ${OUTDIR}/joblog --pipe --keep-order  "python traf.py 2>${OUTDIR}/{#}.stderr"|zstd -o ${OUTDIR}/text.zst
