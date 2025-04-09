D1=$1
D2=$2
OUTDIR=$3

mkdir -p $OUTDIR
paste <(zstdcat ${D1}/lang.zst|jq -c '{'lang1':.lang}') <(zstdcat ${D1}/text.zst|jq -c '{'t1':.t}') <(zstdcat ${D2}/lang.zst|jq -c '{'lang2':.lang}') <(zstdcat ${D2}/text.zst|jq -c '{'t2':.t}') | sed 's!}\t{!,!g' |jq '. + {'collection':((.lang1[0]//"null")+"-"+(.lang2[0]//"null"))}' |zstd >${OUTDIR}/textlang12.zst
