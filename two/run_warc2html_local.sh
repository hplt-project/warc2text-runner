#!/bin/bash
set -euo pipefail

# This script will read commands to run from stdin and run them on the local machine in NJOBS parallel processes.
# This script is started from ./run_warc2html_remote.sh, if you start it separately make sure to redirect stdin.
NJOBS=$1  # number of parallel processes to fork
LOG_DIR=$2
mkdir -p ${LOG_DIR}
echo "Extracting HTML from WARCs in stdin in ${NJOBS} parallel processes, logging to ${LOG_DIR}"

parallel \
    --joblog ${LOG_DIR}/joblog \
    --jobs=${NJOBS} 

JOBS_SUCCESS=`cat ${LOG_DIR}/joblog |cut -f 7|tail -n +2|python -c "import sys; l=list(map(bool,map(int,sys.stdin))); print(len(l)-sum(l),'/',len(l))"`

echo "$JOBS_SUCCESS jobs finished successfully, see ${LOG_DIR}/joblog for details. Run the following command to rerun failed jobs if any:"
echo "parallel --retry-failed --joblog ${LOG_DIR}/joblog"



