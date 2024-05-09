# Language identification script for HPLT

## Overview

* `langid_scripts/proto_langid.py` - the script for language identification (fasttext).
* `langid_scripts/patterns.py` - the modeule with regular expressions for preprocessing the text.
* `langid_scripts/basic_log.py` - the module with basic logging functions.
* `tests/*` - the tests for the script.

## Basic usage

```bash
python -m langid_scripts.proto_langid --model_path $MODEL_PATH < $YOUR_FILE

# See the help message for more options:
python -m langid_scripts.proto_langid --help
```

## Installation

1) Create a virtual environment.

2) Run the following commands to install the [fastText](https://github.com/facebookresearch/fastText?tab=readme-ov-file#building-fasttext-for-python) library.

```bash
git clone https://github.com/facebookresearch/fastText.git
cd fastText
pip install .
```

3) Download the model.
```bash
wget https://data.statmt.org/lid/lid193_merged_arabics.bin
```

4) Install the required packages.

```bash
pip install regex==2024.4.28
pip install ujson==5.9.0
```

4) Install optional packages.

```bash
pip install pytest
```
