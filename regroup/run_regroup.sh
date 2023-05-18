#!/bin/bash

DATASET_DIR=$1
OUTPUT_DIR=$2

BATCH_SIZE=1000000000
NJOBS=240

mkdir -p $OUTPUT_DIR

# Find all text.gz files, calculate their sizes in bytes (-b) and save to sizes.tsv
find $DATASET_DIR -name 'text.gz' -print0 | du -b --files0-from=- > ${OUTPUT_DIR}/sizes.tsv

# Generate a script that concatenates text.gz files for the same langauge into new text.gz files of approximately BATCH_SIZE bytes;
# if there are not enough texts for a languge, the resulting text.gz will be smaller; 
# if some of the original text.gz files is larger, the resulting text.gz will be larger;
# corresponding url.gz will also be concatenated;
# the results will be saved into directories BATCH_ID/LANGUAGE, where BATCH_ID is batch number counted independently for each language.
python batch_by_size.py ${OUTPUT_DIR}/sizes.tsv ${OUTPUT_DIR} ${BATCH_SIZE}
# Run the generated script in parallel.
cat ${OUTPUT_DIR}/tmp.sh | parallel --jobs ${NJOBS}  -N1 --pipe bash

