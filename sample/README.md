# Random sampling of documents stratified by language
Documents for different languages are located in different folders, thus, we rely on 
```shuf -n 1000000```, which does reservoir sampling from stdin and passed all data for each language separately. 
[See commands](sample.sh.history) used to create a sample with 1M documents for each language. Finally, samples were 
shuffled, which make the first N lines a uniform sample from the full data on its own.

# Random sampling of documents stratified by language and collection group.
In the cleaned version of 2nd release of HPLT data we merged crawls into collections, which combine crawls
from the same year for CC crawls and directly correspond to IA crawls. We further introduce 9 collection groups, which 
combine crawls of similar type and age, [see this mapping](collection2group.tsv). Samples were 
shuffled, which make the first N lines a uniform sample from the full data on its own. 
[See commands](strat_sample.sh.history) used to create samples stratified by language and group.

### Notes on usage of samples
Notice that the number of examples for some languages and groups can be smaller than the target number, this means that
the whole dataset contains fewer examples and the sample contains all of them. E.g. in the 1K sample
stratified by language and collection group about 30% of language-group pairs have less than 1K examples.

These samples are stratified, meaning one can easily estimate different quantities for each strata separately.  
To draw estimates for the whole dataset you may want to take proportions of different stratas into account. If you work
with samples stratified by language see [the total size of data extracted for each language](../stats/release2.0_cleaned_stats_mr/stats-1.tsv).
If you work with samples stratified by language and group consider
[the total size of data extracted for each language from each crawl](../stats/release2.0_cleaned_stats_mr/stats.tsv) and
[the mapping from collections to groups](collection2group.tsv).


### Notes on implementation
Documents from different groups but the same language are mixed in the same files. It is unclear how an 
efficient and simple solution with ```shuf``` for this case can look like. Instead, we [implemented stratified sampling](stratified_sample.py)
using one reservoir per group. For efficiency, the algorithm is adapted for batched update of a reservoir. 

### Notes on efficiency
Tests have shown that the speed of [stratified_sample.py](stratified_sample.py) is comparable to the speed of the UNIX 
```wc``` utility when it calculates the number of words among other statistics (```wc -l``` which calculates only the
number of lines is much faster).
For all languages except for Russian and English sampling from all data was finished in about 20h. For Russian and 
English we created a stratified sample from the corresponding 1M per-language samples. Since in the 1M sample each
group is represented with more than 1K examples, the result is identical to sampling from the full data. When using
this optimization, check that the resulting sample contains 1K examples for each group, otherwise the result will be
not identical to sampling from full data!