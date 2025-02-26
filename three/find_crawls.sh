#RUNDIR=cesnet
#REMOTECONFIG="--sshloginfile sshloginfile_cesnet"
#PATTERNS="~/hplt/*/warc/*/*"

RUNDIR=nirdl_three_cc
REMOTECONFIG=""
PATTERNS="~/hplt/three/warc/cc/CC-MAIN*"

module purge; module load parallel; module unload OpenSSL
mkdir -p $RUNDIR
parallel $REMOTECONFIG --keep-order "eval echo {}" ::: $PATTERNS | tr ' ' '\n'  |tee $RUNDIR/crawls.paths
parallel $REMOTECONFIG --keep-order "find {} -name '*.warc*.gz'|wc -l|tr '\n' '\t'; du -sh {}" :::: $RUNDIR/crawls.paths |tee $RUNDIR/crawls.stat
