import pandas as pd
import fire

def check_tsv(tsv):
    df=pd.read_csv(tsv, sep='\s+', header=None, names=['dir']+[f'{f}-{c}' for f in ('metadata','text','lang') for c in ('lines','words','bytes')])
    print('metadata-text lines mismatch:\n', '\n'.join(df[df['metadata-lines'] != df['text-lines']]['dir']))
    print('metadata-lang lines mismatch:\n','\n'.join(df[df['metadata-lines'] != df['lang-lines']]['dir']))


fire.Fire(check_tsv)
