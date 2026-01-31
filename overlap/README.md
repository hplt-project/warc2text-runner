# Overlap Analysis Scripts

This directory contains scripts and notebooks for analyzing the overlap between crawls using probabilistic data structures.
There scripts that calculate overlap in terms of URLs, domains and also texts (ngrams).

# Installation
For using SetSketch install sketch library (https://github.com/dnbaker/sketch):
```
git clone --recursive https://github.com/dnbaker/sketch && cd sketch/python && python3 setup.py build_ext -j4 && python3 setup.py install
```

For using overlap.py install HLL:
```
pip install HLL
```