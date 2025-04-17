#!/bin/bash
BASEOUTDIR=$1

echo "stage2local_batch.sh: running at `hostname`"
echo "stage2local_batch.sh: processing ${@:2}, writing to $BASEOUTDIR"
echo -n "Total size in GB: "
echo "${@:2}"|tr ' ' '\n' | xargs -n1 rclone lsjson|jq -c '.[]|.Size' | awk '{sum+=$1} END {print sum/2**30}'

rc=0
for x in ${@:2}; do 
#    OUTDIR=${BASEOUTDIR}/`echo $x | sed -r 's!.*(/[^/]+/[^/]+/)[^/]+!\1!'`  # BASEOUTDIR/crawl/batch_id/
#    OUTDIR=$(dirname $x)
    OUTDIR=${BASEOUTDIR}/`echo $x | sed -r "s@.*lumio:(.*)/html.zst@\1@"`
    echo "Processing $x, writing to ${OUTDIR}" 1>&2  # forward everything to stderr to interleave correctly with error messages from stage2local.sh
    time stage2local.sh $x ${OUTDIR} || { rc="$?"; echo "ERROR: stage2local.sh exited with code $rc while processing $x" 1>&2; }  # in bash && and || have the same priority
    echo "stage2local_batch.sh planned exit code:" $rc 1>&2
done

if [ "$rc" -eq 0 ]; then
  echo "stage2local_batch.sh: all files processed successfully"
else
  echo "stage2local_batch.sh: all files processed, errors occurred while processing"
fi

exit $rc
