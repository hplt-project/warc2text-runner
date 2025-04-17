#!/usr/bin/bash
FIN=$1
OUTDIR=$2
NJOBS=`nproc --all`

BLOCKSIZE_TRAF=30M  #  more parallel processes than for lid require smaller blocks;
TRAF_TIMEOUT=10  # timeout 10s, increased from 0.5s to compensate for adding xml extraction for the 3rd iteration and hopefully get more long good texts

BLOCKSIZE_LID=100M  # 0.3s-0.5s to load model, 4.4s to FastText.predict for 10k lines, 28 MB (not random sample!)

NJOBS=$(($NJOBS - 8))  # leave some threads for rclone, zstdcat, zstd steps in the pipeline
NJOBS_LID=$(($NJOBS/10 + 1))
NJOBS_TRAF=$(($NJOBS - $NJOBS_LID))

set -euo pipefail

mkdir -p $OUTDIR

S3FIN=`echo $FIN | sed 's@lumio:@s3://@'`
s3cmd get `echo $S3FIN | sed 's@html.zst@metadata.zst@'` ${OUTDIR}/ --continue  # continue downloading in case it failed last time

# --keep-order guarantees that GNU Parallel will collect stdout from tasks and print it to its stdout in the order
# aligned with the order of input lines
# --block issues one task per block of input lines of roughly this size, but without breaking lines;
# making it too small will increase extra costs on script initialization (e.g. weights loading for langid),
# making it too large will require buffering too much outputs in parallel due to --keep-order requirement.
echo Running lid in $NJOBS_LID and trafilatura in $NJOBS_TRAF processes

# rclone occasionally crashes with EOF error when streaming some files from lumio (<1% for bs=10, ~50% for bs=1000)...
# s3cmd shows warnings about EOF for these files, but retries with success
#rclone cat $FIN | zstdcat  \
s3cmd get $S3FIN - | zstdcat  \
    | parallel --halt now,fail=1 --block $BLOCKSIZE_TRAF -j $NJOBS_TRAF --pipe --keep-order  \
        "python -m warc2text_runner.stage2.trafilatura.traf --timelimit_perdoc ${TRAF_TIMEOUT}" | tee >(zstd > ${OUTDIR}/text.zst) \
    | parallel --halt now,fail=1 --block $BLOCKSIZE_LID -j $NJOBS_LID --pipe --keep-order \
        "python -m warc2text_runner.stage2.fastertext_lid.proto_langid" | zstd > ${OUTDIR}/lang.zst

# check the number of lines
C=`paste <(zstdcat ${OUTDIR}/text.zst|wc -l) <(zstdcat ${OUTDIR}/lang.zst|wc -l) <(zstdcat ${OUTDIR}/metadata.zst|wc -l)`
read t l m  <<< "$C"
if [ "$t" != "$m" ]; then
  echo "ERROR: Number of lines mismatch: $t in ${OUTDIR}/text.zst and $m in ${OUTDIR}/metadata.zst"
  exit 1
fi

if [ "$l" != "$m" ]; then
  echo "ERROR: Number of lines mismatch: $l in ${OUTDIR}/lang.zst and $m in ${OUTDIR}/metadata.zst"
  exit 1
fi

echo $t $l $m >${OUTDIR}/.done
#rm $FIN
