# Benchmarking formats for storing data extracted from WARCs 
OUTDATED! Created for HPLT v1.

Scripts to compare different formats for storing data extracted for web archive (WARC) data.  
The primary goal is to compare the efficiency of storing data in separate, compressed files (e.g., `url.gz`, `date.gz`, `text.gz`) 
versus consolidating them into a single compressed JSON file (`singlejson.gz`).

The benchmarks measure the time taken to perform common data processing tasks, such as reading specific fields, decoding content, and preparing data for ingestion into other tools.

## Files

- `run_all.sh`: The main script that executes all benchmark tests and logs their output.
- `separatefiles2json.sh`: Converts data from separate `url.gz`, `date.gz`, and `text.gz` files to other formats.
- `compare_process_text.sh`: Benchmarks reading text data from different formats.
- `compare_process_urldate.sh`: Benchmarks reading URL and date metadata from different formats.
- `compare_process_urltext.sh`: Benchmarks reading URL and text data from different formats.
- `pipeline_overhead.sh`: Measures the overhead of adding extra steps to a processing pipeline.
- `*.log`: Log files containing the output of the benchmark scripts.
