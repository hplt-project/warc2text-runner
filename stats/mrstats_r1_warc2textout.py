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
        self.data_version = 'r1_warc2textout'


    def _build_index(self, df):
        df['index'] = (self.collection + ',' + self.lang)  # given constant value


if __name__ == "__main__":
    Fire(MRStatsR1Warc2text)

