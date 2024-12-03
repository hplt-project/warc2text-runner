import pandas as pd
from fire import Fire
from pathlib import Path


def check_gold(gold_stats_dir='../stats/release2.0_cleaned_stats_mr', hf_stats_dir='tmp111'):
    gdf = pd.read_csv(Path(gold_stats_dir)/'stats.tsv', sep='\t', header=None, names=['index','seg','wcwords','chars','docs'])
    hdf = pd.concat([pd.read_csv(p, sep=' ',header=None, names=['lang','hfchars','hfdocs']) for p in Path('tmp111/').glob('*.out') if p.stat().st_size], ignore_index=True)
    gdf[['crawl','lang']] = gdf['index'].str.split(',', expand=True)
    gdf = gdf.groupby('lang').sum(numeric_only=True).reset_index()
    mdf = gdf.merge(hdf, on='lang', how='left')
    print('No statistics from HF hub for the following languages:\n', '\n'.join(mdf[mdf.hfdocs.isnull()].lang.to_list()), sep='\n')
    print('The number of docs does not match:\n',mdf[mdf.hfdocs-mdf.docs != 0], sep='')
    print('The number of chars does not match:\n',mdf[mdf.hfchars-mdf.chars != 0], sep='')



Fire(check_gold)
