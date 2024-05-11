cat *log|grep -E "file|du|trafbs|real"|tr '\n' '\t'|sed 's/file/\nfile/g' >blocksize.tsv
sed -i -r 's/file |du |trafbs |real\t//g'  blocksize.tsv
