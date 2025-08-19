#!/bin/bash
x="s3://${1#lumio:}"
OUTDIR=$2

mkdir -p $OUTDIR  # create directory, then s3cmd will download to this directory not to a file under its name
echo "$(date) stage2stage.sh: staging $x to $OUTDIR"
s3cmd get "$x" "$OUTDIR" --continue && \
    s3cmd get "${x%/html.zst}"/metadata.zst "$OUTDIR" --continue && \
    echo "$(date) stage2stage.sh: staging $x to $OUTDIR finished" || \
    { echo "$(date) stage2stage.sh: ERROR while staging $x to $OUTDIR" && exit 1; }
