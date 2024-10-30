from pyexpat import features

from datasets import load_dataset, Sequence, Value, Features
from pathlib import Path 
import fire


def upload(lang_dir, remote, cache_dir='/nird/datalake/NS8112K/hf_cache'):
    p = Path(lang_dir)
    part = p.name
    files = [str(f) for f in p.glob("*.zst")]
    print(f'Loading part {part} from {p}: {len(files)} files. Cache dir: {cache_dir}')
    features = Features({
        'f': Value('string'),
        'o': Value('int64'),
        's': Value('int64'),
        'rs': Value('int64'),
        'u': Value('string'),
        'c': Value('string'),
        'ts': Value('timestamp[s]'),
        'collection': Value('string'),
        'lang': Sequence(Value('string')),
        'prob': Sequence(Value('float32')),
        'text': Value('string'),
        'seg_langs': Sequence(Value('string')),
        'robotstxt': Value('string'),
        'id': Value('string'),
        'filter': Value('string'),
        'pii': Sequence(Sequence(Value('int64'))),
        'doc_scores': Sequence(Value('float32'))
    })
    ds = load_dataset('json', data_files=files, cache_dir=cache_dir, features=features)

    print(len(ds['train']))
    print(ds['train'].features)
    print(f'Pushing part {part} from {p} to {remote}')
    ds.push_to_hub(remote, part)
    print(f'Part {part} is pushed to HF!')


fire.Fire(upload)
