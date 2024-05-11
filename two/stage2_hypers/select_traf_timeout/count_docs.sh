#!/bin/bash
PATH=$1

find $PATH -name "metadata.zst"|parallel --eta -j250 -N1 --line-buffer "zstdcat {}|wc -l" > doc_cnts.txt

