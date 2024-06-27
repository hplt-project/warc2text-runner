from fire import Fire
from pathlib import Path
import sys


def batch_htmls(max_gb=1000):
    s = 0
    for l in sys.stdin:
        l = l.strip()
        sz = Path(l).stat().st_size
        if s + sz > max_gb * 2**30:
            s = 0
            print()
        s += sz
        print(l, file=sys.stdout, end=' ')


Fire(batch_htmls)

