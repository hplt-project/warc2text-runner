from datasets import load_dataset
from pathlib import Path 
import fire


def upload(lang_dir, remote, cache_dir='/nird/projects/NS8112K/two/cache'):
    p = Path(lang_dir)
    part = p.name
    files = [str(f) for f in p.glob("*.zst")]
    print(f'Loading part {part} from {p}: {len(files)} files. Cache dir: {cache_dir}')
    import pdb; pdb.set_trace()
    ds = load_dataset('json', data_files=files, cache_dir=cache_dir)
    print(f'Pushing part {part} from {p} to {remote}')
    ds.push_to_hub(remote, part)
    print(f'Part {part} is pushed to HF!')


fire.Fire(upload)
