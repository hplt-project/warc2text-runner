from collections import defaultdict
from pathlib import Path

import numpy as np
from fire import Fire
import zstandard
import pandas as pd
import sys
from tqdm import tqdm


class Reservoir:
    def __init__(self, k):
        self.sdf = pd.DataFrame()
        self.k = k
        self.i = 0  # number of examples processed

    def dump(self, fout):
        self.sdf.to_json(fout, orient='records', lines=True)


    def _process_remaining(self, qdf):
        idx = np.random.randint(0, self.i, size=len(qdf))
        incl = (idx < self.k)  # each new example ends in the sample with prob=k/N, N is the running total
        nincl = incl.sum()
        if nincl == 0:
            return nincl
        idf = qdf.iloc[incl].copy()  # copy() hopefully helps the garbage collector to collect qdf
        #print('REPLACE:', len(idf))
        idx1 = np.random.choice(self.k, nincl, replace=False)  # choose random positions in the reservoir to rewrite
        self.sdf.iloc[idx1] = idf
        return nincl


    def update(self, df):
        self.i += len(df)

        #print('UPDATE: ', df.collection.unique(), len(df))
        if len(self.sdf) < self.k:  # first k examples go to the reservoir unconditionally
            n = self.k - len(self.sdf)
            self.sdf = pd.concat([self.sdf, df.head(n).copy()], ignore_index=True)
            rdf = df.iloc[n:]
        else:
            rdf = df

        if len(rdf) > 0:
            self._process_remaining(rdf)


class Sampler:
    def __init__(self, fcol2group, outdir, fcollection='collection', k=1000):
        """
        :param fcol2group: a mapping from collections to groups
        :param outdir: a directory to dump samples
        :param k: the number of examples sampled per group, if the total number is smaller all examples will be returned
        """
        self.outdir = Path(outdir)
        self.outdir.mkdir(parents=True, exist_ok=False)
        self.k = k
        self.fcollection = fcollection
        if fcol2group:
            mdf = pd.read_csv(fcol2group, sep='\t').set_index('collection').group.to_dict()
            self.col2group = mdf
        else:
            self.col2group = None


    def sample(self, file='-', *files):
        """
        Stratified sampling from a list of files or stdin.
        NB: feed all files for the same language to the script if you don't want to stratify by file as well, otherwise
        different number of examples in different files will not be taken into account!
        NB: tests have shown that processing speed is comparable to the speed of the UNIX ```wc``` utility when it calculates
        the number of words among other statistics (```wc -l``` which calculates only the number of lines is much faster).
        NB: this sampling function requires pandas 2.2.0 at least!
        :param file: the first file or '-' for stdin
        :param files: other files
        :return: nothing
        """
        c2r = defaultdict(lambda: Reservoir(k=self.k))
        files = [file] + list(files)
        inps = [sys.stdin if f=='-' else f for f in files]
        for df in self._batch_it(inps, batch_size=self.k):  # Reservoir currently doesn't work with batches >self.k
            df[0] = df[self.fcollection]
            if self.col2group:
                df[0] = df[0].replace(self.col2group)
            df.groupby(0).apply(lambda dfg : c2r[dfg.name].update(dfg), include_groups=False)

        for k, sdf in c2r.items():
            sdf.dump(self.outdir / f'{k}.jsonl.zst')
        df = pd.DataFrame.from_records(((k,sdf.i) for k, sdf in c2r.items()),
                                       columns=['group','size'])
        df.to_csv(self.outdir / 'groupsizes.tsv', index=False, sep='\t')


    def _batch_it(self, inps, batch_size):
        pbar = tqdm(inps)
        for inp in pbar:
            pbar.set_description(inp) 
            with pd.read_json(inp, orient='records', lines=True, chunksize=batch_size) as reader:
                for df in reader:
                    yield df


if __name__ == "__main__":
    Fire(Sampler)
