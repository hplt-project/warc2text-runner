#!/bin/bash
set -euo pipefail

WARCS_DIR=$1  # directory with input WARC files
OUTPUT_DIR=$2  # directory to write extracted texts and urls to
NJOBS=$3  # number of parallel processes to fork
FILTER_DIR=$4  # directory to take filter files from, if empty then no filtering is applied

LOG_DIR=${OUTPUT_DIR%/}_logs # ${VAR%/} removes trailing slash if there is any
BATCH_SIZE=1000  # each run of warc2text processes BATCH_SIZE WARCs, too small batch will result in too many files generated which may lead to inodes exhaustion

echo "Extracting texts from WARCs in ${WARCS_DIR} in ${NJOBS} parallel processes in batches of ${BATCH_SIZE} WARCs each. Saving texts to ${OUTPUT_DIR} and logs to ${LOG_DIR}."

mkdir ${LOG_DIR} ${OUTPUT_DIR} || exit 1 

if [[ -d $FILTER_DIR ]]; then
    FILTERS="--tag-filters ${FILTER_DIR}/mt-filter-list.annotated  --url-filters ${FILTER_DIR}/url-filter-list.optimised"
    echo "Using filters: ${FILTERS}"
else
    FILTERS=""
    echo "WARNING: FILTER_DIR is not specified: using no filters!"	
fi

find ${WARCS_DIR} -name "*.warc.gz" | 
sort | 
parallel --will-cite --eta \
    --joblog ${LOG_DIR}/joblog \
    --max-args ${BATCH_SIZE} --jobs=${NJOBS} \
    "warc2text -o ${OUTPUT_DIR}/{#} {} ${FILTERS} >${LOG_DIR}/{#}.stdout 2>${LOG_DIR}/{#}.stderr"

JOBS_SUCCESS=`cat ${LOG_DIR}/joblog |cut -f 7|tail -n +2|python -c "import sys; l=list(map(bool,map(int,sys.stdin))); print(len(l)-sum(l),'/',len(l))"`
echo "$JOBS_SUCCESS jobs finished successfully, see ${LOG_DIR}/joblog for details. Run the following command to rerun failed jobs if any:"
echo "parallel --retry-failed --joblog ${LOG_DIR}/joblog"

