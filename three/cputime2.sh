LOGDIR=$1
echo "real time from time, hours:"
grep real $LOGDIR/*out >realtime_time.tsv
python -c "import pandas as pd; print(pd.to_timedelta(pd.read_csv('realtime_time.tsv', header=None, sep='\t')[1]).sum().total_seconds() / 3600)"
