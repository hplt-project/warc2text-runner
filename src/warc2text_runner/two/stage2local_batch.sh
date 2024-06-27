#!/bin/bash
rc=0
for x in $@; do 
    echo Processing $x 1>&2  # forward everything to stderr to interleave correctly with error messages from stage2local.sh
    time stage2local.sh $x $(dirname $x) 250 || (rc=$? && echo "ERROR while processing $x" 1>&2)  # in bash && and || have the same priority
    echo "Current error code:" $rc 1>&2
    
done
exit $rc
