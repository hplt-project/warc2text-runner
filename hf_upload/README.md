# HuggingFace Upload Scripts
OUTDATED! These scripts were created for HPLT v2, for other versions at least the description of features in [this script](hf_upload_lang.py) should be modified.

This directory contains scripts for uploading language-specific datasets to the Hugging Face Hub. 
The main script, `hf_upload.sh`, takes a list of paths to the language-specific directories. 
Then it runs `hf_upload_lang.py` in parallel across languages to load the data from compressed JSONL (`.zst`) files, 
convert it and push it to the HuggingFace repository.

# Observations
Storing data in the converted format requires about 4x more disk space. E.g., for the cleaned version:
* the original size is 15 TB --> the size of the HF cache dir after downloading all languages is 57 TB
* for English 5.7 TB --> 19 TB
* for Russian 1.7 TB --> 7.0 TB
* for Kazakh 4.3 GB --> 21 GB

