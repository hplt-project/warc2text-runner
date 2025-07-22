#!/bin/bash
set -euo pipefail
TASKDIR=$1

time python repack_dedup.py $TASKDIR/tmp2/ $TASKDIR/tmp/*zst &>$TASKDIR/tmp2/repack_dedup.log

