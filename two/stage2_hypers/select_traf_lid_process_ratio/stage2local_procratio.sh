#!/usr/bin/bash
FIN=$1
OUTDIR=out_${SLURM_JOB_ID}
NJOBS=$2

LOG=${SLURM_JOB_ID}.log

BLOCKSIZE_TRAF=30M  #  10x more parallel processes than for lid require smaller blocks;
TRAF_TIMEOUT=0.5  # timout 0.5s, should loose less than 0.5% of docs

BLOCKSIZE_LID=100M  # 0.3s-0.5s to load model, 4.4s to FastText.predict for 10k lines, 28 MB (not random sample!)


set -euo pipefail

mkdir -p $OUTDIR
# --keep-order guarantees that GNU Parallel will collect stdout from tasks and print it to its stdout in the order
# aligned with the order of input lines
# --block issues one task per block of input lines of roughly this size, but without breaking lines;
# making it too small will increase extra costs on script initialization (e.g. weights loading for langid),
# making it too large will require buffering too much outputs in parallel due to --keep-order requirement.

echo file $FIN >>$LOG
echo du `du $FIN|cut -f 1`  >>$LOG
echo trafbs $BLOCKSIZE_TRAF  >>$LOG
echo lidbs $BLOCKSIZE_LID >>$LOG

time (zstdcat $FIN | parallel --halt now,fail=1 --block $BLOCKSIZE_TRAF -j $NJOBS --pipe --keep-order "python -m warc2text_runner.two.trafilatura.traf --timelimit_perdoc ${TRAF_TIMEOUT}"  | zstd > ${OUTDIR}/text.zst ) 2>>$LOG

time (zstdcat ${OUTDIR}/text.zst | parallel --halt now,fail=1 --block $BLOCKSIZE_LID -j $NJOBS --pipe --keep-order \
	"python -m warc2text_runner.two.fastertext_lid.proto_langid" | zstd > ${OUTDIR}/lang.zst ) 2>>$LOG

