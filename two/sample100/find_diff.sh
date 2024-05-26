P1=$1
P2=$2
for c in CC wide; do for x in `seq 1 100`; do echo -n $x; diff <(tr -d ' '<$c/$x.$P1) <(tr -d ' '<$c/$x.$P2) |wc; done | grep -v "0$" |cut -f 1 -d ' ' >$c.${P1}_vs_${P2} ; done
