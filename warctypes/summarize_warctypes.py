import pandas as pd
from pathlib import Path
import fire

def summarize_warctypes(inputdir, t):
    df = pd.concat([pd.read_csv(f, sep='\t') for f in Path(inputdir).glob(f'*{t}.tsv')])
    df['content-length'] = pd.to_numeric(df['content-length'], errors='coerce')
    df = df.dropna()
    mdf = df.groupby('content-type').agg({'content-length':'sum'}).sort_values(by='content-length')/2**30
    print('\nTotal size accounted for:', mdf.sum().iloc[0])
    (mdf / mdf.sum()).to_csv(Path(inputdir)/f'props-{t}',sep='\t')
    mdf.loc['TOTAL'] = mdf.sum()
    mdf.to_csv(Path(inputdir)/f'total-{t}',sep='\t')

def main(inputdir):
    for t in ['contenttypes', 'rectypes']:
        summarize_warctypes(inputdir, t)


fire.Fire(main)
