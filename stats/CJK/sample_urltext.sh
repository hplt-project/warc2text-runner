DIR=$1
FOUT=$2

find $DIR -path '*/zh/url.gz' | parallel --eta --line-buffer "paste <(zcat {}) <(zcat {//}/text.gz) | perl -ne 'print if (rand() < 0.00001)'  " >$FOUT

