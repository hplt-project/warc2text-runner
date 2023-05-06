import gzip
import psutil
from itertools import islice
import sys
import fire
from HLL import HyperLogLog
from math import sqrt


def set_file_intersection(set1, file2, url_preprocess=lambda url: url.strip()):
    """
    Returns intersection between lines if file2 and set1. Lines of file2 are preprocessed with url_preprocess.
    """
    with gzip.open(file2, 'rt', encoding='utf-8') if file2.endswith('gz') else open(file2, 'rt', encoding='utf-8') as inp:
        intersection = set1.intersection((url_preprocess(s) for s in inp))
    return intersection


def read_portion1(iterator, mem_limit, batch_size=10**6, debug=False, url_preprocess=lambda url: url.strip()):
    """
    From iterator reads items into a set while there are items available and
    the memory consumption of the process stays within mem_limit.
    Preprocesses items with url_preprocess.
    Returns a set of items read, number of lines processed, is iterator fully read.
    """
    set1, l = set(), 0
    while batch := tuple(islice(iterator, batch_size)):
        l += len(batch)
        set1.update((url_preprocess(s) for s in batch))
        mem = psutil.Process().memory_info().rss
        if debug: print(mem / 2**30, len(set1)/10**6, file=sys.stderr)
        if mem > mem_limit:
            return set1, l, False
    return set1, l, True

def read_portion(iterator, mem_limit, batch_size=10**6, debug=False):
    """
    From iterator reads items into a set while there are items available and
    the memory consumption of the process stays within mem_limit. 
    Returns a set of items read.
    """
    set1 = set()
    while True:
        set1.update((s.strip() for s in islice(iterator, batch_size)))
        try:
            set1.add(next(iterator))
        except StopIteration:
            return set1
        mem = psutil.Process().memory_info().rss
        if debug: print(mem / 2**30, len(set1)/10**6)
        if mem > mem_limit:
            return set1


def get_interval_estimate(hll, p):
    cardinality_estimate = hll.cardinality()
    if cardinality_estimate < 5 / 2 * 2 ** p:
        print(
            f'WARNING: the estimated cardinality {cardinality_estimate} < {5 / 2 * 2 ** p}, HyperLogLog is biased and its relative error estimates are incorrect! Decrease p.',
            file=sys.stderr)
    rel_err = 1.04 / sqrt(
        2 ** p)  # according to Wikipedia this estimate is for HyperLogLog with all corrections, but from the HLL code it seems not all of them are implemented (compare alpha calculation)
    return cardinality_estimate * (1 - rel_err), cardinality_estimate * (1 + rel_err), cardinality_estimate, rel_err


def intersect(file1, file2, mem_limit=5 * 2 ** 30, domain_level=False, debug=False, p=23):
    """
    Reads urls from file1 in batches such that the memory consumption does not significantly exceeds mem_limit.
    For each batch, reports the number of urls/domains read, the number of unique urls/domains among them,
    and the number of unique urls/domains in file2 that are present in this batch.
    """
    if domain_level:
        url_preprocess = lambda url: url.strip().split('//')[-1].split('/')[0]
    else:
        url_preprocess = lambda url: url.strip()

    if p > 0: hll = HyperLogLog(p, sparse=False)
    intersection = set()
    part = -1
    with gzip.open(file1, 'rt', encoding='utf-8') if file1.endswith('gz') else open(file1, 'rt',
                                                                                    encoding='utf-8') as inp:
        while True:
            set1, l, finished = read_portion1(inp, mem_limit, url_preprocess=url_preprocess, debug=debug)
            part += 1
            if not set1: break
            ss = set_file_intersection(set1, file2, url_preprocess=url_preprocess)
            intersection.update(ss)

            if p > 0:
                hll1 = HyperLogLog(p, sparse=False)
                for s in set1:
                    hll1.add(s)
                hll.merge(hll1)
                est_min, est_max, est, rel_err = get_interval_estimate(hll1, p)
                print(
                    f'HLL unique lines estimate real error is {(est - len(set1)) / est}, theoretic error is {rel_err}',
                    file=sys.stderr)
                if len(set1) < est_min or len(set1) > est_max:
                    print('WARNING: real cardinality is outside of the interval estimate! ', file=sys.stderr)

            print(f'{len(ss)} lines from {file2} found in portion of {len(set1)}/{l} unique/total lines of {file1}',
                  file=sys.stderr)
            print('lines', f'{file1} part{part}', '-', l, sep='\t')
            print('unique lines', f'{file1} part{part}', '-', len(set1), sep='\t')
            print('intersection', f'{file1} part{part}', file2, len(ss), sep='\t')
            del set1
    print('Overlap size:', len(intersection), file=sys.stderr)
    print('intersection', file1, file2, len(intersection), sep='\t')

    if p > 0:
        est_min, est_max, _, _ = get_interval_estimate(hll, p)
        print(f'unique lines estimate: ({est_min}, {est_max})', file=sys.stderr)
        print('unique lines estimate', file1, '-', f'({est_min}, {est_max})', sep='\t')


fire.Fire(intersect)
