r2s2=~/hpltn/two/html_stage2/wide00015
r2s1=~/hpltn/two/html/wide00015

ls $r2s2 | parallel --eta -j 90 "python find_by_url.py release1.2_warc2textout_wide15_sample_zh.tsv  $r2s2/{}/lang.zst  $r2s2/{}/text.zst  $r2s1/{}/html.zst  $r2s1/{}/metadata.zst 1>run1/{#}.out 2>run1/{#}.err"
