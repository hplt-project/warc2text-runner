import sys
import random
from fire import Fire
import pandas as pd
import io 
from smart_open import open
import ujson as json

def write(json_bytestring_list):
    sys.stdout.buffer.write(b'{')
    sys.stdout.buffer.write(b','.join(s.strip(b'{}\n') for s in json_bytestring_list))
    sys.stdout.buffer.write(b'}\n')


def sample(size, fcollectionprobs, strat_field='tld', file='-', *files):
    c2cnt = pd.read_csv(fcollectionprobs, sep='\t', header=None).set_index(1)[0]
    c2prob = size / c2cnt
    c2prob = c2prob.to_dict()
#    print(c2prob)
    files = [file] + list(files)
    inps = [sys.stdin.buffer if f=='-' else io.BufferedReader(open(f, 'rb')) for f in files]
    for x in zip(*inps):
        c = json.loads(x[0].decode('utf-8', errors='replace').strip())[strat_field]
        if random.random() < c2prob.get(c,0):
            write(x)


Fire(sample)
