mkdir -p sample100
for x in wide CC; do zstdcat ../../sample0.01_sample0.001/${x}*/all.zst |shuf -n 100 >sample100/${x}.zst; done
for x in wide CC; do mkdir -p sample100/$x; zstdcat ./sample100/$x.zst|parallel --keep-order --pipe -N 1 "jq -r .h >sample100/$x/{#}.html"; done
for x in wide CC; do mkdir -p sample100/$x; zstdcat ./sample100/$x.zst|parallel --keep-order --pipe -N 1 "jq -r .t >sample100/$x/{#}.txt"; done
