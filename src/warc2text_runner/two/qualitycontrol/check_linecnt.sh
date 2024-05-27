#!/bin/bash

HTMLDIR=$1

module purge; module load LUMI systools parallel
find $HTMLDIR -name text.zst | parallel --eta  -j250 "echo {//}; zstdcat {//}/metadata.zst|wc;  zstdcat {//}/text.zst|wc; zstdcat {//}/lang.zst|wc" > text_lang_linecnts.log
cat text_lang_linecnts.log |tr '\n' ' ' | sed 's!/user!\n/user!g' >text_lang_linecnts.tsv
