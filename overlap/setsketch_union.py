import sketch_ds
from pathlib import Path
import fire

def union(sketch_dir, outpath):
    ss_res = None
    for p1 in Path(sketch_dir).glob('*.setsketch'):
        ss = sketch_ds.setsketch.CSetSketch(str(p1)) 
        print('%e' % ss.report(), p1)
        ss_res = ss if ss_res is None else ss_res.union(ss)
    ss_res.write(outpath)
    print('%e' % ss_res.report(), 'total size')

fire.Fire(union)
