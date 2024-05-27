import pandas as pd

df=pd.read_csv('text_lang_linecnts.tsv', sep='\s+', header=None, names=['dir']+[f'{f}-{c}' for f in ('metadata','text','lang') for c in ('lines','words','bytes')])
print('\n'.join(df[df['metadata-lines'] != df['text-lines']]['dir']))
print('\n'.join(df[df['metadata-lines'] != df['lang-lines']]['dir']))
