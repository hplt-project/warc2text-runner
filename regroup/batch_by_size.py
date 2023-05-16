import pandas as pd
import fire

def batches_by_size(df, size=2**30):
    res = df.groupby(df['size'].cumsum() // size).agg({'size':'sum', 'path': ' '.join})
    return res


def main(fsizes = 'sizes', fbatches = 'batches', size=2**30):
    df = pd.read_csv(fsizes, sep='\t', header=None, names=['size','path'])
    df['lang'] = df.path.str.split('/').str[-2]
    bf = df.groupby('lang').apply(lambda df: batches_by_size(df, size))
    bf.index.rename({'size':'batch'}, inplace=True)
    bf = bf.reset_index()

    bf.to_csv(fbatches, sep='\t')

    print('\n'.join(bf.path))


fire.Fire(main)


