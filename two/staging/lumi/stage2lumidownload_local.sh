#!/bin/bash
set -euo pipefail

DATACENTER=$1
LPATH=$2
FILES=${@:3}

HOSTNAME=`hostname`
RPATH=`cat ${DATACENTER}_${HOSTNAME}.from`
module load lumio
echo $HOSTNAME downloading from $RPATH
echo $FILES | tr ' ' '\n' | rclone copy --stats-one-line --log-level INFO --log-file >(sed "s@^@$HOSTNAME: @") --files-from-raw - --multi-thread-streams 16 --transfers 50 --no-traverse --check-first $RPATH $LPATH 
