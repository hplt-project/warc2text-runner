# warc2text-runner
Scripts for parallelized extraction of plain texts from WARC archieves. Aiming at common and reproducible extraction approach.

## Install
* Install warc2text from https://github.com/bitextor/warc2text
* To use filters from ParaCrawl clone https://github.com/paracrawl/cirrus-scripts

## Run
```./run_warc2text.sh ../wide15-sample300/ test_filtered 250 ../cirrus-scripts/```
takes WARCs from **../wide15-sample300/**, saves extracted texts and urls to **test_filtered** and logs to **test_filtered_logs**, performs extraction in 250 parallel processes, filters documents using filters from **../cirrus-scripts/**

To run without filters:
```./run_warc2text.sh ../wide15-sample300/ test_filtered 250```
