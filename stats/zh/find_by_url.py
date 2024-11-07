import pandas as pd
from warc2text_runner.utils.unifying_iterator import batch_iterator, _release2_iterator
import sys
from fire import Fire
from time import time

def retrieve(fqueries, file, *files):
    inps = [file] + list(files)
    qdf = pd.read_csv(fqueries, sep='\t', names=['u','qtext'])
    # import pdb; pdb.set_trace()
    st = time()
    for df in _release2_iterator(inps, batch_size=10**4):
        dur1 = time() - st
        mdf = df.merge(qdf, on='u', how='inner')    
        dur2 = time() - st
        print(f'Reading is {dur1/(dur2-dur1)}x slower than processing', file=sys.stderr)
        if len(mdf) > 0:
            mdf.to_json(sys.stdout, orient='records', lines=True)     
        st = time()


Fire(retrieve)
