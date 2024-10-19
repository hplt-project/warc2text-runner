REMOTE="nikolare/HPLT2.0_cleaned"
LOGDIR=logs_cleaned
mkdir -p $LOGDIR
cut -f 2 <cleaned_du.tsv | parallel -j 1 --joblog upload_cleaned.log "python hf_upload_lang.py {} $REMOTE >$LOGDIR/{#}.out 2>$LOGDIR/{#}.err"

