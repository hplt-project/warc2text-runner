from pathlib import Path

from fire import Fire
import zstandard
import pandas as pd
import sys

from warc2text_runner.utils import unifying_iterator


class TraferrStats:
    def __init__(self, collection=None):
        self.collection = collection


    def _build_index(self, df):
        df['index'] = self.collection
        df['index'] += ','
        df['index'] += df['lang'].str[0].fillna('null')
        df['index'] += ','
        df['index'] += df['traferr'].fillna('OK')
        df['index'] += ','
        df['index'] += df['text'].apply(lambda t: 'null' if t is None else str(len(t)) if len(t) <= 1 else '>1')


    def _map(self, df):
        """
        Returns dataframe with the same number of rows, each row is the statistics for the corresponding input row.
        """
        self._build_index(df)

        df['text'] = df['text'].fillna('')
        df = df.drop(columns=[c for c in df.columns if c not in {'index','text'}])

        df['text_newlines'] = df.text.str.count('\n') + 1
        df['text_chars'] = df.text.str.len()
        df['docs'] = 1
        df = df.drop(columns='text')
        return df


    def map(self, file='-', *files):
        adf = None
        files = [file] + list(files)
        inps = [sys.stdin if f=='-' else f for f in files]
        for df in unifying_iterator.batch_iterator('r2', inps, batch_size=10**5, encoding_errors='replace'):
            mdf = self._map(df)
            rdf = self._reduce(mdf)
            adf = rdf if adf is None else adf.add(rdf, fill_value=0)

        adf.to_csv(sys.stdout, sep='\t', index=True, header=None)


    def _reduce(self, mdf):
        return mdf.groupby('index').agg('sum')


    def reduce(self, dir):
        mdf = pd.read_csv(Path(dir)/'text_stats.csv',sep='\t', header=None)
        mdf.rename(columns={0: 'index'}, inplace=True)
        rdf = self._reduce(mdf)
        rdf.to_csv(Path(dir)/'stats.tsv', sep='\t', index=True, header=None)
        for f in range(4):
            adf = rdf.groupby(rdf.index.str.split(',').str[f]).agg('sum')
            adf.to_csv(Path(dir) / f'stats-{f}.tsv', sep='\t', index=True, header=None)
        adf = rdf.sum().to_frame('TOTAL').T
        adf.to_csv(Path(dir) / f'stats-TOTAL.tsv', sep='\t', index=True, header=None)


if __name__ == "__main__":
    Fire(TraferrStats)
