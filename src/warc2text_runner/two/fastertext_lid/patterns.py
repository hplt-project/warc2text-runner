"""
The patterns module contains the regex patterns used in the langid scripts.

Based on: https://github.com/hplt-project/warc2text-runner/blob/c973e6f27fbb7abce3ac9da29143175e4b703a13/two/fastertext_lid/patterns.py
"""

import regex

# defines what we want to remove from string for langID
NONWORD_REPLACE_STR = r"[^\p{Word}\p{Zs}]|\d"  # either (not a word nor a space) or (is digit)
NONWORD_REPLACE_PATTERN = regex.compile(NONWORD_REPLACE_STR)
SPACE_PATTERN = regex.compile(r"\s\s+")  # squeezes sequential whitespace
