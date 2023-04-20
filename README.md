# warc2text-runner
Scripts for parallelized extraction of plain texts from WARC archives. Aiming at common and reproducible extraction approach.

## Install
* Install warc2text from https://github.com/bitextor/warc2text
	* later will move to Easybuild
	* for CESNET currently using [this recipe](https://github.com/jelmervdl/warc2text/blob/build-cesnet/Dockerfile)

## Run
```sh
./run_warc2text.sh ../wide15-sample300/ test_filtered 250 ./
```
takes WARCs from **../wide15-sample300/**, saves extracted texts and urls to **test_filtered** and logs to **test_filtered_logs**, performs extraction in 250 parallel processes, filters documents using filters from this repository.

To run without filters:
```sh
./run_warc2text.sh ../wide15-sample300/ test_filtered 250
```

## Calculate language statistics
```sh
cd stats
bash text_stats.sh ../test_filtered ../test_filtered_stats 250
```
calculates statistics for texts in **../test_filtered** extracted by warc2text (number of bytes, words as reported by wc, newlines and documents for each language) and saves it to **../test_filtered_stats** in .tsv format. Processes texts in 250 parallel processes. Additionally generates basic plots for some of these metrics and saves to the same folder.

## Collected statistics and plots
Language statistics was calculated for [cc40](stats/cc40_filtered_stats), [wide00015](stats/wide00015_filtered_stats) and [wide00017](stats/wide00017_filtered_stats)
For generating custom plots comparing different statistics for several languages and datasets you may want start with [this notebook](stats/lang-stats-comparison.ipynb ).