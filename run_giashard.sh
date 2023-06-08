#!/bin/bash

# This script reads language codes from stdin, one code per line.
TEXT_DIR=${1%/}  # ${VAR%/} removes trailing slash if there is any
NJOBS=$2  # number of parallel processes to fork; it seems optimal to use 1, i.e. process languages sequentially, since giashard.sh processes each language on all available CPUs
#TODO: it may be reasonable to merge this script with giashard.sh and get rid of nested parallels by creating a set of tasks differing by language and part, and also balance batches in giashard.sh by size in bytes. This will result in better estimation and indication of the time left.
OUTPUT_DIR=${TEXT_DIR}-shards

LOG_DIR=${OUTPUT_DIR}_logs 
mkdir -p ${LOG_DIR} ${OUTPUT_DIR} || exit 1 


parallel --will-cite --eta \
    --jobs ${NJOBS} \
    --joblog ${LOG_DIR}/joblog \
    "./giashard.sh ${TEXT_DIR} {} >${LOG_DIR}/{}.stdout 2>${LOG_DIR}/{}.stderr"

JOBS_SUCCESS=`cat ${LOG_DIR}/joblog |cut -f 7|tail -n +2|python -c "import sys; l=list(map(bool,map(int,sys.stdin))); print(len(l)-sum(l),'/',len(l))"`
echo "$JOBS_SUCCESS jobs finished successfully, see ${LOG_DIR}/joblog for details. Run the following command to rerun failed jobs if any:"
echo "parallel --retry-failed --joblog ${LOG_DIR}/joblog"

