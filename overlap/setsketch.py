import gzip
from math import sqrt

from fire import Fire
import sys
from sketch_ds import setsketch
import mmh3

def buildsketch(outpath, fpath='-', domain_level=False, p=18, debug=False):
    """
    Reads urls (or any kind of lines) from stdin / text file / gzip-ed text file. Builds and saves a setsketch.
    Later it can be used to estimate the number of unique urls and jaccard similarity of two streams of urls built independently.
    The relative standard error for cardinality estimation is 1/sqrt(2**p). E.g. 0.002 (0.2%) for p=18.
    The relative standard error for jaccard estimation is sqrt((1/j-1)/2**p). E.g. 0.004 for jaccard=0.2, 0.06 (6%) for jaccard j=0.0009.
    :param outpath:
    :param fpath: source of lines, can be an ordinary file, a .gz file or '-' to read from stdin
    :param domain_level: from each line extracts a substring between the last '//' but before the first '/' after that; if the line is an URL, this extract its domain name.
    :param p: m=2**p registers will be used resulting in a sketch of 8*2**p bytes saved (e.g. 2 MB for p=18).
    :param debug: add lines to a set and print its exact cardinality to compare with an estimate from setsketch for sanity checking.
    :return:
    """
    if domain_level:
        url_preprocess = lambda url: url.strip().split('//')[-1].split('/')[0]
    else:
        url_preprocess = lambda url: url.strip()

    m = 2**p  # number of registers
    sk = setsketch.CSetSketch(m)
    if debug: ss = set()

    cnt = 0
    with sys.stdin if fpath=='-' else gzip.open(fpath, 'rt', encoding='utf-8') if fpath.endswith('gz') else open(fpath, 'rt', encoding='utf-8') as inp:
        # ss = {url_preprocess(s) for s in inp}
        for s in inp:
            item = url_preprocess(s)
            h,_ = mmh3.hash64(item, seed=0, signed=False,)
            sk.add(h)
            if debug: ss.add(item)
            cnt += 1

    print('lines', fpath, '-', cnt, sep='\t')
    print(cnt, 'lines are read', file=sys.stderr)
    if debug: print('unique lines, hashset', fpath, '-', len(ss), sep='\t')

    est = sk.report()
    stderr = 1.0 / sqrt(m)

    print('unique lines, csetsketch', fpath, '-', (est, stderr), sep='\t')
    print(f'number of unique lines by setsketch: {est}, relative stderr: {stderr}, 95% CI: ({est*(1-2*stderr)}, {est*(1+2*stderr)})', file=sys.stderr)
    sk.write(outpath)



Fire(buildsketch)
