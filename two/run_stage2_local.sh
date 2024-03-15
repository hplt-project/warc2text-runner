#!/usr/bin/bash
FIN=$1
OUTDIR=$2
NJOBS=$3
BLOCKSIZE=10M

NJOBS_LID=$(($NJOBS/10 + 1))
NJOBS_TRAF=$(($NJOBS - $NJOBS_LID))
#echo Running lid in $NJOBS_LID and trafilatura in $NJOBS_TRAF processes

set -euo pipefail

module --quiet purge
module load LUMI/23.09 cray-python parallel/20231022

mkdir -p $OUTDIR
zstdcat $FIN  | parallel --halt now,fail=1 --block $BLOCKSIZE -j $NJOBS_TRAF --pipe --keep-order  "python trafilatura/traf.py" | tee >(zstd > ${OUTDIR}/text.zst) | parallel --halt now,fail=1 --block $BLOCKSIZE -j $NJOBS_LID --pipe --keep-order "python fastertext_lid/proto_langid.py" | zstd > ${OUTDIR}/lang.zst

