import argparse
import io
import trafilatura
from trafilatura.settings import use_config
from trafilatura.utils import load_html
import timeit
import logging
import zstandard
import json
import functools


def setup_traf(args):
    trafilatura_options = {
        "include_comments": args.include_comments,
        "include_tables": args.include_tables,
        "no_fallback": False,
        "output_format": args.output_format,
        "with_metadata": False,
        "include_formatting": True,
    }
    config = use_config()
    min_extracted_size = 0
    config.set("DEFAULT", "MIN_EXTRACTED_SIZE", str(min_extracted_size))
    return trafilatura_options, config

def extarct(doc_html):
    tree = load_html(doc_html)
    if tree is None:
        return ''
    text = trafilatura.extract(
        tree,
        config=config,
        **trafilatura_options,
    )
    return text


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', default='2.0.0')
    parser.add_argument('--include_tables', action='store_true')
    parser.add_argument('--include_comments', action='store_true')
    parser.add_argument('--output_format', default='xml')
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, filename="speed.log")
    logging.info(args)
    trafilatura_options, config = setup_traf(args)

    times = []
    with io.BufferedReader(
            zstandard.open('../../../../two/sample100/CC.zst', 'rb')) as instream:
        counter = 0

        for byteline in instream:
            errors = []
            try:
                line = byteline.decode('utf-8', errors='strict')
            except UnicodeDecodeError as e:
                errors.append('UnicodeDecodeError')
                line = None

            if line is not None:
                doc = json.loads(line.strip())
                doc_html = doc['h']
                time = timeit.timeit(functools.partial(extarct, doc_html), number=3)
                times.append(time)
    logging.info(sum(times)/len(times))
