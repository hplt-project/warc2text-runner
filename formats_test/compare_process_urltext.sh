echo "Reading url, text from separate files url.gz, text.gz and passing to stdin as TSV (requires separate base64 decoding):"
time paste <(zcat url.gz) <(zcat text.gz) |wc

echo Reading url, text from separate files url.gz, text.gz and passing to stdin as jsonlines:
time paste <(zcat url.gz) <(zcat text.gz) |jq -Rc 'split("\t")|{"url":.[0],"text":.[1]|@base64d}'|wc

echo Reading url, text from singlejson.gz
time zcat singlejson.gz | jq -c '{url,text}'|wc
