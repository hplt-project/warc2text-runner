cat ../sample_run4.1/sample0.002_bs10.paths|parallel --eta -j10 -N1 --line-buffer "zstdcat {//}/text.zst|jq -r .dur"|shuf -n 1000000 >dur_nofallback.txt
