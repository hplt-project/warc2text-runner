#!/bin/bash
# Feed content of text.zst to the stdin
jq -c .traferr | sort | uniq -c
