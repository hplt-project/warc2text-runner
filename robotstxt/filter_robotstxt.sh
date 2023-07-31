URLS_DIR=$1

find $URLS_DIR -name "*.gz"|parallel --max-args 10  --eta "zcat {}|grep 'robots.txt[/]*[[:cntrl:]]*$'" 

