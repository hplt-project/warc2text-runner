RUNDIR=$1
BS=$2
#REMOTECONFIG="--sshlogin 1/mon3"
REMOTECONFIG=""

cat $RUNDIR/crawls.paths | parallel -j1 --keep-order --linebuffer $REMOTECONFIG "module purge; module load parallel; eval find {} -name '*.warc.gz' | parallel -I [] --seqreplace [#] -n $BS echo [#] : ~/hplt/two/text/{/} : []" >$RUNDIR/tasks.args
