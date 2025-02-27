echo "from sacct, hours:"
sacct -X --starttime 2025-02-26T22:57:40 --format=TotalCPU,CPUTime,Elapsed,start,end,JobID,Partition,Account, >cputime_sacct.tsv
python -c "import pandas as pd; print(pd.read_csv('cputime_sacct.tsv', sep=' +', engine='python')[1:][['CPUTime','Elapsed']].replace('-',' days ',regex=True).apply(pd.to_timedelta).sum().apply(lambda ts: ts.total_seconds()/3600).to_string())"

echo "real time from time, hours:"
grep real sample_twoenv/*out >realtime_time.tsv
python -c "import pandas as pd; print(pd.to_timedelta(pd.read_csv('realtime_time.tsv', header=None, sep='\t')[1]).sum().total_seconds() / 3600)"
