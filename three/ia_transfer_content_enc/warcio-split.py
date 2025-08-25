import fire
from warcio.archiveiterator import ArchiveIterator
from warcio.warcwriter import WARCWriter
import ujson as json
import sys
from collections import defaultdict
from pathlib import Path

def get_writer(outdir, writers, k):
    if k not in writers:
        writers[k] = WARCWriter(open(Path(outdir) / (k+'.warc.gz'), 'wb'), gzip=True)
    return writers[k]

def split_records(outdir):
    filter_types = {'video/','image/','audio/','binary/'}
    text_types = {"text/plain", "text/html", "application/xml", "text/vnd.wap.wml", "application/atom+xml", "application/opensearchdescription+xml", "application/rss+xml", "application/xhtml+xml"}
    writers = dict()
    for record in ArchiveIterator(sys.stdin.buffer, arc2warc=True):
        if record.rec_type != 'response' or record.http_headers is None: continue
        content_type = record.http_headers.get_header('Content-Type')
        if content_type is None: continue
        content_type = content_type.lower()
        if any(t in content_type for t in filter_types): continue
        res = {
            'content_type': record.http_headers.get_header('Content-Type')  if record.http_headers else None,
            'transfer_encoding': record.http_headers['Transfer-Encoding'] if record.http_headers else None,
            'content_encoding': record.http_headers['Content-Encoding'] if record.http_headers else None
        }
        is_text_type = any(t in content_type for t in text_types)
        try:
            get_writer(outdir, writers, f"{res['transfer_encoding']}-{res['content_encoding']}-{is_text_type}").write_record(record)
        except:
            print('ERROR: writing the record')

fire.Fire(split_records)
