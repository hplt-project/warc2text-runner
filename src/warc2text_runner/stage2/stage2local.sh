#!/usr/bin/bash
FIN=$1
OUTDIR=$2
NJOBS=$3

BLOCKSIZE_TRAF=30M  #  10x more parallel processes than for lid require smaller blocks;
TRAF_TIMEOUT=0.5  # timout 0.5s, should loose less than 0.5% of docs

BLOCKSIZE_LID=100M  # 0.3s-0.5s to load model, 4.4s to FastText.predict for 10k lines, 28 MB (not random sample!)

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
rclone cat $FIN | zstdcat  \
    | parallel --halt now,fail=1 --block $BLOCKSIZE_TRAF -j $NJOBS_TRAF --pipe --keep-order  \
        "python -m warc2text_runner.stage2.trafilatura.traf --timelimit_perdoc ${TRAF_TIMEOUT}" | tee >(zstd > ${OUTDIR}/text.zst) \
    | parallel --halt now,fail=1 --block $BLOCKSIZE_LID -j $NJOBS_LID --pipe --keep-order \
        "python -m warc2text_runner.stage2.fastertext_lid.proto_langid" | zstd > ${OUTDIR}/lang.zst

