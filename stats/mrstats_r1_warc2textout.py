import base64
from fire import Fire
from mrstats_r2 import MRStatsR2
import pandas as pd

from warc2text_runner.utils import unifying_iterator


class MRStatsR1Warc2text(MRStatsR2):
    def __init__(self, collection, lang):
        super().__init__()
        self.collection = collection
        self.lang = lang


    def _build_index(self, df):
        df['index'] = (self.collection + ',' + self.lang)  # given constant value


    def _batch_it(self, inps, batch_size):
        unifying_iterator.batch_iterator('r1_warc2textout', inps, batch_size)

if __name__ == "__main__":
    Fire(MRStatsR1Warc2text)

