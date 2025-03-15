## Resiliparse

fast, but [not removing much boilerplate](https://github.com/MariaFjodorowa/warc2text-runner/tree/main/two/sample100/resili) 

## Preliminary speed comparison

All in one process only, including conversion to Markdown

TLDR: for trafilatura, fallback influences more than tables 

| Method                                                 | seconds for 100 documents |
|--------------------------------------------------------|---------------------------|
| Resiliparse default                                    | 0.395                     |
| Resiliparse main_content True                          | 0.405                     |
| Trafilatura with tables, html+pyhtml2md, with fallback | 3.299                     |
| Trafilatura with tables, html+pyhtml2md, no fallback   | 2.297                     |
| Trafilatura with tables, markdown, with fallback       | 3.64                      |
| Trafilatura with tables, markdown, no fallback         | 1.853                     |
| Trafilatura, no tables, markdown, no fallback          | 1.931                     |
|Trafilatura 1.8, no tables, txt, with fallback| 11.761|

## Markdown and tables

### Markdown can be done with Trafilatura only or with Trafilatura + pyhtml2md, or with Resiliparse + pyhtml2md

### Markdown including tables can only be done reliably with Trafilatura with fallback + pyhtml2md

Pros of Markdown:

- [longer documents are more readable](https://github.com/MariaFjodorowa/warc2text-runner/blob/main/two/sample100/traf/traf-markdown-tables-True-no_fallback-True/IS_TABLE-61-traf-markdown-tables-True-no_fallback-True.md)
- possible to train models that output pretty formatted tables, [lists](https://github.com/MariaFjodorowa/warc2text-runner/blob/main/two/sample100/traf/traf-html-tables-True-no_fallback-True/55-traf-html-tables-True-no_fallback-True.md), [code](https://github.com/MariaFjodorowa/warc2text-runner/blob/main/two/sample100/traf/traf-markdown-tables-True-no_fallback-True/56-traf-markdown-tables-True-no_fallback-True.md)
- [documents with emodjis look better](https://github.com/MariaFjodorowa/warc2text-runner/blob/main/two/sample100/traf/traf-markdown-tables-True-no_fallback-True/18-traf-markdown-tables-True-no_fallback-True.md)

Cons of Markdown:

- possible lost spaces and newlines in formulas (although not sure formulas were readable w/o Markdown)
- possible redundant "|"s if table was not fully recognized (especially from Trafilatura with native Markdown)

Pros of table extraction:

- users like it

Cons of table extraction:

- most tables are removed as boilerplate anyway, e.g. in the table below "empty" is where all text was removed and "no table" is where text was extracted, but tables were judged to be boilerplate
- usefulness of the tables that are extracted properly is in question (see docs [30](https://github.com/MariaFjodorowa/warc2text-runner/blob/main/two/sample100/traf/traf-html-tables-True-no_fallback-False/30-traf-html-tables-True-no_fallback-False.md), [15](https://github.com/MariaFjodorowa/warc2text-runner/blob/main/two/sample100/traf/traf-html-tables-True-no_fallback-False/15-traf-html-tables-True-no_fallback-False.md), [3](https://github.com/MariaFjodorowa/warc2text-runner/blob/main/two/sample100/traf/traf-html-tables-True-no_fallback-False/3-traf-html-tables-True-no_fallback-False.md))

Documents with tables (those containing `<td>` tag):

| N  | Trafilatura native markdown (with fallback) | Trafilatura + pyhtml2md (with fallback) | Trafilatura + pyhtml2md (no fallback) | Trafilatura native markdown (no fallback) |
|----|---------------------------------------------|-----------------------------------------|---------------------------------------|-------------------------------------------|
| 1  | no table                                    | no table                                | no table                              | no table                                  
| 3  | x                                           | v                                       | v                                     | x                                         |
| 4  | no table                                    | no table                                | empty                                 | empty                                     | 
| 5  | no table                                    | no table                                | no table                              | no table                                  
| 10 | no table                                    | no table                                | no table                              | no table                                  
| 15 | x                                           | v                                       | v                                     | x                                         | 
| 30 | x                                           | v                                       | x                                     | x                                         |
| 34 | empty                                       | empty                                   | empty                                 | empty                                     
| 40 | x                                           | no table                                | v                                     | x                                         
| 49 | no table                                    | no table                                | no table                              | no table                                  
| 50 | no table                                    | no table                                | empty                                 | empty                                     
| 53 | x                                           | no table                                | v                                     | x                                         
| 57 | no table                                    | no table                                | x                                     | x                                         
| 60 | x                                           | no table                                | empty                                 | empty                                     
| 61 | no table                                    | no table                                | no table                              | no table                                  
| 62 | empty                                       | empty                                   | empty                                 | empty                                     
| 64 | v                                           | x                                       | x                                     | v                                         |
| 74 | empty                                       | no table                                | empty                                 | empty                                     |
| 75 | no table                                    | no table                                | no table                              | no table                                  |
| 83 | no table                                    | no table                                | no table                              | no table                                  
| 89 | no table                                    | no table                                | empty                                 | empty                                     
| 90 | x                                           | x                                       | x                                     | x                                         
| 92 | no table                                    | no table                                | no table                              | no table                                  |
| 95 | x                                           | no table                                | no table                              | no table
| 97 | no table                                    | no table                                | no table                              | no table
|98| no table                                    | no table                                | x                                     |x

