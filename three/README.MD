# Third HPLT data release
Extraction of raw texts from WARC archives is performed in two stages. In the first stage WARC files
are processed and relevant records are selected. From these records web pages in HTML format and
additional metadata are extracted and dumped to disk. This stage requires voluminous storage and
fast access to WARC files stored in two data centers, but it is not computationally intensive, thus, this
stage is executed on the compute nodes in the data centers directly attached to the storage with WARC
files.
The second stage consists of parsing HTML pages, removing boilerplate and extracting text in natural
language and additional metadata, and finally running language identification on the extracted text. 
This stage is significantly more computationally intensive, thus, it is run on the LUMI cluster.

## Stage1 (a.k.a. warc2html)
### Install dependencies
* Install warc2text 1.3.0 from https://github.com/bitextor/warc2text. To reproduce what was done for the third HPLT data 
release, follow the installation method using EasyBuild. 
* Clone this repo. Install as a python module:
```bash
pip install .
```

### Configure
The following instructions rely on the file structure and configuration of NIRD and CESNET, in particular:
1. a symlink ~/hplt in your home directory points to the project directory; e.g. for NIRD:
```commandline
ln -s /nird/datalake/NS8112K/ ~/hplt
```
2. passwordless access to the computing nodes:
```commandline
eval `ssh-agent`
ssh-add
```

### Run
1. Create the input directory and put a list of crawls to process there. E.g., the following script is NIRD-specific, 
it creates a directory nirdl_three_cc with a list of some CC crawls stored there, adapt it to your needs:
```commandline
./find_crawls.sh
```

2. Generate a list of processing tasks from the list of crawls, e.g. for the third-iteration CC crawls on NIRD:
```commandline
generate_tasks.sh nirdl_three_cc 1000 ~/hplt/three/html 
```
This will take find all WARC files, combine them into batches of 1000 WARCs and for each batch write a command that 
processes this batch with warc2text to nirdl_three_cc/tasks.args.gz. These commands specify ~/hplt/three/html as the
output directory for stage1.


3. Run HTML extraction with warc2text. E.g. for NIRD:
```commandline
run_warc2html_remote.sh nirdl_three_cc 250 "--sshlogin 1/nird-d,1/nird-c"
```
takes tasks from nirdl_three_cc/tasks.args.gz and runs warc2text on two nodes (nird-d and nird-c), in 250 parallel processes on each node.
To run locally specify the empty string as the 3rd argument:
```commandline
run_warc2html_remote.sh nirdl_three_cc 250 ""
```
NB! On NIRD ssh connection to other node occasionally dropped, thus, we preferred splitting crawls manually and running
on each node locally. On CESNET the first remote option works well. 

At the end it reports how many nodes finished all their tasks without unrecoverable errors. In case of any unrecoverable
errors, inspect joblogs for each compute node (dumped to nirdl_three_cc_logs/$HOSTNAME/joblog), find the failed commands 
and their batch ids, inspect stdout/stderr of warc2text for the corresponding batch ids (dumped to  ~/hplt/three/html/*_logs). 
For recoverable errors (e.g. one of the input WARC files is corruputed) warc2text only leaves error messages in 
~/hplt/three/html/*_logs and no errors are reported in joblogs, grep errors from the logs.


## Data transfer to LUMIO
1) Limit the number of parts per file for multipart uploads to 1K: --s3-max-upload-parts 1000 (The number of files per 
bucket on LUMIO is limited to 500K files, rclone uses multipart upload with max 10K parts per file by default.)
2) Increase upload chunk size: --s3-chunk-size 128M (splitting files into many small chunks results in too many IOPS, especially on CESNET)

```commandline
rclone copy -P --s3-max-upload-parts 1000 --transfers 16 --s3-upload-concurrency 16 --s3-chunk-size 128M --checkers 1 --log-level DEBUG --log-file lumio-upload.log html_three_cc_nird_part1 lumio:threecc/html_three_cc_nird_part1
```

NB! Make sure you have at least 32 GB of RAM (max memory consumption is --transfers * --s3-chunk-size * --s3-upload-concurrency). 
If less, use  --max-buffer-memory (see rclone docs).

## Stage2 (a.k.a. html2text)
Stage2 does text extraction with boilerplate removal (Trafilatura) and language identification (fasterText with the openLID model).
It is executed on 100 LUMI compute nodes, in 250 parallel processes on each.

### Install on LUMI
Clone this repository. Load the required LUMI modules:
```commandline
source src/warc2text_runner/stage2/stage2preplumic.sh
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

### Run on LUMI, method1: for data from LUMI-O object store
```commandline
source src/warc2text_runner/stage2/stage2preplumic.sh
source venv/bin/activate
```

Prepare a list of HTML files to process from LUMIO:
```commandline
rclone ls --include="html.zst" lumio:htmlsample | sed -r 's!( *[0-9]+\s+)!\1 lumio:htmlsample/!' >lumio.paths
```

NB! If you want to process local files, please create an rclone endpoint with the type 'alias' for the parent folder of
all of these files and provide a list of files in the format endpoint:path. The code supports only paths in this format.
It strips endpoint: and reconstructs path under the specified OUTPUT directory.

Specify the account and the partition SLURM should use:
```commandline
export SLURM_ACCOUNT=project_465002259
export SLURM_MEM_PER_NODE=0  # same as --mem=0, requests all memory since standard nodes are allocated fully
export SLURM_PARTITION=standard
export SLURM_TIMELIMIT=0-48:00:00
```


```commandline
export SLURM_ACCOUNT=project_465002259
export SLURM_MEM_PER_CPU=1750M  # same as --mem-per-cpu=1750M, recommended for the small partition in the LUMI docs to avoid extra billing for larger memory nodes
export SLURM_PARTITION=small
export SLURM_TIMELIMIT=0-72:00:00
```

Run processing in 100 parallel nodes max, 50 GB of input HTMLs per SLURM job:
```commandline
stage2nodeparallel_batched.sh 100 lumio.paths 50 ~/hplt/three/html_test
```


