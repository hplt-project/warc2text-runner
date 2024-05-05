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
# --keep-order guarantees that GNU Parallel will collect stdout from tasks and print it to its stdout in the order
# aligned with the order of input lines
# --block issues one task per block of input lines of roughly this size, but without breaking lines
zstdcat $FIN  \
    | parallel --halt now,fail=1 --block $BLOCKSIZE -j $NJOBS_TRAF --pipe --keep-order  \
        "python -m warc2text_runner.two.trafilatura.traf" | tee >(zstd > ${OUTDIR}/text.zst) \
    | parallel --halt now,fail=1 --block $BLOCKSIZE -j $NJOBS_LID --pipe --keep-order \
        "python -m warc2text_runner.two.fastertext_lid.proto_langid" | zstd > ${OUTDIR}/lang.zst

