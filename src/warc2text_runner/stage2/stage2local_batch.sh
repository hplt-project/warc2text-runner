#!/bin/bash
BASEOUTDIR=$1

getoutdir() {
    x=$1
#    OUTDIR=${BASEOUTDIR}/`echo $x | sed -r 's!.*(/[^/]+/[^/]+/)[^/]+!\1!'`  # BASEOUTDIR/crawl/batch_id/
#    OUTDIR=$(dirname $x)
    if [ "${x#$BASEOUTDIR}" = "$x" ]; then  # if removing $BASEOUTDIR from the beginning of $x doesn't change $x, then it doesn't start with it
        OUTDIR=${BASEOUTDIR}/`echo $x | sed -r "s@[^:]+:(.*)/html.zst@\1@"`
    else
        OUTDIR=$(dirname "$x")
    fi
    echo $OUTDIR
}

process() {
    local x=$1
    local OUTDIR=$2
    echo "$(date) Processing $x, writing to ${OUTDIR}"  # forward everything to stderr to interleave correctly with error messages from stage2local.sh
    stage2local.sh $x ${OUTDIR}
    c="$?"
    echo "$(date) stage2local_batch.sh exit code: $c"
    return $c
}

stage() {
    local x="s3://${1#lumio:}"
    local OUTDIR=$2
    mkdir -p $OUTDIR  # create directory, then s3cmd will download to this directory not to a file under its name
    echo "$(date) stage2local_batch.sh: staging $x to $OUTDIR"
    s3cmd get "$x" "$OUTDIR" --continue && \
        s3cmd get "${x%/html.zst}"/metadata.zst "$OUTDIR" --continue && \
        echo "$(date) stage2local_batch.sh: staging $x to $OUTDIR finished" || \
        { echo "$(date) stage2local_batch.sh: ERROR while staging $x to $OUTDIR" && return 1; }
}

clean() {
    local OUTDIR=$1
    echo "$(date) stage2local_batch.sh: cleaning $OUTDIR"
    rm -f "$OUTDIR"/html.zst
}

echo "$(date) stage2local_batch.sh: running at `hostname`"
echo "$(date) stage2local_batch.sh: processing ${@:2}, writing to $BASEOUTDIR"
echo -n "Total size in GB: "
echo "${@:2}"|tr ' ' '\n' | xargs -n1 rclone lsjson|jq -c '.[]|.Size' | awk '{sum+=$1} END {print sum/2**30}'

rc=0
current="$2"
for next in "${@:3}"; do
    stage "$next" "$(getoutdir "$next")" &
    staging_job=$!
    process "$current" "$(getoutdir "$current")" && clean "$(getoutdir "$current")" || rc="$?"
    # staging should have finished, otherwise don't waste expensive node-hours to wait for it
    kill $staging_job && echo "WARNING: staging $next stopped because it has not finished in time"
    wait $staging_job && current="$(getoutdir "$next")/html.zst" || { current=$next && clean "$(getoutdir "$current")"; }
done
process "$current" "$(getoutdir "$current")" && clean "$(getoutdir "$current")" || rc="$?"

if [ "$rc" -eq 0 ]; then
  echo "$(date) stage2local_batch.sh: all files processed successfully"
else
  echo "$(date) stage2local_batch.sh: all files processed, errors occurred while processing"
fi

exit $rc
