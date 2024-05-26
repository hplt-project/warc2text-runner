import io
import os
import sys
import ujson as json
import trafilatura
import fire
import zstandard
import traceback
from trafilatura.settings import use_config
from trafilatura.utils import load_html
from timeit import default_timer as timer
import signal
from contextlib import contextmanager, nullcontext
from warc2text_runner.two.tagfilter.tagfilter1 import TagFilter1 as TagFilter

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutError("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


def traf(instream, fast_mode, decoding_errors, min_extracted_size=0, timelimit_perdoc=None, matcher=None):
    trafilatura_options = {"include_comments": False, "include_tables": False, "no_fallback": fast_mode}
    config = use_config()
    config.set("DEFAULT", "MIN_EXTRACTED_SIZE", str(min_extracted_size))

    for byteline in instream:
        # st = timer()
        errors = []
        tagmatch = None

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
                with time_limit(timelimit_perdoc) if timelimit_perdoc else nullcontext():
                    tree = load_html(html)
                    if tree is None:
                        raise ValueError("Could not parse HTML")
                    tagmatch = matcher.matches(tree)
                    # trafilatura.extract() changes the tree, tagfilters should be matched before
                    text = trafilatura.extract(tree, config=config, **trafilatura_options)
            except TimeoutError as e:
                errors.append(f'Trafilatura timed out: {timelimit_perdoc}s')
                text = None
            except Exception as e:
                errors.append(traceback.format_exc())
                text = None

        # dur = timer() - st
        res = {'t': text}
        # res = {'t': text, 'dur': f'{dur:.1e}'}

        if errors:
            res['traferr'] = errors
        if tagmatch is not None:
            res['tagfilter'] = tagmatch
        print(json.dumps(res))


def main(fpath: str = '-', fast_mode: bool = False, decoding_errors: str = 'ignore', min_extracted_size: int = 0,
         timelimit_perdoc: float = None):
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
    :param timelimit_perdoc: sets maximum time (in seconds) for processing 1 document with Trafilatura
    """
    matcher = TagFilter()
    with sys.stdin.buffer if fpath == '-' else io.BufferedReader(zstandard.open(fpath, 'rb')) as inp:
        traf(inp, fast_mode, decoding_errors, min_extracted_size, timelimit_perdoc, matcher)


if __name__ == '__main__':
    fire.Fire(main)
