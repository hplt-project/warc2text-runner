D1=$1
D2=$2
OUTDIR=$3

mkdir -p $OUTDIR

process_batch() {
    mkdir -p $3
    paste <(zstdcat ${1}/lang.zst|jq -c '{'lang1':.lang}') <(zstdcat ${1}/text.zst|jq -c '{'t1':.t}') <(zstdcat ${2}/lang.zst|jq -c '{'lang2':.lang}') <(zstdcat ${2}/text.zst|jq -c '{'t2':.t}') | sed 's!}\t{!,!g' |jq -c 'select(.lang1[0]!=.lang2[0]) | . + {'collection':((.lang1[0]//"null")+"-other")}' |zstd >${3}/lang_changed.zst
}

export -f process_batch

find $D1 -name "lang.zst" | parallel --eta "process_batch {//} $D2/{= s:.*/([^/]+/[^/]+)/[^/]+.zst:\1: =} $OUTDIR/{= s:.*/([^/]+/[^/]+)/[^/]+.zst:\1: =}"
