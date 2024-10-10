#!/bin/bash
set -euo pipefail

NJOBS=$1  # number of parallel processes to fork
LOG_DIR=$2
FILTER_DIR=$(dirname $0)/..  # directory to take filter files from, if empty then no filtering is applied
mkdir -p ${LOG_DIR}
echo "Extracting HTML from WARCs in stdin in ${NJOBS} parallel processes, logging to ${LOG_DIR}"

#find ${WARCS_DIR} -name "*.warc*.gz" | 
#sort | 
parallel --colsep ':' \
    --joblog ${LOG_DIR}/joblog \
    --jobs=${NJOBS} \
    "mkdir -p {2}_log {2}/{1} || exit 1; cd {3}; eval echo warc2text --robotspass {2}/{1}/robotstxt -f html,metadata --jsonl --compress zstd --compress-level 9 --skip-text-extraction --classifier skip --url-filters ${FILTER_DIR}/url-filter-list.optimised -o {2}/{1} {4} >{2}_log/{1}.stdout 2>{2}_log/{1}.stderr"

JOBS_SUCCESS=`cat ${LOG_DIR}/joblog |cut -f 7|tail -n +2|python -c "import sys; l=list(map(bool,map(int,sys.stdin))); print(len(l)-sum(l),'/',len(l))"`

echo "$JOBS_SUCCESS jobs finished successfully, see ${LOG_DIR}/joblog for details. Run the following command to rerun failed jobs if any:"
echo "parallel --retry-failed --joblog ${LOG_DIR}/joblog"



