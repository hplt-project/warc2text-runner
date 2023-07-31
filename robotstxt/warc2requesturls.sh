WARCDIR=$1
OUTDIR=$2

mkdir -p $OUTDIR

find $WARCDIR -name "*.warc.gz" |parallel --joblog $OUTDIR/joblog --eta -n 10 "warcfilter -T request {}|grep '^WARC-Target-URI: '|cut -f 2- -d ' ' | gzip >${OUTDIR}/{#}.gz 2>${OUTDIR}/{#}.stderr" 
