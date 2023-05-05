import gzip
import psutil
from itertools import islice
import sys
import fire


def set_file_intersection(set1, file2, url_preprocess=lambda url: url.strip):
    """
    Returns intersection between lines if file2 and set1. Lines of file2 are preprocessed with url_preprocess.
    """
    with gzip.open(file2, 'rt', encoding='utf-8') if file2.endswith('gz') else open(file2, 'rt', encoding='utf-8') as inp:
        intersection = set1.intersection((url_preprocess(s) for s in inp))
    return intersection


def read_portion1(iterator, mem_limit, batch_size=10**8, debug=False, url_preprocess=lambda url: url.strip):
    """
    From iterator reads items into a set while there are items available and
    the memory consumption of the process stays within mem_limit.
    Preprocesses items with url_preprocess.
    Returns a set of items read.
    """
    set1, l = set(), 0
    while batch := tuple(islice(iterator, batch_size)):
        l += len(batch)
        set1.update((url_preprocess(s) for s in batch))
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


def intersect(file1, file2, mem_limit=5 * 2 ** 30, domain_level=False, debug=False):  # 1 GB memory limit
    """
    Reads urls from file1 in batches such that the memory consumption does not significantly exceeds mem_limit.
    For each batch, reports the number of urls/domains read, the number of unique urls/domains among them,
    and the number of unique urls/domains in file2 that are present in this batch.
    """
    if domain_level:
        url_preprocess = lambda url: url.strip().split('//')[-1].split('/')[0]
    else:
        url_preprocess = lambda url: url.strip()

    intersection = set()
    part = -1
    with gzip.open(file1, 'rt', encoding='utf-8') if file1.endswith('gz') else open(file1, 'rt',
                                                                                    encoding='utf-8') as inp:
        while True:
            set1, l = read_portion1(inp, mem_limit, url_preprocess=url_preprocess, debug=debug)
            part += 1
            if not set1: break
            ss = set_file_intersection(set1, file2, url_preprocess=url_preprocess)
            intersection.update(ss)
            print(f'{len(ss)} lines from {file2} found in portion of {len(set1)}/{l} unique/total lines of {file1}',
                  file=sys.stderr)
            print('lines', f'{file1} part{part}', '-', l, sep='\t')
            print('unique_lines', f'{file1} part{part}', '-', len(set1), sep='\t')
            print('intersection', f'{file1} part{part}', file2, len(ss), sep='\t')
            del set1
    print('Overlap size:', len(intersection), file=sys.stderr)
    print('intersection', file1, file2, len(intersection), sep='\t')


fire.Fire(intersect)
