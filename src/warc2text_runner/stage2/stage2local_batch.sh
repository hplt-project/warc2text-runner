#!/bin/bash
BASEOUTDIR=$1

echo "$(date) stage2local_batch.sh: running at `hostname`"
echo "$(date) stage2local_batch.sh: processing ${@:2}, writing to $BASEOUTDIR"
echo -n "Total size in GB: "
echo "${@:2}"|tr ' ' '\n' | xargs -n1 rclone lsjson|jq -c '.[]|.Size' | awk '{sum+=$1} END {print sum/2**30}'

rc=0
for x in ${@:2}; do 
#    OUTDIR=${BASEOUTDIR}/`echo $x | sed -r 's!.*(/[^/]+/[^/]+/)[^/]+!\1!'`  # BASEOUTDIR/crawl/batch_id/
#    OUTDIR=$(dirname $x)
    OUTDIR=${BASEOUTDIR}/`echo $x | sed -r "s@[^:]+:(.*)/html.zst@\1@"`
    echo "$(date) Processing $x, writing to ${OUTDIR}"  # forward everything to stderr to interleave correctly with error messages from stage2local.sh
    stage2local.sh $x ${OUTDIR}
    c="$?"
    echo "$(date) stage2local_batch.sh exit code: $c"
    if [ "$c" -ne 0 ]; then
       rc="$c"
       echo "$(date) stage2local_batch.sh: ERROR: processing $x, writing to ${OUTDIR} finished with code $c" 1>&2
    fi
done

if [ "$rc" -eq 0 ]; then
  echo "$(date) stage2local_batch.sh: all files processed successfully"
else
  echo "$(date) stage2local_batch.sh: all files processed, errors occurred while processing"
fi

exit $rc
