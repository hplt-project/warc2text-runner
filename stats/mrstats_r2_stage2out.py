from fire import Fire
import zstandard
import pandas as pd
import sys

from stats.mrstats_base import MRStatsR2


class MRStatsR2S2(MRStatsR2):
    def __init__(self, collection):
        self.collection = collection


    def _build_index(self, df):
        df['index'] = self.collection + ','  # given constant value
        df['index'] += df.lang.str[0].fillna('null')



Fire(MRStatsR2S2)
