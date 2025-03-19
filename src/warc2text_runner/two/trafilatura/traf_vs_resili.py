import argparse
import io
import logging
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
                        choices=('traf', 'resili', 'traf_1_8'))
    parser.add_argument('--fpath', default='~/html.zst')
    parser.add_argument(
        '--output_format',
        default='markdown',
        choices=('markdown', 'xml', 'txt', 'html'),
    )
    parser.add_argument('--include_tables', action='store_true')
    parser.add_argument('--output_dir', default='../../../two/sample100/')
    parser.add_argument('--no_fallback', action='store_true')
    parser.add_argument('--main_content', action='store_true')
    parser.add_argument('--include_comments', action='store_true')
    parser.add_argument('--include_formatting', action='store_true')
    parser.add_argument('--with_metadata', action='store_true')
    return parser.parse_args()


def setup_traf(args):
    trafilatura_options = {
        "include_comments": args.include_comments,
        "include_tables": args.include_tables,
        "no_fallback": args.no_fallback,
        "output_format": args.output_format,
        "with_metadata": args.with_metadata,
        "include_formatting": args.include_formatting,
    }
    config = use_config()
    min_extracted_size = 0
    config.set("DEFAULT", "MIN_EXTRACTED_SIZE", str(min_extracted_size))
    return trafilatura_options, config


def traf(doc_html, config, trafilatura_options):
    tree = load_html(doc_html)
    if tree is None:
        # raise ValueError("Could not parse HTML")
        return ''
    text = trafilatura.extract(
        tree,
        config=config,
        **trafilatura_options,
    )
    if (trafilatura_options['output_format'] == 'html') and isinstance(text,
                                                                       str):
        try:
            text = pyhtml2md.convert(text)
        except UnicodeDecodeError:
            trafilatura_options['output_format'] = 'markdown'
            text = trafilatura.extract(
                tree,
                config=config,
                **trafilatura_options,
            )
    return text


def resili(doc_html, args):
    preserve_formatting = True
    if args.output_format == 'markdown':
        preserve_formatting = "minimal_html"
    text = extract_plain_text(
        doc_html,
        preserve_formatting=preserve_formatting,
        main_content=args.main_content,
    )
    if args.output_format == 'markdown':
        text = pyhtml2md.convert(text)
    return text


def extract(args, method_name, outdir):
    fpath = os.path.expanduser(args.fpath)
    if "traf" in args.extractor:
        trafilatura_options, config = setup_traf(args)
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
                doc = json.loads(line.strip())
                doc_html = doc['h']
                counter += 1
                out_fn = f"{counter}-{method_name}{os.extsep}{FORMATS[args.output_format]}"
                if '<td>' in doc_html:
                    out_fn = f'IS_TABLE-{out_fn}'
                t_doc = time.time()
                if "traf" in args.extractor:
                    text = traf(doc_html, config, trafilatura_options)
                    if (text is not None) and ('<comments>' in text):
                        out_fn = f'IS_COMMENTS-{out_fn}'
                elif args.extractor == "resili":  # does not extract tables?
                    text = resili(doc_html, args)
                times_doc.append(time.time() - t_doc)

                with open(
                        os.path.join(outdir, out_fn),
                        'w',
                        encoding='utf8',
                ) as f:
                    if not isinstance(text, str):
                        text = ''
                    f.write(text)

                if counter == 1000:
                    break
                if counter % 100 == 0:
                    logging.info(f"{counter} docs processed")
        logging.info(f"Total time: {round(time.time() - t0, 3)}")
    logging.info(
        f"Average doc time {round(sum(times_doc) / len(times_doc), 3)}")

    # traf 1.8 w/o parallel Total time: 76.71070313453674, 1000 docs
    # Average doc time 0.07639440846443177

    # resili w/o parallel Total time: 6.220118522644043, 1000 docs
    # Average doc time 0.005949894905090332

    # resili w/o parallel main_content True: Total time: 5.647077798843384, 1000 docs
    # Average doc time 0.005403486728668213

    ## resili w/o parallel  and markdown conversion Total time: 3.437060594558716, 1000 docs
    # Average doc time 0.0031591196060180666


if __name__ == '__main__':
    args = parse_args()
    if 'traf' in args.extractor:
        method_name = '-'.join(
            (
                args.extractor,
                args.output_format,
                f"tables-{args.include_tables}",
                f"no_fallback-{args.no_fallback}",
                f"comments-{args.include_comments}",
                f"formatting-{args.include_formatting}",
                f"metadata-{args.with_metadata}",
            )
        )
    elif args.extractor == 'resili':
        method_name = f"{args.extractor}-{args.output_format}-main_content-{args.main_content}"
    outdir = f'{args.output_dir}/{args.extractor}/{method_name}'
    os.makedirs(outdir, exist_ok=True)
    logging.basicConfig(level=logging.INFO,
                        filename=os.path.join(outdir, f'{method_name}.log'))
    logging.info(
        args.extractor
    )
    extract(args, method_name, outdir)
