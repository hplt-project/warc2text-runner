FIN=$1
OUTDIR=$2
NJOBS=$3
BLOCKSIZE=10M

module purge
module load LUMI/23.09 cray-python parallel/20231022

mkdir -p $OUTDIR
zstdcat $FIN |parallel --block $BLOCKSIZE -j $NJOBS --joblog ${OUTDIR}/joblog --pipe --keep-order  "python traf.py" | zstd > ${OUTDIR}/text.zst

