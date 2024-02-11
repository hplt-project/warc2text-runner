#!/bin/bash
set -euo pipefail

RUNDIR=$1
NJOBS=$2
REMOTECONFIG=$3

#RUNDIR='cesnet'
#NJOBS=60
#REMOTECONFIG="--sshlogin 1/mon3,1/mon4,1/mon6"

#RUNDIR='nirdl'
#NJOBS=250
#REMOTECONFIG="--sshlogin 1/nird-d,1/nird-c"

LOG_DIR=${RUNDIR%/}_logs  # ${VAR%/} removes trailing slash if there is any

rm -rf $LOG_DIR; mkdir -p $LOG_DIR
zcat ${RUNDIR}/tasks.args.gz | parallel \
    --pipe -j1 --roundrobin -N1 \
    --joblog ${LOG_DIR}/joblog $REMOTECONFIG \
    "pwd; cd ~/hplt/two/code/warc2text-runner/two; module purge; module load parallel nlpl-warc2text/1.2; ./run_warc2html_local.sh ${NJOBS} \`hostname\` "

JOBS_SUCCESS=`cat ${LOG_DIR}/joblog |cut -f 7|tail -n +2|python -c "import sys; l=list(map(bool,map(int,sys.stdin))); print(len(l)-sum(l),'/',len(l))"`
echo "$JOBS_SUCCESS jobs finished successfully, see ${LOG_DIR}/joblog for details. Run the following command to rerun failed jobs if any:"
echo "parallel --retry-failed --joblog ${LOG_DIR}/joblog"

