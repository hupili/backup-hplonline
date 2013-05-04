#!/bin/bash

rm -rf tech.formatted
mkdir -p tech.formatted

for i in `cat tech.list`
do
	md_name=`python get_md_name.py $i`
	python make_preamble.py $i > tech.formatted/$md_name
	python extract_body.py tech.orig/$i >> tech.formatted/$md_name
	break
done
