LOGDIR=$1
echo "real time from time, hours:"
grep real $LOGDIR/*out >realtime_time.tsv
python -c "import pandas as pd; df=pd.read_csv('realtime_time.tsv', header=None, sep='\t'); df[1]=pd.to_timedelta(df[1]); print(df[1].sum().total_seconds() / 3600);print(df.groupby(0)[1].sum().apply(lambda td:td.total_seconds()/3600).describe(percentiles=[.01, .05, .25, .5, .75, .95, .99]))"
