import sys
from time import time

import pandas as pd
from fire import Fire

from warc2text_runner.utils import unifying_iterator


def retrieve(fqueries, file, *files):
    inps = [file] + list(files)
    qdf = pd.read_csv(fqueries, sep='\t', names=['u','qtext'])
    # import pdb; pdb.set_trace()
    st = time()
    for df in unifying_iterator.batch_iterator('r2', inps, batch_size=10**4, encoding_errors='replace'):
        dur1 = time() - st
        mdf = df.merge(qdf, on='u', how='inner')    
        dur2 = time() - st
        print(f'Reading is {dur1/(dur2-dur1)}x slower than processing', file=sys.stderr)
        if len(mdf) > 0:
            mdf.to_json(sys.stdout, orient='records', lines=True)     
        st = time()


Fire(retrieve)
