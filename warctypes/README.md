Code to study types and sizes of records stored in WARC files. 

# Usage:
```bash run_warctypes.sh <WARCDIR> <SAMPLESIZE> <OUTDIR>```

samples SAMPLESIZE WARC files from WARCDIR, extracts content-type and content-length fields from all records of type 'response' from these WARCs.

```python summarize_warctypes.py <OUTDIR>```

prints content-types having the largest content-lengths along with this content-lengths (absolute and relative).

# Installation: 
```pip install warctools```