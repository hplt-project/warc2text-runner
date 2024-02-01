echo; echo Reading url, date from url.gz and date.gz
time paste <(zcat url.gz) <(zcat date.gz)|wc

echo; echo Reading url, date from singlejson.gz
time zcat singlejson.gz |jq -cr '[.url,.date]|join("\t")'|wc

echo; echo Reading url, date from metajson.gz:
time zcat metajson.gz |jq -cr '[.url,.date]|join("\t")'|wc
