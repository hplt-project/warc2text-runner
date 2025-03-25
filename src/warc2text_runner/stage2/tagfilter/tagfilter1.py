import re
from collections import defaultdict
from pathlib import Path
from importlib.resources import files


def load_tagfilters(tagfilters_fname="mt-filter-list.annotated"):
    # For Python<3.10 replace importlib.resources with importlib_resources,
    # see https://setuptools.pypa.io/en/latest/userguide/datafiles.html for details
    filters_text = files('warc2text_runner.stage2.tagfilter').joinpath(tagfilters_fname).read_text()

    tagfilters = defaultdict(list)
    for l in filters_text.split('\n'):
        l = l.strip()
        if l == '' or l.startswith('#'):
            continue
        ff = l.split('\t')
        tagfilters[tuple(ff[:2])].append(ff[-1])
    return tagfilters


class TagFilter1:
    """
    Iterates over all nodes with the specified tag having the specified attribute with lxml Element.iterfind(),
    checks the value using pre-compiled regexps with Python re
    """
    def  __init__(self):
        tagfilters = load_tagfilters()
        ignorecase = True  # ignore case for better matching, though in the original C++ implementation it was not ignored
        self.tagattr2re = {k: re.compile('|'.join(f'({t})' for t in v), flags=re.IGNORECASE if ignorecase else 0)
                           for k, v in tagfilters.items()}
        # print(self.tagattr2re)

    def matches(self, tree):
        for (tag, attr), regex in self.tagattr2re.items():
            for e in tree.iterfind(f".//{tag}[@{attr}]"):
                val = e.get(attr)
                # print(tag, attr, val)
                for m in regex.finditer(val):
                    return tag, attr, val
        return None
