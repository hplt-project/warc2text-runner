
DS=$1
OUTDIR=$2
mkdir -p $OUTDIR
export HF_HOME=/nird/datalake/NS8112K/hf_home
export HF_HUB_ETAG_TIMEOUT=120

python -c "import datasets; print('\n'.join(datasets.get_dataset_config_names('$DS')))" >$OUTDIR/configs.txt

cat $OUTDIR/configs.txt | parallel -j 3 --eta --joblog $OUTDIR/joblog "python hf_size.py $DS {} 1>$OUTDIR/{#}.out 2>$OUTDIR/{#}.err" 

