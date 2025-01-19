LOGDIR=$1
echo "crawl nlogs nparsed cpu-seconds"
for x in ${LOGDIR}/*; do
  echo -n $(basename $x _logs) `ls $x/*stderr|wc -l` " "
  tail -q -n 1 $x/*stderr | grep 'elapsed' | sed -r 's!^.* ([^ ]+)$!\1!' | python warc2html-time-from-logs.py 


done
