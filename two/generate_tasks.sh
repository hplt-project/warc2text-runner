RUNDIR=$1
BS=$2
REMOTECONFIG="--sshlogin 3/mon3,3/mon4,3/mon6"
#REMOTECONFIG="--sshlogin 5/nird-c,5/nird-d"

cat $RUNDIR/crawls.paths | parallel --joblog $RUNDIR/joblog_generate_batches --eta --keep-order --linebuffer $REMOTECONFIG "module purge; module load parallel; cd {}; find ./ -name '*.warc*.gz' | parallel -I [] --seqreplace [#] -n $BS echo ~/hplt/two/code/warc2text-runner/two/run_warc2html_task.sh [#] ~/hplt/two/text/{/} {} []" |gzip >$RUNDIR/tasks.args.gz
