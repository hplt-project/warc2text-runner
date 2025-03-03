# Third HPLT data release
Here we describe differences with the second HPLT data release. For explanations and the unchanged parts refer to 
[the second release README](../two/README.MD) 

## Stage1 (a.k.a. warc2html)
### Install
* Install warc2text 1.3.0 from https://github.com/bitextor/warc2text. 
* Install warc2text-runner:
```aiignore
pip install .
```

### Run
1. Compile a list of crawls to process. Before running the script, change path templates inside.
```commandline
./find_crawls.sh
```

2. Generate a list of processing tasks from the list of crawls, e.g. for third-iteration CC crawls on NIRD:
```commandline
generate_tasks.sh nirdl_three_cc 1000 ~/hplt/three/html 
```

3. Run HTML extraction with warc2text. E.g. for NIRD:
```commandline
run_warc2html_remote.sh nirdl_three_cc 250 "--sshlogin 1/nird-d,1/nird-c"
```
To run locally specify the empty string as the 3rd argument:
```commandline
run_warc2html_remote.sh nirdl_three_cc 250 ""
```
NB! On NIRD ssh connection to other node occasionally dropped, thus, we preferred splitting crawls manually and running
on each node locally. On CESNET the first remote option works well. 
