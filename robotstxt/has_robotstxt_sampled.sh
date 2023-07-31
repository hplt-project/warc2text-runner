find ./wide00017_urls/ -name "*.gz" |parallel --eta -n 10 "zcat {}|sed -n 0~100000p" >sample
sort -R sample|head -100|cut -f -3 -d '/' |sed 's!$!/robots.txt!'|parallel "grep -F -l {} wide00017_robotstxt|wc"
