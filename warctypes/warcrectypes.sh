# Installation: pip install warctools

warcfilter -T response $@ | grep -i -a -E "^(WARC/1.0|Content-Type:|Content-Length:)" | tr -d '\r '|tr '\n' '\t' | sed 's!^WARC/1.0\t!!g' | sed 's!WARC/1.0\t!\n!g'
