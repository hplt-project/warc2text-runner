import fire
import trafilatura
from trafilatura.settings import use_config

def process_html(fpath, include_comments=False, include_tables=False, no_fallback=False,
                 favour_precision=False, min_extracted_size=None):
    config = use_config()
    if min_extracted_size is not None:
        config.set("DEFAULT", "MIN_EXTRACTED_SIZE", str(min_extracted_size))

    with open(fpath) as inp:
        html = inp.read()
        text = trafilatura.extract(html, include_comments=include_comments, include_tables=include_tables,
                                   no_fallback=no_fallback, config=config,
                                   favor_precision=favour_precision)
#        text = trafilatura.extract(html, output_format='xml', tei_validation=True, **trafilatura_options)
        print(text)


fire.Fire(process_html)