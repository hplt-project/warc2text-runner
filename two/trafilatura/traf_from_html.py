import fire
import trafilatura
from trafilatura.settings import use_config
import logging


def process_html(fpath, include_comments=False, include_tables=False, no_fallback=False,
                 favour_precision=False, min_extracted_size=None, flog=None):
    logger = logging.getLogger(__name__)
    if flog is not None:
        logging.basicConfig(filename=flog, encoding='utf-8', level=logging.DEBUG)

    trafilatura_args = {
        "include_comments": include_comments,
        "include_tables": include_tables,
        "no_fallback": no_fallback,
        "favor_precision": favour_precision
    }

    config = use_config()
    if min_extracted_size is not None:
        config.set("DEFAULT", "MIN_EXTRACTED_SIZE", str(min_extracted_size))

    logger.info(f'Processing {fpath} with Trafilature version {trafilatura.__version__}')
    logger.info(trafilatura_args)
    logger.info(', '.join([f'{n}:{k}={v}' for n,d in config.items() for k, v in d.items()]))

    with open(fpath) as inp:
        html = inp.read()
        text = trafilatura.extract(html, config=config, **trafilatura_args)
#        text = trafilatura.extract(html, output_format='xml', tei_validation=True, **trafilatura_options)
        print(text)


fire.Fire(process_html)