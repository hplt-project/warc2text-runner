#!/usr/bin/bash
LOG=${SLURM_JOB_ID}.log

bs=$1
OUTDIR=out_${SLURM_JOB_ID}
NJOBS=250


set -euo pipefail

mkdir -p $OUTDIR
# --keep-order guarantees that GNU Parallel will collect stdout from tasks and print it to its stdout in the order
# aligned with the order of input lines
# --block issues one task per block of input lines of roughly this size, but without breaking lines;
# making it too small will increase extra costs on script initialization (e.g. weights loading for langid),
# making it too large will require buffering too much outputs in parallel due to --keep-order requirement.
for FIN in `cat ../sample_run4.1/sample0.002_bs10.paths`; do
echo file $FIN >>$LOG
echo du `du $FIN|cut -f 1` >>$LOG
echo trafbs $bs >>$LOG
time (zstdcat $FIN  \
    | parallel --halt now,fail=1 --block $bs -j $NJOBS --pipe --keep-order  \
    "python -m warc2text_runner.two.trafilatura.traf" | tee >(zstd > ${OUTDIR}/text.zst) >/dev/null) 2>>$LOG
#    | parallel --halt now,fail=1 --block $BLOCKSIZE_LID -j $NJOBS_LID --pipe --keep-order \
#        "python -m warc2text_runner.two.fastertext_lid.proto_langid" | zstd > ${OUTDIR}/lang.zst
done
