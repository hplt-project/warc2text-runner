# warc2text-runner
Scripts for parallelized extraction of plain texts from WARC archives. Aiming at common and reproducible extraction approach.

## Install
* Install warc2text from https://github.com/bitextor/warc2text (later will move to Easybuild)
* To use filters from ParaCrawl clone https://github.com/paracrawl/cirrus-scripts

## Run
```sh
./run_warc2text.sh ../wide15-sample300/ test_filtered 250 ./
```
takes WARCs from **../wide15-sample300/**, saves extracted texts and urls to **test_filtered** and logs to **test_filtered_logs**, performs extraction in 250 parallel processes, filters documents using filters from this repository.

To run without filters:
```sh
./run_warc2text.sh ../wide15-sample300/ test_filtered 250
```
