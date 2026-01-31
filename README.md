# warc2text-runner
NB! For the latest version of the HPLT text extraction pipelines used for HPLT v4 please refer to the 
[HPLT-textpipes repository](https://github.com/hplt-project/HPLT-textpipes/).

This repository contains code for the earlier stages (extracting textual data from WARC files) of the text processing 
pipelines used to create versions 1-3 of the [HPLT monolingual datasets](https://hplt-project.org/) and auxiliary code 
mostly related to data analysis. The repository is mainly of historical interest, some parts may be outdated and documentation quality vary.

Instructions for reproduction of text extraction from HPLT versions 1-3:
- [HPLT v3](three/README.MD)
- [HPLT v2](two/README.MD)
- [HPLT v1](one/README.md).

Auxiliary code:
- [Types and sizes of WARC records](warctypes/README.md)
- [Benchmarking formats for storing data extracted from WARCs (HPLT v1)](formats_test/README.md)
- [HuggingFace Upload Scripts (HPLT v2)](hf_upload/README.md)
- [Analysis of the relationship between TLDs and detected languages](labeling)
- [Analysis of overlap between different crawls](overlap)
- [Preliminary analysis for robotstxt filtering](robotstxt)
- [Various scripts to create samples from HPLT](sample/README.md)
- [Code that calculates various statistics for HPLT datasets and calculated statistics itself](stats)

# Acknowledgements

This project has received funding from the European Union’s Horizon Europe research and innovation programme under grant agreement No 101070350 and from UK Research and Innovation (UKRI) under the UK government’s Horizon Europe funding guarantee [grant number 10052546]
