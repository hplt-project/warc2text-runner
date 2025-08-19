import fire
from warcio.archiveiterator import ArchiveIterator
import ujson as json
import sys

def print_records():
    text_types = {"text/plain", "text/html", "application/xml", "text/vnd.wap.wml", "application/atom+xml", "application/opensearchdescription+xml", "application/rss+xml", "application/xhtml+xml"}
    for record in ArchiveIterator(sys.stdin.buffer, arc2warc=True):
        if record.rec_type == 'response':
            content = record.content_stream().read()
            content = content.decode('utf-8', errors='replace')
            res = {
                'u': record.rec_headers.get_header('WARC-Target-URI'),
                'h': content,
                'content_type': record.http_headers.get_header('Content-Type')  if record.http_headers else None,
                'transfer_encoding': record.http_headers['Transfer-Encoding'] if record.http_headers else None,
                'content_length': record.http_headers['Content-Length'] if record.http_headers else None,
                'content_encoding': record.http_headers['Content-Encoding'] if record.http_headers else None,
                'status': record.http_headers.get_statuscode() if record.http_headers else None
            }
            res['text_content_type'] = any(res['content_type'].lower().startswith(t) for t in text_types) if res['content_type'] else None
            print(json.dumps(res))


fire.Fire(print_records)
