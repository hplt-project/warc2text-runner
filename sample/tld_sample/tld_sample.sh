stream_file(){
  local FIN=$1
  #echo "Streaming $FIN" 1>&2
  if [[ $FIN =~ ^s3: ]]; then
    s3cmd get $FIN -
  else
    rclone cat $FIN
  fi
}

stream_tlds(){
  local FIN=${1}/metadata.zst
  stream_file $FIN | zstdcat | jq -cr .u | perl -MURI -ne '$u = URI->new($_); @h = split /\./, $u->host; print $h[-1],"\n"' | jq -Rc '{"tld":.}'
}

tld_stats2(){
  local DIN=${1}
  #echo "tld_stats2 $DIN" 1>&2
  stream_tlds ${1} | jq -c '{ "text":"", "collection":.tld}' | python ../../stats/mrstats.py --lang=$(basename $(dirname $(dirname $DIN/f))) map -
}

export -f stream_file
export -f stream_tlds
export -f tld_stats2


FPATHS=$1
STATS_DIR=$2
NJOBS=$3

mkdir -p $STATS_DIR
time cat $FPATHS | parallel --joblog $STATS_DIR/tld_stats.joblog --eta --jobs=$NJOBS "tld_stats2 {//}" > $STATS_DIR/text_stats.csv
time python ../../stats/mrstats.py reduce $STATS_DIR


FWEIGHTS=tmp/tld_weights.tsv
#time cat $FPATHS | parallel --line-buffer --joblog $STATS_DIR/sample.joblog --eta --jobs=$NJOBS "python paste_sample_weighted.py 300 $FWEIGHTS tld <(stream_tlds {//}) {//}/metadata.zst {//}/html.zst" | zstd >$STATS_DIR/sample.zst


