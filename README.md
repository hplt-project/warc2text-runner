# Language identification for HPLT



## Obstacles

1) What is the best way to install and use fastText?

    a. Via [building for python](https://github.com/facebookresearch/fastText?tab=readme-ov-file#building-fasttext-for-python) or via [building for CMake](https://github.com/facebookresearch/fastText?tab=readme-ov-file#building-fasttext-using-cmake)

    b. Kenneth merged [the pull request for faster inference](https://github.com/facebookresearch/fastText/pull/1341). For what models/hardware configs is this faster? Need tests.

    c. Kenneth tested on `nllblid218e` and  `lid.176.bin` models.

2) What model/cleaning to use?

    a. Laurie has `lid201-model.bin` model (from this [repo](https://github.com/laurieburchell/open-lid-dataset))

    b. `lid201-model.bin` trained on super-clean data. See this scripts [here](https://github.com/laurieburchell/open-lid-dataset/tree/main/data_cleaning).

    c. Laurie will release a new model soon and it also uses clean data.
    https://github.com/laurieburchell/cs-lid-harder-than-you-think








