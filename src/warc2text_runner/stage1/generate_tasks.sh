RUNDIR=$1
BS=$2
OUTDIR=$3
REMOTECONFIG=""
#REMOTECONFIG="--sshloginfile sshloginfile"
#REMOTECONFIG="--sshlogin 3/mon3,3/mon4,3/mon6"
#REMOTECONFIG="--sshlogin 5/nird-c,5/nird-d"

cat $RUNDIR/crawls.paths | parallel -j 4 --joblog $RUNDIR/joblog_generate_batches --eta --keep-order --linebuffer $REMOTECONFIG "module purge; module load parallel; cd {}; find ./ -name '*.warc*.gz' | shuf | parallel -I [] --seqreplace [#] -n $BS echo run_warc2html_task.sh [#] $OUTDIR/{/} {} []" | shuf | gzip >$RUNDIR/tasks.args.gz
