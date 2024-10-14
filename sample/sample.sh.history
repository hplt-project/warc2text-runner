find ~/hplt/public/two/cleaned/ -name "???_????"|parallel  --eta --line-buffer  -j 200 "zstdcat {}/*zst | shuf -n 1000000 >{/}"
mkdir per_lang_1M
find -name "???_????" | parallel --eta --line-buffer -j 200 "shuf {} | zstd -o per_lang_1M/{/}.shuf.zst"
rm ???_????


for x in per_lang_1M/*.zst; do echo $x;  python split_by_collection.py $x per_lang_group/$(basename $x .shuf.zst) collection2group.tsv; done
for x in per_lang_1M/*.zst; do echo $x;  python split_by_collection.py $x per_lang_collection/$(basename $x .shuf.zst) ; done



