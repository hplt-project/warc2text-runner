# Second HPLT data release

## Phase2
Phase2 does text extraction with boilerplate removal (Trafilatura) and language identification (fasterText with the openLID model).
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

### Install on LUMI with EasyBuild (WORK IN PROGRESS)
export EBU_USER_PREFIX=/project/project_465000498/software/eb
TBD

### Install on other systems (not tested - TBD)
You might want to install on your local machine or a cluster other than LUMI.
Install using pip all the requirements, including those coming from cray-python module on LUMI, then download the required models: 
```commandline
python -m venv venv
source venv/bin/activate
pip install -r  two/requirements_LUMIall.txt
pip install .
```
TBD

### Download the required model weights
```commandline
stage2download.sh
```

### Run on LUMI (TBD)
```commandline
source src/warc2text_runner/two/stage2preplumic.sh
source venv/bin/activate
```

```commandline
find <PATH TO STAGE1 OTPUTS> -name "html.zst" >portion1.paths
stage2nodeparallel.sh portion1.paths
```

