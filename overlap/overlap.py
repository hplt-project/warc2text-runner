import gzip
import psutil
from itertools import islice
import sys
import fire


def set_file_overlap(set1, file2):
    with gzip.open(file2, 'rt', encoding='utf-8') if file2.endswith('gz') else open(file2, 'rt', encoding='utf-8') as inp:
        overlap = set1.intersection((s.strip() for s in inp))
    return overlap



def read_portion1(iterator, mem_limit, batch_size=10**6, debug=False):
    """
    From iterator reads items into a set while there are items available and
    the memory consumption of the process stays within mem_limit. 
    Returns a set of items read.
    """
    set1, l = set(), 0
    while batch := tuple(islice(iterator, batch_size)):
        l += len(batch)
        set1.update((s.strip() for s in batch))
        mem = psutil.Process().memory_info().rss
        if debug: print(mem / 2**30, len(set1)/10**6, file=sys.stderr)
        if mem > mem_limit:
            return set1, l
    return set1, l



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



def overlap(file1, file2, mem_limit = 8*2**30):  # 8 GB memory limit
    overlap = set()
    with gzip.open(file1, 'rt', encoding='utf-8') if file1.endswith('gz') else open(file1, 'rt', encoding='utf-8') as inp:
        while True:
            set1, l = read_portion1(inp, mem_limit)
            if not set1: break
            ss = set_file_overlap(set1, file2)
            overlap.update(ss)
            print( f'{len(ss)} lines from {file2} found in portion of {len(set1)}/{l} unique/total lines of {file1}')
            del set1
    print('Overlap size:', len(overlap))


fire.Fire(overlap)
