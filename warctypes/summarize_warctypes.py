import pandas as pd
from pathlib import Path
import fire

def summarize_warctypes(inputdir, t):
    df = pd.concat([pd.read_csv(f, sep='\t') for f in Path(inputdir).glob(f'*{t}.tsv')])
    df['content-length'] = pd.to_numeric(df['content-length'], errors='coerce')
    df = df.dropna()
    mdf = df.groupby('content-type').agg({'content-length':'sum'}).sort_values(by='content-length')/2**30
    mdf.to_csv(Path(inputdir)/f'total-{t}',sep='\t')
    print(mdf.tail(25))
    print('\nTotal size accounted for:', mdf.sum().iloc[0])
    print((mdf/mdf.sum()).tail(25))


def main(inputdir):
    for t in ['contenttypes', 'rectypes']:
        summarize_warctypes(inputdir, t)


fire.Fire(main)
