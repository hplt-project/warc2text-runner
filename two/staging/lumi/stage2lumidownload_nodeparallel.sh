#!/bin/bash
DATACENTER=$1
FPATHS=$2
LPATH=$3
FIFO=${DATACENTER}.fifo

REMOTECONFIG="--sshlogin 1/uan01,1/uan02,1/uan04"

cat $FPATHS | parallel --joblog ${DATACENTER}.download.joblog --line-buffer $REMOTECONFIG --eta -N 48 "cd ~/hplt/two/code/warc2text-runner/two/staging/lumi; ./stage2lumidownload_local.sh $DATACENTER $LPATH {}" | tee -a ${DATACENTER}.download.log >>$FIFO

