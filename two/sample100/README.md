## Resiliparse

fast, but [not removing much boilerplate](resili) 

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

## Comments

### XML outcomes:

- [no comments opening tag](traf/traf-xml-tables-True-no_fallback-False-comments-True-formatting-True-metadata-True/8-traf-xml-tables-True-no_fallback-False-comments-True-formatting-True-metadata-True.xml)
- [boilerplate](traf/traf-xml-tables-True-no_fallback-False-comments-True-formatting-True-metadata-True/IS_COMMENTS-6-traf-xml-tables-True-no_fallback-False-comments-True-formatting-True-metadata-True.xml)
- [more boilerplate](traf/traf-xml-tables-True-no_fallback-False-comments-True-formatting-True-metadata-True/IS_COMMENTS-33-traf-xml-tables-True-no_fallback-False-comments-True-formatting-True-metadata-True.xml)
- [boilerplate may be in any language](traf/traf-xml-tables-True-no_fallback-False-comments-True-formatting-True-metadata-True/IS_COMMENTS-44-traf-xml-tables-True-no_fallback-False-comments-True-formatting-True-metadata-True.xml)
- [continuation of the main content](traf/traf-xml-tables-True-no_fallback-False-comments-True-formatting-True-metadata-True/IS_COMMENTS-38-traf-xml-tables-True-no_fallback-False-comments-True-formatting-True-metadata-True.xml)
- [TRUE comments!!!](traf/traf-xml-tables-True-no_fallback-False-comments-True-formatting-True-metadata-True/IS_COMMENTS-IS_TABLE-61-traf-xml-tables-True-no_fallback-False-comments-True-formatting-True-metadata-True.xml). Actually a lot of useful text. But still includes some boilerplate like "ReplyDelete"

### TXT

- [where there is no comments opening tag in XML, there is nothing in txt](traf/traf-txt-tables-False-no_fallback-False-comments-True-formatting-False-metadata-False/8-traf-txt-tables-False-no_fallback-False-comments-True-formatting-False-metadata-False.txt)
- [boilerplate looks like a usual plaintext in any language](traf/traf-txt-tables-False-no_fallback-False-comments-True-formatting-False-metadata-False/44-traf-txt-tables-False-no_fallback-False-comments-True-formatting-False-metadata-False.txt), may be difficult to filter out
- [true comments look like a regular text](traf/traf-txt-tables-False-no_fallback-False-comments-True-formatting-False-metadata-False/IS_TABLE-61-traf-txt-tables-False-no_fallback-False-comments-True-formatting-False-metadata-False.txt), they are in no way distinguished from the main body, which seems to be bad for LM

## include_formatting

makes sense also with txt output format: it turns it into markdown [(not any better as when output_format='markdown')](traf/traf-txt-tables-False-no_fallback-False-comments-False-formatting-True-metadata-True/56-traf-txt-tables-False-no_fallback-False-comments-False-formatting-True-metadata-True.txt), so it's not true that is only valuable for xml as official docstring says at the time of writing

in case of xml it preserves formatting tags like attributes of the tag [`<hi>`](https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-hi.html). Compare [files with names starting with `REND_TAG` with formatting](traf/traf-xml-tables-True-no_fallback-False-comments-True-formatting-True-metadata-False) and [without](traf/traf-xml-tables-True-no_fallback-False-comments-True-formatting-False-metadata-False).

## with_metadata

- [xml metadata](traf/traf-xml-tables-True-no_fallback-False-comments-True-formatting-True-metadata-True)
- [xml w/o metadata](traf/traf-xml-tables-True-no_fallback-False-comments-True-formatting-False-metadata-False)
- [txt metadata](traf/traf-txt-tables-False-no_fallback-False-comments-False-formatting-True-metadata-True)

## Markdown and tables

### Markdown can be done with Trafilatura only or with Trafilatura + pyhtml2md, or with Resiliparse + pyhtml2md

### Markdown including tables can only be done reliably with Trafilatura with fallback + pyhtml2md (but still not as reliably as we would wish)

Pros of Markdown:

- [longer documents are more readable](traf/traf-markdown-tables-True-no_fallback-True/IS_TABLE-61-traf-markdown-tables-True-no_fallback-True.md)
- possible to train models that output pretty formatted tables, [lists](traf/traf-html-tables-True-no_fallback-True/55-traf-html-tables-True-no_fallback-True.md), [code](traf/traf-markdown-tables-True-no_fallback-True/56-traf-markdown-tables-True-no_fallback-True.md)
- [documents with emodjis look better](traf/traf-markdown-tables-True-no_fallback-True/18-traf-markdown-tables-True-no_fallback-True.md)

Cons of Markdown:

- lost spaces and newlines in formulas, code
- lost list elements
- redundant "|"s if table was not fully recognized (especially from Trafilatura with native Markdown)

Pros of Markdown table extraction:

- users like it

Cons of Markdown table extraction:

- most tables are removed as boilerplate anyway, e.g. in the table below "empty" is where all text was removed and "no table" is where text was extracted, but tables were judged to be boilerplate
- usefulness of the tables that are extracted properly is in question (see docs [30](traf/traf-html-tables-True-no_fallback-False/30-traf-html-tables-True-no_fallback-False.md), [15](traf/traf-html-tables-True-no_fallback-False/15-traf-html-tables-True-no_fallback-False.md), [3](traf/traf-html-tables-True-no_fallback-False/3-traf-html-tables-True-no_fallback-False.md))
- Trafilatura doesn't fix non-standard source tables, and uses an own non-standard set of tags

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

