#!/bin/bash
set -euo pipefail

DATACENTER=$1
FPATHS=$2
LPATH=$3

LOGDIR=${DATACENTER}_logs
mkdir -p ${LOGDIR}

FIFO=${LOGDIR}/.fifo
REMOTECONFIG="--sshlogin 3/uan01,3/uan02,3/uan04"

cat $FPATHS | parallel --joblog ${LOGDIR}/download.joblog --line-buffer $REMOTECONFIG --eta -n 150 "echo -n we are on; hostname; cd ~/hplt/two/code/warc2text-runner/two/staging/lumi; bash stage2lumidownload_local.sh $DATACENTER $LPATH {}" | tee -a ${LOGDIR}/download.log >>$FIFO


