import fire
import trafilatura
from trafilatura.settings import use_config
import logging
import lxml.etree as etree
# from resiliparse.extract.html2text import extract_plain_text


def process_html(fpath, include_comments=True, include_tables=False, no_fallback=False,
                 favour_precision=True, favour_recall=False, min_extracted_size=250, flog=None):
    logger = logging.getLogger(__name__)
    if flog is not None:
        logging.basicConfig(filename=flog, encoding='utf-8', level=logging.DEBUG)

    trafilatura_args = {
        "include_comments": include_comments,
        "include_tables": include_tables,
        "no_fallback": no_fallback,
        "favor_precision": favour_precision,
        "favor_recall": favour_recall,
        "with_metadata": False,
        # "target_language": "bg"
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
        # text = trafilatura.extract(html, output_format='xml', tei_validation=False, **trafilatura_args)
        # text = trafilatura.extract(html, output_format='markdown', **trafilatura_args)
        # text = trafilatura.extract(html, output_format='txt', **trafilatura_args)
        print(text)

        # text = extract_plain_text(html, main_content=True)
        # print(text)


fire.Fire(process_html)