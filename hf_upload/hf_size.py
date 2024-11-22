import datasets
from fire import Fire
import sys

def size(ds, config, num_proc=20, cache_dir='~/hplt/hf_cache'):
    configs = datasets.get_dataset_config_names(ds)
    if config not in configs:
        print(f'config {config} not in', configs, file=sys.stderr)
    ds = datasets.load_dataset(ds,config, cache_dir=cache_dir, num_proc=num_proc)
    docs = len(ds['train'])
    chars = sum(len(e['text']) for e in ds['train'])
    print(config, chars, docs)






Fire(size)
