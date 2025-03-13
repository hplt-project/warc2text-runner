Pros of Markdown:

- longer documents are more readable
- possible to train models that output pretty formatted tables and lists 
- documents with emodjis look better


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

Resiliparse - does not extract tables