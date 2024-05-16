#!/bin/bash
DATACENTER=$1
LPATH=$2
FILES=${@:3}

HOSTNAME=`hostname`
RPATH=`cat ${DATACENTER}_${HOSTNAME}.from`
module load lumio
echo $HOSTNAME downloading from $RPATH
echo $FILES | tr ' ' '\n' | rclone copy --stats-one-line --log-level INFO --log-file >(sed "s@^@$HOSTNAME: @") --files-from-raw - --multi-thread-streams 100 --transfers 4 $RPATH $LPATH 
