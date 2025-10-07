import sys
import random
from fire import Fire
import pandas as pd
import io 
from smart_open import open
import ujson as json
from pathlib import Path
from tqdm import tqdm


class DedupWriter:
    def __init__(self, tld, outdir):
        super().__init__()
        self.outp = open(outdir / f'{tld}.jsonl.zst', 'wb')
        self.hashes = set()


    def write(self, binary_data, dedup_key=None):
        if dedup_key:
            h = hash(dedup_key)
            if h in self.hashes:
                return
            self.hashes.add(h)
        self.outp.write(binary_data)


def get_dedup_writer(tld, tld2writer, outdir):
    if tld not in tld2writer:
        tld2writer[tld] = DedupWriter(tld, outdir)
    return tld2writer[tld]

def repack_dedup(outdir, fstrat, fdedup, file, *files):
    """
    """
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    files = [file] + list(files)

    tld2writer = dict()
    for f in tqdm(files):
        fin = sys.stdin.buffer if f=='-' else io.BufferedReader(open(f, 'rb'))
        for bl in fin:
            d = json.loads(bl.decode('utf-8', errors='replace').strip())
            writer = get_dedup_writer(d[fstrat], tld2writer, outdir)
            writer.write(bl, d[fdedup] if fdedup else None)


Fire(repack_dedup)
