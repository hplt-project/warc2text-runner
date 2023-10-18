from fire import Fire
import sketch_ds
import mmh3

def run(step, cnt=4*10**11, m=2**18):
    hll = sketch_ds.setsketch.CSetSketch(m)
    for c,i in enumerate(range(step, step*cnt+1, step)):
        o,_ = mmh3.hash64(str(i), seed=0, signed=False)
        hll.add(o)
#        hll.addh(str(i))
        if (c+1) & c == 0:  # c+1 is a power of 2
            hll.write(f'setsketch_simulation/{step}_{i}')
                        
Fire(run)                        
