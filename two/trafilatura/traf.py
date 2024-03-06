import os
import sys
import ujson as json
import trafilatura
import fire
import zstandard
import codecs
import traceback

def traf(instream, fast_mode):
    trafilatura_options = {"include_comments": False, "include_tables": False, "no_fallback": True} if fast_mode \
        else {}
    unicode_error = False
    cnt = 0
    while True:
        errmsg = None
        try:
            line = instream.readline()
            if unicode_error:
                unicode_error = False
                continue  # recovering after UnicodeDecodeError: reading the rest of line and skipping it
        except UnicodeDecodeError as e:
            errmsg = 'UnicodeDecodeError'
            unicode_error = True
            continue

        if line == '':
            break

        try:
            d = json.loads(line.strip())
            html = d['h']
            text = trafilatura.extract(html, **trafilatura_options)
            # print(text)
        except Exception as e:
#            import pdb; pdb.set_trace()
            errmsg = traceback.format_exc()
            text = None

        print(json.dumps({'t': text, 'e': errmsg}))
        cnt += 1


def main(fpath='-', fast_mode=True, decoding_errors='ignore'):
    """

    :param fpath:
    :param fast_mode:
    :param decoding_errors: how to handle utf-8 decoding errors, see https://docs.python.org/3/library/functions.html#open for options
    :return:
    """

    with (open(os.dup(sys.stdin.fileno()), 'rt', encoding='utf-8', errors=decoding_errors) if fpath == '-' else
        zstandard.open(fpath, 'rt', encoding='utf-8', errors=decoding_errors)) as text_inp:
        traf(text_inp, fast_mode)


fire.Fire(main)
