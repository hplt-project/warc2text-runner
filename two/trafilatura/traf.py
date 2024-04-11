import io
import os
import sys
import ujson as json
import trafilatura
import fire
import zstandard
import codecs
import traceback
from trafilatura.settings import use_config
from timeit import default_timer as timer


def traf(instream, fast_mode, decoding_errors, min_extracted_size=0):
    trafilatura_options = {"include_comments": False, "include_tables": False, "no_fallback": fast_mode}
    config = use_config()
    config.set("DEFAULT", "MIN_EXTRACTED_SIZE", str(min_extracted_size))

    for byteline in instream:
        st = timer()
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
                text = trafilatura.extract(html, config=config, **trafilatura_options)
            except Exception as e:
                errors.append(traceback.format_exc())
                text = None

        dur = timer() - st
        print(json.dumps({'t': text, 'e': errors, 'dur': f'{dur:.1e}'}))


def main(fpath: str = '-', fast_mode: bool = False, decoding_errors: str = 'ignore', min_extracted_size: int = 0):
    """
    Extracts texts from HTMLs using Trafilatura library.
    Reads jsonlines with "h" field containing HTMLs from stdin or file. Writes jsonlines to stdout containing text
    extracted, any errors occurred while decoding from utf-8 or text extraction, document processing time.
    In case of errors returns None in the 't' field instead of extracted text.

    :param fpath: path to the input .zst or '-' to read from stdin
    :param fast_mode:
    :param decoding_errors: how to handle utf-8 decoding errors, see https://docs.python.org/3/library/functions.html#open for options;
    the script will always try to decode in 'strict' mode to detect and report any errors, if decoding_errors!='strict'
    then in case of errors will retry using the specified mode.
    :param min_extracted_size: when Trafilatura cannot extract text of at least this length from HTML, it falls back
    to a simple baseline extraction algorithm (that almost doesn't remove boilerplate and performs poorly according
    to the evaluation in the whitepaper). Recommended to keep the default value of 0 to keep boilerplate removed for
    short pages.
    """

    with sys.stdin.buffer if fpath == '-' else io.BufferedReader(zstandard.open(fpath, 'rb')) as inp:
        traf(inp, fast_mode, decoding_errors, min_extracted_size)


fire.Fire(main)
