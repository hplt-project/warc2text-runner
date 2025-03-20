# Extraction of language info from HTML is based on the code of Trafilatura's language filter:
# https://github.com/adbar/trafilatura/blob/3d7e786a58167eb1d0959f1d6872b48d908b77a9/trafilatura/utils.py#L390
from collections import defaultdict
import re

TARGET_LANG_ATTRS = ('http-equiv="content-language"', 'property="og:locale"')
RE_HTML_LANG = re.compile(r'([a-z]{2})')

def extract_lang_info(tree):
    res = defaultdict(list)
    for attr in TARGET_LANG_ATTRS:
        elems = tree.findall(f'.//meta[@{attr}][@content]')
        if elems:
            res['metalang'].extend(elem.get("content", "") for elem in elems)

    elems = tree.xpath("//html[@lang]")
    if elems:
        res['htmllang'].extend(elem.get("lang", "") for elem in elems)

    return res
