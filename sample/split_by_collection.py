from fire import Fire
import pandas as pd
from pathlib import Path


def split(fin, outdir, collection2group=None):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=False)  # since we append to the files, better remove them before re-running
    if collection2group is not None:
        mdf = pd.read_csv(collection2group, sep='\t')
        collection2group = mdf.set_index('collection')['group'].to_dict()
    df = pd.read_json(fin, orient='records', lines=True)
    for c in df.collection.unique():
        cdf = df[df.collection==c]
        group = collection2group.get(c) if collection2group is not None else c
        cdf.to_json(outdir/str(group),orient='records',lines=True, index=False, mode='a')  # str(group) to support group=None


Fire(split)
