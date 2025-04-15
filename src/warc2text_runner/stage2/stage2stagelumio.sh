#!/bin/bash
BASEOUTDIR=$1

XX=`echo ${@:2} | sed 's/lumio://g'`
YY=`echo $XX | sed 's/html.zst/metadata.zst/g'`
ZZ=`echo $XX | sed 's/html.zst/robotstxt.warc.gz/g'`

echo $XX $YY $ZZ|tr ' ' '\n' | rclone copy -v lumio: $BASEOUTDIR --include-from="-" --transfers=64 --multi-thread-streams=0 --checkers=1
