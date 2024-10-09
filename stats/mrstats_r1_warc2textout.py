import base64
from fire import Fire
from mrstats_r2 import MRStatsR2
import pandas as pd


class MRStatsR1Warc2text(MRStatsR2):
    def __init__(self, collection, lang):
        super().__init__()
        self.collection = collection
        self.lang = lang


    def _build_index(self, df):
        df['index'] = (self.collection + ',' + self.lang)  # given constant value


    def _batch_it(self, inps, batch_size):
        assert len(inps) == 1, 'Specify only the file with base64-encoded texts!'
        reader = pd.read_csv(inps[0], sep='\t', header=None, chunksize=10**5, names=['text'])
        for df in reader:
            df.text = df.text.apply(lambda b: base64.b64decode(b).decode('utf-8'))
            yield df


if __name__ == "__main__":
    Fire(MRStatsR1Warc2text)

