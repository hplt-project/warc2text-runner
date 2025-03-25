FPATS="html.zst pdf.warc.gz metadata.zst robotstxt.warc.gz"
echo $FPATS total
for x in ${@}; do 
	for fpat in $FPATS; do 
		find $x -name "$fpat" -exec du -ch {} +|grep total|cut -f 1|tr '\n' ' '; done ;  du -sh $x;  
done
