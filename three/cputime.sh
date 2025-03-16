START="2025-03-16T00:35:40"

echo "from sacct, hours:"
sacct -X --starttime $START --format=TotalCPU,CPUTime,Elapsed,start,end,JobID,Partition,Account, >cputime_sacct.tsv
python -c "import pandas as pd; print(pd.read_csv('cputime_sacct.tsv', sep=' +', engine='python')[1:][['CPUTime','Elapsed']].replace('-',' days ',regex=True).apply(pd.to_timedelta).sum().apply(lambda ts: ts.total_seconds()/3600).to_string())"


