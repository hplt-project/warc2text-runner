#!/bin/bash

WARCS_DIR=$1
OUTPUT_DIR=$2
NJOBS=$3

LOG_DIR=${OUTPUT_DIR}_logs
BATCH_SIZE=100

echo "Extracting texts from WARCs in ${WARCS_DIR} in ${NJOBS} parallel processes in batches of ${BATCH_SIZE} WARCs each. Saving texts to ${OUTPUT_DIR} and logs to ${LOG_DIR}."

mkdir ${LOG_DIR} ${OUTPUT_DIR} || exit 1 
find ${WARCS_DIR} -name "*.warc.gz" | sort | parallel --will-cite --halt now,fail=1 --eta --max-args ${BATCH_SIZE} --jobs=${NJOBS} "warc2text -o ${OUTPUT_DIR}/{#} {} &> ${LOG_DIR}/{#}.log"

#TODO: 1. filter MT-generated texts 2. probably continue running even when some tasks fail, but make it simple to re-run failed tasks (--joblog and --retry-failed )
