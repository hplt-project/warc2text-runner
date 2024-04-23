C=$1
S1=$2
S2=$3
for X in `cat $C.${S1}_vs_${S2}`; do open $C/$X.html; vimdiff $C/$X.${S1} $C/$X.${S2} ; done
