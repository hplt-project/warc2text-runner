# Second HPLT data release
Extraction of raw texts from WARC archives is performed in two stages. In the first stage WARC files
are processed and relevant records are selected. From these records web pages in HTML format and
additional metadata are extracted and dumped to disk. This stage requires voluminous storage and
fast access to WARC files stored in two data centers but it is not computationally intensive, thus, this
stage is run on the compute nodes in the data centers directly attached to the storage with WARC
files.
The second stage consists of parsing HTML pages, removing boilerplate and extracting text in natural
language, and finally running language identification on the extracted text. This stage is significantly
more computationally intensive, thus, it is run on the LUMI cluster.

## Stage1 (a.k.a. warc2html)
### Install
* Install warc2text 1.2.0 from https://github.com/bitextor/warc2text. To reproduce what was done for the second data 
release, follow the installation method using EasyBuild. 

### Configure
The following instructions rely on the file structure and configuration of NIRD and CESNET, in particular:
1. a symlink ~/hplt in your home directory points to the project directory; e.g. for NIRD:
```commandline
ln -s /nird/datalake/NS8112K/ ~/hplt
```
2. this repository is cloned to ~/hplt/two/code/warc2text-runner;
3. passwordless access to the computing nodes 


### Run
1. Compile a list of crawls to process, e.g. see lists for [CESNET](cesnet/crawls.paths) and [NIRD](nirdl/crawls.paths).
Do this manually or adapt and run [this script](find_crawls.sh), which reflects what was done in the 2nd data release.
E.g. for NIRD just run:
```commandline
./find_crawls.sh
```

2. Generate a list of processing tasks from the list of crawls, e.g. for NIRD:
```commandline
 ./generate_tasks.sh nirdl 1000
```
This will take find all WARC files, combine them into batches of 1000 WARCs and for each batch write a command that 
processes this batch with warc2text to nirdl/tasks.args.gz

3. Run HTML extraction with warc2text. E.g. for NIRD:
```commandline
./run_warc2html_remote.sh nirdl 250 "--sshlogin 1/nird-d,1/nird-c"
```
takes tasks from nirdl/tasks.args.gz and runs warc2text on two nodes (nird-d and nird-c), in 250 parallel processes on each node.
To run locally specify the empty string as the 3rd argument:
```commandline
./run_warc2html_remote.sh nirdl 250 ""
```
At the end it reports how many nodes finished all their tasks successfully. In case of any errors, inspect joblogs for
each compute node (dumped to ./$HOSTNAME/joblog), find the failed commands and their batch ids, 
inspect stdout/stderr of warc2text for the corresponding batch ids (dumped to  ~/hplt/two/text/*_logs). 
The output HTMLs will be dumped to ~/hplt/two/text/.

## Stage2 (a.k.a. html2text)
Stage2 does text extraction with boilerplate removal (Trafilatura) and language identification (fasterText with the openLID model).
It is executed on 100 LUMI compute nodes, in 250 parallel processes on each.

### Install on LUMI
Load the required modules.
```commandline
source src/warc2text_runner/two/stage2preplumic.sh
``` 

Install with pip in a virtual environment. Use --system-site-packages to reuse 
packages installed in cray-python when possible, which may be better optimized for LUMI. 
Install only extra dependencies from two/requirements_LUMIextra.txt 
```commandline
python -m venv --system-site-packages venv
source venv/bin/activate
pip install -r two/requirements_LUMIextra.txt
pip install .  
```

### Install on other systems (not tested!)
You might want to install on your local machine or a cluster other than LUMI.
Install using pip all the requirements, including those coming from cray-python module on LUMI: 
```commandline
python -m venv venv
source venv/bin/activate
pip install -r  two/requirements_LUMIall.txt
pip install .
```

### Download the required model weights
```commandline
stage2download.sh
```

### Run on LUMI, method1: for locally located input data
```commandline
source src/warc2text_runner/two/stage2preplumic.sh
source venv/bin/activate
```

To run processing on 100 nodes:
```commandline
find <PATH TO STAGE1 OTPUTS> -name "html.zst" >portion1.paths
stage2nodeparallel.sh 100 portion1.paths
```

### Run on LUMI, method2: with input data staging
First configure rclone adding all required remote servers.
```commandline
source src/warc2text_runner/two/stage2preplumic.sh
rclone config
```
Make sure ssh-ing is passwordless. You might want to use ssh-agent to store passwords for those 
servers that require it (e.g. NIRD):  
```commandline
eval `ssh-agent`
ssh-add
```
Prepare a list of files to download if you don't have one. E.g. this will list all 
files on CESNET and NIRD that are outputs of stage1. Customize to your needs.
```commandline
cd hplt/two/code/warc2text-runner/
source src/warc2text_runner/two/stage2preplumic.sh
source venv/bin/activate
cd two/staging
./stage2listfiles.sh
```

In the first terminal run the processing script:
```commandline
cd hplt/two/code/warc2text-runner/
source src/warc2text_runner/two/stage2preplumic.sh
source venv/bin/activate
cd two/staging
./stage2wstaging1.sh nird nird_left.paths /scratch/project_465000498/two/html_staging/ 50
```

In the second terminal run the downloading script with exactly the same arguments (the last one will be ignored though):
```commandline
source src/warc2text_runner/two/stage2preplumic.sh
source venv/bin/activate
cd two/staging
lumi/stage2lumidownload_nodeparallel.sh nird nird_left.paths /scratch/project_465000498/two/html_staging/ 50 
```
The first script creates a named pipe, reads rclone log messages about newly downloaded files 
and starts a job for each html.zst downloaded. 20 is the maximum number of parallel jobs it will queue.
TBD: encapsulate LUMI-related processing logic into a separate script and feed it as an argument. This way we 
may easily apply the framework in other processing environments.

The second script downloads the files (e.g. cesnet_left.paths) from the specified datacenter (e.g. cesnet) to 
the specified local directory.  

### Run on LUMI, method3: for locally located input data, with batching that optimizes waiting time in the LUMI queue
Processing time on LUMI consists of time in the queue and processing time. Processing several html.zst files in each task
significantly reduces the waiting and the total time. Processing one batch should not take longer than the maximum 
task duration, e.g. 2 days for standard LUMI nodes. Since html.zst file sizes significantly vary, batch size is 
defined as their total size instead of the number of files assuming processing time primarily depends on the input data 
size.

```commandline
source src/warc2text_runner/two/stage2preplumic.sh
source venv/bin/activate
```
To run on 30 LUMI nodes in parallel, combining html.zst files from interrupted.paths into batches of roughly 1500 GB: 
```commandline
stage2nodeparallel_batched.sh 30 interruped.paths 1500
```

## Sanity checks for the outputs of Stage2
### Line counts
src/warc2text_runner/two/qualitycontrol/check_linecnt.sh checks that the number of lines (i.e. documents) in the input
metadata.zst and the output text.zst and lang.zst files matches. To reduce processing time it does not check html.zst 
files assuming Stage1 was done correctly. It also does not check that the lines are aligned between files, i.e. i-th line
in all files represent the same document, this should be guaranteed by the --keep-order flag of GNU parallel in the
data processing scripts.