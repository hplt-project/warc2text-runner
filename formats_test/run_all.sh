set -x
if [[ ! -f url.gz || ! -f text.gz || ! -f date.gz ]]; then
    echo "Copy input files to the current directory!"
    exit
fi

bash separatefiles2json.sh &> NIRD_separatefiles2json.log
bash compare_process_text.sh &> NIRD_compare_process_text.log
bash compare_process_urltext.sh &> NIRD_compare_process_urltext.log
bash compare_process_urldate.sh &> NIRD_compare_process_urldate.log
