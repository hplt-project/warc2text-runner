cat *log|grep -E "file|du|trafbs|lidbs|real"|tr '\n' '\t'|sed 's/file/\nfile/g' >sequential_traf_lid_100proc.tsv
sed -i -r 's/file |du |trafbs |lidbs |real\t//g'  sequential_traf_lid_100proc.tsv
