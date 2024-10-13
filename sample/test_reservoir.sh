seq 0 10000000 | jq -Rc '{"collection":"cc20", "v":.}'  | python stratified_sample.py sample --fcol2group=./collection2group.tsv --outdir=tmp --k=10000
jq '.v' <tmp/cc_n | python -c 'import sys; import pandas as pd; print(pd.read_csv(sys.stdin, header=None).describe())'
echo "Mean should be around 5M, 95% CI for the mean is 5M +- 2*std/100"
