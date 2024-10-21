#!/bin/bash
wget -P bam_Latn https://data.hplt-project.org/two/cleaned/bam_Latn/1.jsonl.zst
python hf_upload_lang.py bam_Latn nikolare/HPLT2.0_cleaned ./cache

