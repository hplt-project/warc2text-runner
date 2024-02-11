#!/bin/bash
set -euo pipefail

NJOBS=$1  # number of parallel processes to fork
LOG_DIR=$2
mkdir -p ${LOG_DIR}
echo "Extracting HTML from WARCs in stdin in ${NJOBS} parallel processes, logging to ${LOG_DIR}"

#find ${WARCS_DIR} -name "*.warc.gz" | 
#sort | 
parallel \
    --joblog ${LOG_DIR}/joblog \
    --jobs=${NJOBS} 

JOBS_SUCCESS=`cat ${LOG_DIR}/joblog |cut -f 7|tail -n +2|python -c "import sys; l=list(map(bool,map(int,sys.stdin))); print(len(l)-sum(l),'/',len(l))"`

echo "$JOBS_SUCCESS jobs finished successfully, see ${LOG_DIR}/joblog for details. Run the following command to rerun failed jobs if any:"
echo "parallel --retry-failed --joblog ${LOG_DIR}/joblog"



