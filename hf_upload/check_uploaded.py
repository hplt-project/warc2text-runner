from fire import Fire
import datasets

def check(path):
    configs = datasets.get_dataset_config_names(path)
    print(len(configs), 'configs:', configs)
    for c in configs:
        b = datasets.load_dataset_builder(path, c)
        print(c, 'None' if b.info.splits is None else '\t'.join([f'{k}\t{v}' for k,v in b.info.splits.items()]), sep='\t')


Fire(check)
