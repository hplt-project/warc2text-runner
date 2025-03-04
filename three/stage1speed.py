import pandas as pd
from pathlib import Path
import multiprocessing as mp
from tqdm import tqdm
import re
import fire

def file_size(path): 
    return Path(path).stat().st_size


def read_tasks(task_dir, max_warcs):
    tdf = pd.read_csv(task_dir/'tasks.args.gz', sep=' ', names=list(range(max_warcs+5)), header=None)

    warcs_ser = tdf.loc[:,4:].apply(lambda r: [e for e in r if not pd.isnull(e)], axis=1)
    tdf = tdf.drop(columns=[0]+list(tdf.columns[4:]))
    tdf['warcs'] = warcs_ser
    tdf = tdf.rename(columns={1:'batch',2:'outdir', 3:'indir'})
    print(len(tdf), 'tasks')
    tdf = tdf.explode('warcs')
    print(len(tdf), 'WARC files')
    with mp.Pool(30) as pool:
        results = pool.map(file_size, tqdm(list(tdf.indir + '/' + tdf.warcs)))
    
    tdf['size'] = results
    return tdf


# In[4]:


def read_logs(logs_dir):
    pat = re.compile(r'(?:hostname: (?P<hostname>.*))|(\[(?P<start>.*)\] \[info\] (?:.*Processing (?P<warcs>.*)|(?P<finished>elapsed)))')
    
    dfs = []
    for p in tqdm(list(logs_dir.glob('*_logs/*.stderr'))):
        with open(p, 'r') as inp:
            q = [match.groupdict() for l in inp if (match := pat.match(l))]
            hostname = q[0].get('hostname')
            if hostname:
                q = q[1:]
            else:
                hostname = 'unknown hostname'
                
            if q[-1]['finished']:
                finished = q[-1].get('start')
                q = q[:-1]
            else:
                finished = None
    
            df = pd.DataFrame(q).drop(columns=['finished'])
            df['hostname'] = hostname
            df['start'] = pd.to_datetime(df.start)
            df['end'] = df['start'].shift(-1)
            df.iloc[-1,-1] = finished
            df['dur_min'] =  (df.end.fillna(pd.Timestamp.now())-df.start)
            
            df['outdir'] = str(p.parent).replace('_logs','')
            dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)
    return df



# task_dir = Path('/home/hplt/hplt/three/code/warc2text-runner/three/cesnet_ia')
# logs_dir = Path('/home/hplt/hplt/three/log_html')

#task_dir = Path('/home/hplt/hplt/three/code/warc2text-runner/three/cesnet_cc1')
#logs_dir = Path('/home/hplt/hplt/three/html_cesnet_cc1/')

def main(task_dir, logs_dir, freq='10min', max_warcs=1000):
    task_dir = Path(task_dir)
    logs_dir = Path(logs_dir)
    #max_warcs = 1000  # specify batch size here, required for correct loading with pandas
    #freq = '10min'  # frequency for the speed grid

    # Load warc sizes from cache or compute
    tdf_path = Path(task_dir)/'warc_size.tsv'
    if not tdf_path.exists():
        tdf = read_tasks(task_dir, max_warcs)
        tdf.to_csv(tdf_path, sep='\t', index=False)
    tdf = pd.read_csv(tdf_path, sep='\t')

     # Load logs
    ldf = read_logs(logs_dir)
    ldf.outdir = ldf.outdir.str.replace('log_', '')

   # Merge warc sizes and processing time
    df = ldf.merge(tdf, how='inner',on=['outdir','warcs'])
    assert len(df) == len(ldf), f'{len(df)}!={len(ldf)}'

    # Compute speed, for currently running warcs estimate min speed as 0 and max speed as if they have just finished
    df['TB/day min'] = (df['size'] / 2**40 / (df.end-df.start).dt.seconds * 3600 * 24).fillna(0.0)
    df['TB/day max'] = (df['size'] / 2**40 / df.dur_min.dt.seconds * 3600 * 24)

    def overlapping_mask(df, ts):
        return (df.start <= ts) & ((df.end > ts) | df.end.isnull())

    gdf = pd.DataFrame(pd.date_range(df.start.min(), df.end.fillna(pd.Timestamp.now()).max(), freq=freq))
    sdf = gdf[0].apply(lambda ts: df[overlapping_mask(df, ts)][['TB/day min','TB/day max']].sum())
    sdf['nwarcs'] = gdf[0].apply(lambda ts: overlapping_mask(df, ts).sum())

    # Add per-host stats
    for host in df.hostname.unique():
        df1 = df[df.hostname==host]
        sdf1 = gdf[0].apply(lambda ts: df1[overlapping_mask(df1, ts)][['TB/day min','TB/day max']].sum())
        sdf1['nwarcs'] = gdf[0].apply(lambda ts: overlapping_mask(df1, ts).sum())
        sdf1.rename(columns={c:f'{host}:{c}' for c in sdf1.columns}, inplace=True)
        sdf = pd.concat([sdf,sdf1], axis=1)

    sdf['ts'] = gdf[0]
    sdf.to_csv(task_dir/'speed.tsv', sep='\t', index=False)
    sdf.describe().to_csv(task_dir/'speed_stats.tsv', sep='\t', index=False)

    mdf = tdf.merge(df[['outdir','warcs','end']], how='left', on=['outdir','warcs'])

    print(f"Running for: {df.end.max() - df.start.min()}")
    print(f"{mdf[mdf['end'].isnull()]['size'].sum() / 2**40} TB out of {mdf['size'].sum() / 2**40} TB left")

    g = sdf[[c for c in sdf.columns if ':' not in c]].plot(x='ts', rot=90, grid=True)
    g = g.legend(loc='center left',bbox_to_anchor=(1.0, 0.5)).get_figure()
    g.savefig(task_dir/'speed-total.pdf')

    g = sdf[[c for c in sdf.columns if ':' in c or c=='ts']].plot(x='ts', rot=90, grid=True)
    g = g.legend(loc='center left',bbox_to_anchor=(1.0, 0.5)).get_figure()
    g.savefig(task_dir/'speed-pernode.pdf')

    g = sdf[sdf.ts.describe().loc['75%'] <= sdf.ts][[c for c in sdf.columns if ':' in c or c=='ts']].plot(x='ts', rot=90, grid=True)
    g = g.legend(loc='center left',bbox_to_anchor=(1.0, 0.5)).get_figure()
    g.savefig(task_dir/'speed-pernode-lastquarter.pdf')


fire.Fire(main)
