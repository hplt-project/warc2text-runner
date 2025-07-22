FIN=$1
time zstdcat $FIN | python sample_cmp.py >cmp_sample_python.jsonl  
time zstdcat $FIN | perl -ne 'print if rand() < 0.0001' >cmp_sample_perl.jsonl
time zstdcat $FIN | awk 'BEGIN { srand() } { if (rand() < 0.0001) print $0 }' >cmp_sample_awk.jsonl

