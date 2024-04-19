export C=$1; 
for X in `cat $C.MIN_EXTRACTED_SIZE_0_vs_.no_fallback_False.txt`; do open $C/$X.html; vimdiff $C/$X.MIN_EXTRACTED_SIZE_0.txt $C/$X.no_fallback_False.txt ; done
