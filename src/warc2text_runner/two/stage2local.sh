#!/usr/bin/bash
FIN=$1
OUTDIR=$2
NJOBS=$3
BLOCKSIZE=10M  # TODO: think about increasing, esp. for langid which will load the model once per BLOCKSIZE of inputs!

NJOBS_LID=$(($NJOBS/10 + 1))
NJOBS_TRAF=$(($NJOBS - $NJOBS_LID))
#echo Running lid in $NJOBS_LID and trafilatura in $NJOBS_TRAF processes

set -euo pipefail

mkdir -p $OUTDIR
# --keep-order guarantees that GNU Parallel will collect stdout from tasks and print it to its stdout in the order
# aligned with the order of input lines
# --block issues one task per block of input lines of roughly this size, but without breaking lines;
# making it too small will increase extra costs on script initialization (e.g. weights loading for langid),
# making it too large will require buffering too much outputs in parallel due to --keep-order requirement.
zstdcat $FIN  \
    | parallel --halt now,fail=1 --block $BLOCKSIZE -j $NJOBS_TRAF --pipe --keep-order  \
        "python -m warc2text_runner.two.trafilatura.traf" | tee >(zstd > ${OUTDIR}/text.zst) \
    | parallel --halt now,fail=1 --block $BLOCKSIZE -j $NJOBS_LID --pipe --keep-order \
        "python -m warc2text_runner.two.fastertext_lid.proto_langid" | zstd > ${OUTDIR}/lang.zst

