#RUNDIR=cesnet
#REMOTECONFIG="--sshloginfile sshloginfile_cesnet"
#PATTERNS="~/hplt/*/warc/*/*"

RUNDIR=nirdl
REMOTECONFIG=""
PATTERNS="~/hplt/one/warc/ia/* ~/hplt/two/warc/archivebot/* ~/hplt/two/warc/cc/CC* ~/hplt/two/warc/cc/_SAMPLE/*"


mkdir -p $RUNDIR
parallel $REMOTECONFIG --keep-order "eval echo {}" ::: $PATTERNS | tr ' ' '\n'  |tee $RUNDIR/crawls.paths
parallel $REMOTECONFIG --keep-order "find {} -name '*.warc.gz'|wc -l|tr '\n' '\t'; du -sh {}" :::: $RUNDIR/crawls.paths |tee $RUNDIR/crawls.stat
