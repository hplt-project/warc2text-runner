from fire import Fire
import sys
import re
import prtpy

def batch_htmls(max_gb=1000):
    f2s = {}
    for l in sys.stdin:
        sz,l = re.split(r'\s+',l.strip())
        f2s[l] = float(sz)

    res = prtpy.pack(algorithm=prtpy.packing.first_fit_decreasing, binsize=max_gb*2**30, items=f2s)
    print('\n'.join(' '.join(r) for r in res))
    total = sum(f2s.values()) / 2 ** 30
    print(f'{len(f2s)} files of total size {total} GB packed into {len(res)} bins of max size {max_gb} GB.', file=sys.stderr)

Fire(batch_htmls)

