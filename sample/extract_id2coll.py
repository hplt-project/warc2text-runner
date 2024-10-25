from tqdm import tqdm
import pandas as pd
from pathlib import Path
from fire import Fire


def extract_id2c():
    dfs = []
    for p in tqdm(list(Path('./per_lang_group_1K').glob('*/*zst'))): 
        df1 = pd.read_json(p, orient='records', lines=True)
        dfs.append(df1)
    df1 = pd.concat(dfs, ignore_index=True)
    df1[['id','collection']].to_csv('per_lang_group_1K_id2c.tsv', sep='\t', index=False)
    

Fire(extract_id2c)
