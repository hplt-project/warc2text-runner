from fire import Fire
import zstandard
import pandas as pd
import sys

class MRStatsR2:
    def __init__(self):
        pass


    def _build_index(self, df):
        df['index'] = df['collection']
        df['index'] += df['lang'].str[0].fillna('null')


    def _map(self, df, ftext, count_words=False):
        """
        Returns dataframe with the same number of rows, each row is the statistics for the corresponding input row.
        Counting words is expensive, disabled by default.
        """
        self._build_index(df)

        df['text'] = df[ftext].fillna('')
        df = df.drop(columns=[c for c in df.columns if c not in {'index','text'}])

        df['text_newlines'] = df.text.str.count('\n') + 1
        if count_words:
            df['text_wcwords'] = (' ' + df.text).str.count(r'\s\S')
        df['text_chars'] = df.text.str.len()
        df['docs'] = 1
        df = df.drop(columns='text')
        return df


    def map(self, ftext='t', file='-', *files):
        adf = None
        files = [file] + list(files)
        inps = [sys.stdin if f=='-' else zstandard.open(f, 'r') for f in files]
        while True:
            dfs = [pd.read_json(inp, nrows=10**5, orient='records', lines=True) for inp in inps]
            assert all( len(dfs[i]) == len(dfs[0]) for i in range(1,len(dfs)) )
            df = pd.concat(dfs, axis=1)
            if len(df) == 0:
                break

            mdf = self._map(df, ftext, count_words=False)
            rdf = self._reduce(mdf)
            adf = rdf if adf is None else adf.add(rdf, fill_value=0)

        adf.to_csv(sys.stdout, sep='\t', index=True, header=None)


    def _reduce(self, mdf):
        return mdf.groupby('index').agg('sum')


    def reduce(self):
        mdf = pd.read_csv('tmp/text_stats.csv',sep='\t', header=None)
        mdf.rename(columns={0: 'index'}, inplace=True)
        rdf = self._reduce(mdf)
        rdf.to_csv(sys.stdout, sep='\t', index=True, header=None)


Fire(MRStatsR2)