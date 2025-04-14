D1=$1
D2=$2

bash combine_textlang_12.sh $D1 $D2 byoldlang
bash combine_textlang_12.sh $D2 $D1 bynewlang

python ../../sample/stratified_sample.py --fcol2group="" --outdir=lang-other sample byoldlang/*/*/lang_changed.zst
python ../../sample/stratified_sample.py --fcol2group="" --outdir=other-lang sample bynewlang/*/*/lang_changed.zst
