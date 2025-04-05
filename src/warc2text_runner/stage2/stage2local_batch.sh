#!/bin/bash
BASEOUTDIR=$1

rc=0
for x in ${@:2}; do 
    OUTDIR=${BASEOUTDIR}/`echo $x | sed -r 's!.*(/[^/]+/[^/]+/)[^/]+!\1!'`
    echo "Processing $x, writing to ${OUTDIR}" 1>&2  # forward everything to stderr to interleave correctly with error messages from stage2local.sh
    time stage2local.sh $x ${OUTDIR} || { rc="$?"; echo "ERROR while processing $x" 1>&2; }  # in bash && and || have the same priority
    echo "Current error code:" $rc 1>&2
    
done
exit $rc
