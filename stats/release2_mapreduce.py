from fire import Fire
import zstandard
import pandas as pd
import sys


def _map(df, ftext, index_prefix, count_words=False):
    """
    Returns dataframe with the same number of rows, each row is the statistics for the corresponding input row.
    Counting words is expensive, disabled by default.
    """
    if index_prefix != '':
        index_prefix += ','
    df['index'] = index_prefix
    df['index'] += df.lang.str[0].fillna('null')

    df['text'] = df[ftext].fillna('')
    df = df.drop(columns=[c for c in df.columns if c not in {'index','text'}])
    
    df['text_newlines'] = df.text.str.count('\n') + 1
    if count_words:
        df['text_wcwords'] = (' ' + df.text).str.count(r'\s\S')
    df['text_chars'] = df.text.str.len()
    df['docs'] = 1
    df = df.drop(columns='text')
    return df


def _reduce(mdf):
    return mdf.groupby('index').agg('sum')


def stats(ftext='t', index_prefix='', file=sys.stdout, *files):
    adf = None
    files = [file] + list(files)
    inps = [zstandard.open(f, 'r') for f in files]
    while True:
        dfs = [pd.read_json(inp, nrows=10**6, orient='records', lines=True) for inp in inps]
        assert all( len(dfs[i]) == len(dfs[0]) for i in range(1,len(dfs)) )
        df = pd.concat(dfs, axis=1)
        if len(df) == 0:
            break

        mdf = _map(df, ftext, index_prefix, count_words=False)
        rdf = _reduce(mdf)    
        adf = rdf if adf is None else adf.add(rdf, fill_value=0)

    adf.to_csv(sys.stdout, sep='\t', index=True, header=None) 




Fire(stats)
