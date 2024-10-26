import pandas as pd
from warc2text_runner.utils.unifying_iterator import batch_iterator, _release2_iterator
import sys
from fire import Fire


def retrieve(fqueries, file, *files):
    inps = [file] + list(files)
    qdf = pd.read_csv(fqueries, sep='\t', names=['url','text'])
    # import pdb; pdb.set_trace()
    for df in _release2_iterator(inps, batch_size=10**5):
        mdf = df.merge(qdf, on='url', how='inner')    
        if len(mdf) > 0:
            mdf.to_csv(sys.stdout)     


Fire(retrieve)
