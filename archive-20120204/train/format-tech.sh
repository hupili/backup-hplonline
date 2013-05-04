#!/bin/bash

output="tech.formatted"
#rm -rf $output
mkdir -p $output

for i in `cat tech.list`
do
	md_name=`python get_md_name.py $i`
	if [[ ! -e "$output/$md_name" ]] ; then
		echo $i
		python make_preamble.py $i > "$output/$md_name"
		python extract_body.py tech.orig/$i >> "$output/$md_name"
	else
		echo $i already exists
	fi
	#break
done
