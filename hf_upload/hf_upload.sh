#!/bin/bash
FLIST=$1

REMOTE="nikolare/test"
#REMOTE="HPLT/HPLT2.0_dedup"
LOGDIR=${FLIST}_logs
mkdir -p $LOGDIR
cut -f 2 <$FLIST | parallel -j 11 --joblog $LOGDIR/joblog "python hf_upload_lang.py {} $REMOTE >$LOGDIR/{#}.out 2>$LOGDIR/{#}.err"

