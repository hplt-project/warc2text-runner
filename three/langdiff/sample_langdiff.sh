D1=$1
D2=$2
OUTDIR=$3

#find $D1 -name "lang.zst" | parallel --eta "bash combine_textlang_12.sh {//} $D2/{= s:.*/([^/]+/[^/]+)/[^/]+.zst:\1: =} $OUTDIR/{= s:.*/([^/]+/[^/]+)/[^/]+.zst:\1: =}"

zstdcat $OUTDIR/*/*/textlang12.zst |jq -c 'select(.lang1[0]!=.lang2[0])|. + {"collection":(.collection|split("-")|.[0]+"-x")}' | python ../../sample/stratified_sample.py --fcol2group="" --outdir=lang-x sample
zstdcat $OUTDIR/*/*/textlang12.zst |jq -c 'select(.lang1[0]!=.lang2[0])|. + {"collection":("x-"+ .collection|split("-")|.[1])}' | python ../../sample/stratified_sample.py --fcol2group="" --outdir=x-lang sample
