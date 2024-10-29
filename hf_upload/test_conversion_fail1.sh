#!/bin/bash
#for lang in kon_Latn; do
for lang in bam_Latn uij_Arab; do
    wget -P ${lang} https://data.hplt-project.org/two/cleaned/${lang}/1.jsonl.zst
    python hf_upload_lang.py ${lang} nikolare/HPLT2.0_cleaned ./cache
done

