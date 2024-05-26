find . -name "lang.zst"|parallel  --eta "mkdir -p ../sample0.01_sample0.001/{//}; paste <(zstdcat {}) <(zstdcat {//}/metadata.zst) <(zstdcat {//}/text.zst) <(zstdcat {//}/html.zst)|perl -ne 'print if (rand() < 0.001)'|sed 's/}\t{/,/g'|zstd >../sample0.01_sample0.001/{//}/{#}.zst"
for x in *; do zstdcat $x/*/*zst |zstd >$x/all.zst; done

