These are 25 randomly sampled documents from release 1, WIDE15, zh folder, just after text extraction by warc2text. Documents with the same URL were retrieved from release 2, WIDE15, any language, just after text extraction by Trafilatura. If several documents for the same URL were retrieved, the first one was taken. We provide texts extracted by warc2text in release 1 and extracted by Trafilatura in release 2, and also their translations using ```googletrans``` (https://pypi.org/project/googletrans/).

For convenient comparison from the command line you can use:
```for x in `seq 0 25`; do vimdiff translated_r1_s${x}.txt translated_r2_s${x}.txt ; sleep 2;  done```

