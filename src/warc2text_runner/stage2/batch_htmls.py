from fire import Fire
from pathlib import Path
import sys
import re

def batch_htmls(max_gb=1000):
    s = 0
    for l in sys.stdin:
        sz,l = re.split(r'\s+',l.strip())
        sz = float(sz)
        if s + sz > max_gb * 2**30:
            s = 0
            print()
        s += sz
        print(l, file=sys.stdout, end=' ')


Fire(batch_htmls)

