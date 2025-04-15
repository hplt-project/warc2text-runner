#!/bin/bash
set -euo pipefail

BASEOUTDIR=$1  # directory to download files to, remote paths will be preserved inside this directory
XX="${@:2}"  # html.zst files to download

YY=`echo $XX | sed 's/html.zst/metadata.zst/g'`
ZZ=`echo $XX | sed 's/html.zst/robotstxt.warc.gz/g'`

# download all files from the batch with one rclone call; since we process 100-300 batches in parallel,
# to reduce the number of parallel tasks we run only 1 checker for md5sum of the downloaded files and no
# multi-thread downloads (on LUMI multi-thread downloads from lumio seems to be slower anyway)
echo $XX $YY $ZZ | sed 's@lumio:@@g' | tr ' ' '\n' | \
  rclone copy -v lumio: $BASEOUTDIR --files-from="-" --transfers=32 --multi-thread-streams=0 --checkers=1 --no-traverse
ls `echo $XX $YY $ZZ | sed "s@lumio:@${BASEOUTDIR}/@g"` >/dev/null  # if any file is absent, return non-zero error code