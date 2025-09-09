from fire import Fire
from pathlib import Path
import pandas as pd


def main(outdir, bs, charlen, file, *files):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=False)  
    files=  [file] + list(files)
    dfs = []
    for p in files:
        print('Loading', p)
        df = pd.read_json(p, lines=True)
        df['file'] = Path(p).name
        df['line'] = df.index
        dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)
    df = df.sort_values(by='line file'.split())

    df['text_show'] = df.text.str.replace('\n',' ')
    df['text_show'] = df.text_show.apply(lambda s: s if len(s) <= 2*charlen else s[:charlen] + '\n..........\n' + s[len(s)//2:len(s)//2+charlen] )
    df['porn?\nempty/1'] = ''
    df['unnatural?\nempty/1'] = ''
    df['lang correct?\n0/1'] = ''

    for b in range(len(df) // bs):
        bdf = df[[c for c in df.columns if c.endswith('/1')] + 'text_show id'.split()].iloc[b*bs:b*bs+bs]
        bdf.to_csv(outdir/f'batch{b}.tsv', sep='\t', index=False)



Fire(main)
