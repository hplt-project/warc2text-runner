#!/bin/bash
HPLTDIR=/users/arefevni/hplt/zaragoza/monotextor-processing/cleaned/
FSTATS=../stats/release3.0_cleaned_stats_mr/stats-1.tsv
SIZE=1000
OUTDIR=per_lang_1000

TMP=$OUTDIR/tmp
mkdir -p $TMP

cut -f1,5 $FSTATS | sort >$OUTDIR/weights.tsv # language code and the number of docs
find $HPLTDIR  -name "*.jsonl.zst"|sed -r 's!'"${HPLTDIR%/}"'/(.*)/(.*)!\1\t\2!' | sort >$OUTDIR/paths.tsv


join -t$'\t' $OUTDIR/weights.tsv $OUTDIR/paths.tsv | awk -v OFS=$'\t' '{$2 = '$SIZE'/$2*1.2; print $0}' >$OUTDIR/matched.tsv  # matched langauges can be parallelized by file
join -t$'\t' -v2 $OUTDIR/weights.tsv $OUTDIR/paths.tsv | cut -f 1 | uniq >$OUTDIR/unmatched.tsv  # files in the unmatched folders will be processed sequentially because we don't know sampling probs 

# first process unmatched languages - there should be not very large ones, so it should be faster
#cat $OUTDIR/unmatched.tsv | parallel --joblog $OUTDIR/sample-perlang.joblog1  --eta --line-buffer  -j 200 "zstdcat $HPLTDIR/{}/*zst | shuf -n $SIZE >$TMP/{/}"

# now process matched languages
mkdir -p $OUTDIR/tmp2/
cat $OUTDIR/matched.tsv | parallel --colsep $'\t' --joblog $OUTDIR/sample-perlang.joblog2  --eta --line-buffer  -j 200 "zstdcat $HPLTDIR/{1}/{3} | ./utils/sample_with_prob.sh {2} >$OUTDIR/tmp2/{1}-{3}"
cat $OUTDIR/matched.tsv | cut -f 1 | sort | uniq |  parallel --joblog $OUTDIR/sample-perlang.joblog3 --eta --line-buffer  -j 200 "cat $OUTDIR/tmp2/{}-* >$TMP/{}"

# final shuffling and trimming

ls $TMP | parallel --joblog $OUTDIR/sample-perlang.joblog4 --eta --line-buffer -j 200 "shuf $TMP/{} | head -n $SIZE | zstd -o $OUTDIR/{}.shuf.zst"
#rm ???_????



