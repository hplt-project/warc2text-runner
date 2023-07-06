import pandas as pd
import fire
import sys

def rectypes(finname, foutname):
    with sys.stdin if finname=='-' else open(finname, 'rt') as inp:
        df = pd.DataFrame.from_records(( dict(e.lower().split(':', maxsplit=1) for e in q.strip().split('\t')[:2]) for q in inp ))
    df.to_csv(foutname, sep='\t', index=False)


def contenttypes(finname, foutname):
    with sys.stdin if finname=='-' else open(finname, 'rt') as inp:
        df = pd.DataFrame.from_records(( dict(e.lower().split(':', maxsplit=1) for e in q.strip().split('\t')[-2:]) for q in inp ))
    df.to_csv(foutname, sep='\t', index=False, errors='backslashreplace') # warc files occasionally contain non-utf8 values



if __name__ == '__main__':
      fire.Fire()

