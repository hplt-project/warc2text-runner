Code to study types and sizes of records stored in WARC files. 
This code aims at calculating a rough estimate of proportions of different types of content inside a crawl, thus it processes a random sample of WARC files and may fail to process a few of them. Look at joblog and make sure that the proportion of failures is not too large, otherwise the estimate may be too bad.  

# Usage:
```bash run_warctypes.sh <WARCDIR> <SAMPLESIZE> <OUTDIR>```

samples SAMPLESIZE WARC files from WARCDIR, extracts content-type and content-length fields from all records of type 'response' from these WARCs.

```python summarize_warctypes.py <OUTDIR>```

prints content-types having the largest content-lengths along with this content-lengths (absolute and relative).

# Installation: 
```pip install warctools```