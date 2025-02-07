RUNDIR=$1
BS=$2
REMOTECONFIG=""
#REMOTECONFIG="--sshloginfile sshloginfile"
#REMOTECONFIG="--sshlogin 3/mon3,3/mon4,3/mon6"
#REMOTECONFIG="--sshlogin 5/nird-c,5/nird-d"

cat $RUNDIR/crawls.paths | parallel -j 4 --joblog $RUNDIR/joblog_generate_batches --eta --keep-order --linebuffer $REMOTECONFIG "module purge; module load parallel; cd {}; find ./ -name '*.warc*.gz' | shuf | parallel -I [] --seqreplace [#] -n $BS echo run_warc2html_task.sh [#] /nird/projects/NS8112K/three/html/{/} {} []" |gzip >$RUNDIR/tasks.args.gz
