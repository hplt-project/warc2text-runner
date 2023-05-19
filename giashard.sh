#!/bin/bash
set -euo pipefail
ulimit -n 16348

BATCHSIZE=128

function batch {
	count=0
	line=()
	while read word; do
		line+=("$word")
		if [ "${#line[@]}" -eq $1 ]; then
			echo "${line[@]}"
			line=()
		fi
	done

	if [ "${#line[@]}" -gt 0 ]; then
		echo "${line[@]}"
	fi
}

# Make sure the output directory exists
mkdir -p $1-shards/

# Make sure we haven't processed this language yet (mv would fail otherwise anyway)
test ! -d $1-shards/$2

# Find all directories for a single language ($2), batch it into groups of $BATCHSIZE, and pivot it
find $1 -mindepth 2 -maxdepth 2 -type d -name $2 |
	sort |
	batch $BATCHSIZE |
	parallel \
	-N1 \
	--colsep ' ' \
	--halt now,fail=1 \
	--tagstring '[{#}]' \
	--group \
	giashard-static \
		-d $HOME/domain-suffixes.txt \
		-f text,url \
		-b 8192 \
		-o "$1-shards/$2.$$.{#}" \
		"{}"

# Combine parallel runs
mkdir -p $1-shards/$2.$$

parallel \
	--verbose \
	-N1 \
	"giamerge-static -f text,url,source -b $(( 3 * 8192 )) -o $1-shards/$2.$$/{}/ $1-shards/$2.$$.*/{}/*/" \
	::: {0..255}

# Fix filenames
for batch in $1-shards/$2.$$/*/*/; do
	mv ${batch}{text,plain_text}.gz
done

# Move final output to permanent path
mv $1-shards/$2{.$$,}

# Remove intermediate data
rm -r $1-shards/$2.$$.*/

