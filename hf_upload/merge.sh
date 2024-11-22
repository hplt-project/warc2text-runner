#!/bin/bash
# Login with ```huggingface-cli login``` before running this script!

DS=HPLT/HPLT2.0_dedup


huggingface-cli download --repo-type dataset --local-dir ./tmp/$DS $DS README.md
# remove the 'dataset_info' section
sed -z -r -e 's!\n([^a-z])!\t\1!g'  <tmp/$DS/README.md | grep -v '^dataset_info' | tr '\t' '\n' >tmp/$DS/README.md.1 
# merge subsets for one language: 
#   1. replace paths: e.g. eng_Latn_123/ to eng_Latn*/
#   2. replace config names: e.g. eng_Latn_123 to eng_Latn
#   3. removing duplicated configs appeared after configs 
sed -z -r -e 's!\n !\t !g' -e 's!_?[0-9]*/!*/!g' -e 's!_[0-9]+!!g'  <tmp/$DS/README.md.1 | uniq | tr '\t' '\n' >tmp/$DS/README.md.2

huggingface-cli upload --repo-type dataset $DS tmp/$DS/README.md.2 README.md
