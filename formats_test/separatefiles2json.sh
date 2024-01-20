echo; echo Separate files: 
du -sch url.gz date.gz text.gz


time paste <(zcat url.gz) <(zcat date.gz) <(zcat text.gz)|jq -Rc 'split("\t")|{"date":.[1],"url":.[0],"text":.[2]|@base64d}' | gzip >singlejson.gz
echo; echo Single gziped json:
du -sch singlejson.gz

time paste <(zcat url.gz) <(zcat date.gz) |jq -Rc 'split("\t")|{"date":.[1],"url":.[0]}' | gzip >metajson.gz
time zcat text.gz|jq -Rc '{"text":@base64d}' | gzip >textjson.gz
echo; echo Text and meta  gziped jsons:
du -sch metajson.gz textjson.gz


