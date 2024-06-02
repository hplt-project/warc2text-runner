#!/bin/bash

HTMLDIR=$1

module purge; module load LUMI systools parallel
find $HTMLDIR -name metadata.zst | parallel --eta  -j250 "echo {//}; zstdcat {}|wc; test -f {//}/text.zst && zstdcat {//}/text.zst|wc || echo 0 0 0; test -f {//}/lang.zst && zstdcat {//}/lang.zst|wc || echo 0 0 0" >text_lang_linecnts.log
cat text_lang_linecnts.log |tr '\n' ' ' | sed 's!/user!\n/user!g' >text_lang_linecnts.tsv
python -m warc2text_runner.two.qualitycontrol.check_text_lang_linecnt text_lang_linecnts.tsv
