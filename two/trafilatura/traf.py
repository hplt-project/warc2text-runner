import io
import os
import sys
import orjson as json
import trafilatura
import fire
import zstandard
import codecs
import traceback

def traf(instream, fast_mode, decoding_errors):
    trafilatura_options = {"include_comments": False, "include_tables": False, "no_fallback": True} if fast_mode \
        else {}

    for byteline in instream:
        errors = []

        try:
            line = byteline.decode('utf-8', errors='strict')
        except UnicodeDecodeError as e:
            errors.append('UnicodeDecodeError')
            line = None if decoding_errors == 'strict' else byteline.decode('utf-8', errors=decoding_errors)

        if line is None:
            text = None
        else:
            try:
                d = json.loads(line.strip())
                html = d['h']
                text = trafilatura.extract(html, **trafilatura_options)
            except Exception as e:
                errors.append(traceback.format_exc())
                text = None

        print(json.dumps({'t': text, 'e': errors}))


def main(fpath='-', fast_mode=True, decoding_errors='ignore'):
    """

    :param fpath:
    :param fast_mode:
    :param decoding_errors: how to handle utf-8 decoding errors, see https://docs.python.org/3/library/functions.html#open for options
    :return:
    """
    with sys.stdin.buffer if fpath == '-' else io.BufferedReader(zstandard.open(fpath, 'rb')) as inp:
        traf(inp, fast_mode, decoding_errors)


fire.Fire(main)
