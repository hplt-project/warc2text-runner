echo; echo "Read text from text.gz, this requires decoding from base64:"
time zcat text.gz|base64 -d|wc

echo; echo "Read text from single json:"
time zcat singlejson.gz |jq -rj ".text"|wc

echo; echo "Read text from text json:"
time zcat textjson.gz |jq -rj ".text"|wc
