for version in 2.0.0; do
pip install trafilatura==$version
for x in */*.html ; do
  python ../../src/warc2text_runner/two/trafilatura/traf_from_html.py  $x --flog traf_args_search.log --include_tables --favour_precision >$(dirname $x)/$(basename $x .html).search_fineweblike_traf${version}.txt
  python ../../src/warc2text_runner/two/trafilatura/traf_from_html.py  $x --flog traf_args_search.log --favour_precision >$(dirname $x)/$(basename $x .html).search_fineweblike_notables_traf${version}.txt
  python ../../src/warc2text_runner/two/trafilatura/traf_from_html.py  $x --flog traf_args_search.log --favour_precision --min_extracted_size=0 >$(dirname $x)/$(basename $x .html).search_fineweblike_ms0_notables_traf${version}.txt
  python ../../src/warc2text_runner/two/trafilatura/traf_from_html.py  $x --flog traf_args_search.log --min_extracted_size=0 >$(dirname $x)/$(basename $x .html).search_fineweblike_ms0_notables_dontfavourprecision_traf${version}.txt
  python ../../src/warc2text_runner/two/trafilatura/traf_from_html.py $x --flog traf_args_search.log --no_fallback --min_extracted_size=0 >$(dirname $x)/$(basename $x .html).search_fineweblike_ms0_notables_nofallback_traf${version}.txt
done
done