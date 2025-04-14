D1=$1
D2=$2
OUTDIR=$3

mkdir -p $OUTDIR
echo $D1 $D2 $OUTDIR >$OUTDIR/args

process_batch() {
    mkdir -p $3
    paste <(zstdcat ${1}/metadata.zst|jq -c '{'u':.u}') <(zstdcat ${1}/lang.zst|jq -c '{'lang1':.lang, 'prob1':.prob}') <(zstdcat ${1}/text.zst|jq -c '{'t1':.t}') <(zstdcat ${2}/lang.zst|jq -c '{'lang2':.lang, 'prob2':.prob}') <(zstdcat ${2}/text.zst|jq -c '{'t2':.t,'metalang':.metalang,'htmllang':.htmllang}') | sed 's!}\t{!,!g' | tee >(jq -c 'select(.lang1[0]==.lang2[0]) | . + {'collection':.lang1[0]}' | zstd >${3}/lang_same.zst) | jq -c 'select(.lang1[0]!=.lang2[0])' | tee >(jq -c '. + {'collection':((.lang1[0]//"null")+"-other")}' |zstd >${3}/lang_1.zst) | jq -c '. + {'collection':("other-"+(.lang2[0]//"null"))}' |zstd >${3}/lang_2.zst
}

export -f process_batch

find $D1 -name "lang.zst" | parallel --eta "process_batch {//} $D2/{= s:.*/([^/]+/[^/]+)/[^/]+.zst:\1: =} $OUTDIR/{= s:.*/([^/]+/[^/]+)/[^/]+.zst:\1: =}"
