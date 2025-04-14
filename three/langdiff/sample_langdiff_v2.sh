D1=$1
D2=$2

#bash combine_textlang_123.sh $D1 $D2 combined3

python ../../sample/stratified_sample.py --fcol2group="" --outdir=v4_samples/lang-other sample combined4_withmetadata/*/*/lang_1.zst &
python ../../sample/stratified_sample.py --fcol2group="" --outdir=v4_samples/other-lang sample combined4_withmetadata/*/*/lang_2.zst &
#python ../../sample/stratified_sample.py --fcol2group="" --outdir=v3_samples/lang-same sample combined3/*/*/lang_same.zst &
