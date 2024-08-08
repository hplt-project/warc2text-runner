#!/bin/bash
set -euo pipefail

# This script runs commands from ${RUNDIR}/tasks.args.gz in parallel on several remote nodes, and in parallel on each node

RUNDIR=$1  # The directory with tasks.args.gz to take tasks from
NJOBS=$2  # The number of tasks to run in parallel on each remote node
REMOTECONFIG=$3  # Configuration of remote nodes for GNU Parallel, pass the empty string to run locally. E.g. "--sshlogin 1/mon3,1/mon4,1/mon6", "--sshloginfile sshloginfile_cesnet"

#RUNDIR='cesnet'
#NJOBS=60
#REMOTECONFIG="--sshlogin 1/mon3,1/mon4,1/mon6"

#RUNDIR='nirdl'
#NJOBS=250  # number of commands executed in parallel on each remote node
#REMOTECONFIG="--sshlogin 1/nird-d,1/nird-c"  # hostnames of the compute nodes, ensure passwordless access to them

LOG_DIR=${RUNDIR%/}_logs  # ${VAR%/} removes trailing slash if there is any

rm -rf $LOG_DIR; mkdir -p $LOG_DIR

# run_warc2html_local.sh will be started on the remote host and will take commands to run from the stdin
zcat ${RUNDIR}/tasks.args.gz | parallel \
    --pipe -j1 --roundrobin -N1 \
    --joblog ${LOG_DIR}/joblog $REMOTECONFIG \
    "pwd; cd ~/hplt/two/code/warc2text-runner/two; module purge; module load parallel nlpl-warc2text/1.2; ./run_warc2html_local.sh ${NJOBS} \`hostname\` "

JOBS_SUCCESS=`cat ${LOG_DIR}/joblog |cut -f 7|tail -n +2|python -c "import sys; l=list(map(bool,map(int,sys.stdin))); print(len(l)-sum(l),'/',len(l))"`
echo "$JOBS_SUCCESS jobs finished successfully, see ${LOG_DIR}/joblog for details. Run the following command to rerun failed jobs if any:"
echo "parallel --retry-failed --joblog ${LOG_DIR}/joblog"

