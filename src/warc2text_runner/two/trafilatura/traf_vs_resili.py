import argparse
import io
import os
import sys
import time

import zstandard
import ujson as json
import trafilatura
from trafilatura.settings import use_config
from trafilatura.utils import load_html
from resiliparse.extract.html2text import extract_plain_text
import pyhtml2md

FORMATS = {
    'markdown': 'md',
    'xml': 'xml',
    'txt': 'txt',
    'html': 'md',
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--extractor', default='traf',
                        choices=('traf', 'resili'))
    parser.add_argument('--fpath', default='~/html.zst')
    parser.add_argument(
        '--output_format',
        default='markdown',
                        choices=('markdown', 'xml', 'txt', 'html'),
                        )
    parser.add_argument('--include_tables', action='store_true')
    parser.add_argument('--output_dir', default='../../../two/sample100/')
    return parser.parse_args()


def extract(args):
    fpath = os.path.expanduser(args.fpath)
    if args.extractor == "traf":
        trafilatura_options = {
            "include_comments": False,
            "include_tables": args.include_tables,
            "no_fallback": False,
            "output_format": args.output_format,
            "with_metadata": False,
            "include_formatting": True,
        }
        config = use_config()
        min_extracted_size = 0
        config.set("DEFAULT", "MIN_EXTRACTED_SIZE", str(min_extracted_size))
    outdir = f'{args.output_dir}/{args.extractor}-{args.output_format}-tables-{args.include_tables}'
    os.makedirs(outdir, exist_ok=True)
    times_doc = []
    with sys.stdin.buffer if fpath == '-' else io.BufferedReader(
            zstandard.open(fpath, 'rb')) as instream:
        counter = 0
        t0 = time.time()

        for byteline in instream:

            errors = []

            try:
                line = byteline.decode('utf-8', errors='strict')
            except UnicodeDecodeError as e:
                errors.append('UnicodeDecodeError')
                line = None

            if line is not None:
                t_doc = time.time()
                doc = json.loads(line.strip())
                doc_html = doc['h']
                tree = load_html(doc_html)
                if tree is None:
                    # raise ValueError("Could not parse HTML")
                    continue
                if args.extractor == "traf":
                    # text = trafilatura.extract(tree, config=config, **trafilatura_options)
                    # print(text)
                    # tree = load_html(doc_html)
                    text = trafilatura.extract(
                        tree,
                        config=config,
                        **trafilatura_options,
                    )
                    if (args.output_format == 'html') and isinstance(text, str):
                        try:
                            text = pyhtml2md.convert(text)
                        except UnicodeDecodeError:
                            trafilatura_options['output_format'] = 'markdown'
                            text = trafilatura.extract(
                                tree,
                                config=config,
                                **trafilatura_options,
                            )
                elif args.extractor == "resili":  # does not extract tables?
                    preserve_formatting = True
                    if args.output_format == 'markdown':
                        preserve_formatting = "minimal_html"
                    text = extract_plain_text(
                        doc_html,
                        preserve_formatting=preserve_formatting,
                        # main_content=True,
                    )
                    if args.output_format == 'markdown':
                        text = pyhtml2md.convert(text)
                times_doc.append(time.time() - t_doc)
                counter += 1
                with open(os.path.join(outdir,
                                       f"{counter}-{args.extractor}{os.extsep}{FORMATS[args.output_format]}"), 'w',
                          encoding='utf8') as f:
                    if not isinstance(text, str):
                        text = ''
                    f.write(text)

                if counter == 1000:
                    break
                if counter % 100 == 0:
                    print(f"{counter} docs processed")
        print(f"Total time: {time.time() - t0}")
    print(f"Average doc time {sum(times_doc) / len(times_doc)}")

    # traf w/o parallel Total time: 76.71070313453674
    # Average doc time 0.07639440846443177

    # resili w/o parallel Total time: 6.220118522644043
    # Average doc time 0.005949894905090332

    # resili w/o parallel main_content True: Total time: 5.647077798843384
    # Average doc time 0.005403486728668213

    ## resili w/o parallel  and markdown conversion Total time: 3.437060594558716
    # Average doc time 0.0031591196060180666


if __name__ == '__main__':
    args = parse_args()
    print(
        args.extractor
    )
    extract(args)
