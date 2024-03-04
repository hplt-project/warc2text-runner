import os
import sys
import ujson as json
import trafilatura
import fire
import zstandard
import codecs

def traf(instream, fast_mode):
    trafilatura_options = {"include_comments": False, "include_tables": False, "no_fallback": True} if fast_mode \
        else {}

    while True:
        try:
            line = instream.readline()
            if line == '':
                break

            d = json.loads(line.strip())
            html = d['h']
            text = trafilatura.extract(html, **trafilatura_options)
            print(json.dumps({'t': text}))
            # print(text)

        except UnicodeDecodeError as e:
            print(e, file=sys.stderr)


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