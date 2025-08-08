from pathlib import Path

from fire import Fire
import zstandard
import pandas as pd
import sys

from warc2text_runner.utils import unifying_iterator


class MRStats:
    def __init__(self, collection=None, lang=None, data_version='r2'):
        self.lang = lang
        self.collection = collection
        self.data_version = data_version


    def _build_index(self, df):
        df['index'] = self.collection or df['collection']
        df['index'] += ','
        df['index'] += self.lang or df['lang'].str[0].fillna('null')


    def _map(self, df, count_words=False):
        """
        Returns dataframe with the same number of rows, each row is the statistics for the corresponding input row.
        Counting words is expensive, disabled by default.
        """
        self._build_index(df)

        df['text'] = df['text'].fillna('')
        df = df.drop(columns=[c for c in df.columns if c not in {'index','text'}])

        df['text_newlines'] = df.text.str.count('\n') + 1
        if count_words:
            df['text_wcwords'] = (' ' + df.text).str.count(r'\s\S')
        df['text_chars'] = df.text.str.len()
        df['docs'] = 1
        df = df.drop(columns='text')
        return df


    def map(self, file='-', *files):
        adf = None
        files = [file] + list(files)
        inps = [sys.stdin if f=='-' else f for f in files]
        for df in unifying_iterator.batch_iterator(self.data_version, inps, batch_size=10**3, encoding_errors='replace'):
            mdf = self._map(df, count_words=True)
            rdf = self._reduce(mdf)
            adf = rdf if adf is None else adf.add(rdf, fill_value=0)

        adf.to_csv(sys.stdout, sep='\t', index=True, header=None)


    # def _batch_it(self, inps, batch_size):
#         readers = [
#             pd.read_json(inp, orient='records', lines=True, chunksize=batch_size)
#             for inp in inps]
# #        import pdb; pdb.set_trace()
#         for dfs in zip(*readers):
#             assert all(len(dfs[i]) == len(dfs[0]) for i in range(1, len(dfs)))
#             df = pd.concat(dfs, axis=1)
#             df.rename(columns={self.ftext: 'text'}, inplace=True)
#             df.lang, df.text = df.lang.astype(object), df.text.astype(str)
#             yield df


    def _reduce(self, mdf):
        return mdf.groupby('index').agg('sum')


    def reduce(self, dir):
        mdf = pd.read_csv(Path(dir)/'text_stats.csv',sep='\t', header=None)
        mdf.rename(columns={0: 'index'}, inplace=True)
        rdf = self._reduce(mdf)
        rdf.to_csv(Path(dir)/'stats.tsv', sep='\t', index=True, header=None)
        for f in (0,1):
            adf = rdf.groupby(rdf.index.str.split(',').str[f]).agg('sum')
            adf.to_csv(Path(dir) / f'stats-{f}.tsv', sep='\t', index=True, header=None)
            adf.astype('float').to_csv(Path(dir) / f'stats-{f}.exp.tsv', sep='\t', index=True, header=None, float_format='%.3e')
        adf = rdf.sum().to_frame('TOTAL').T
        adf.to_csv(Path(dir) / f'stats-TOTAL.tsv', sep='\t', index=True, header=None)


if __name__ == "__main__":
    Fire(MRStats)
