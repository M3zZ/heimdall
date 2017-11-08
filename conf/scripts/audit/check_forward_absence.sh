#!/usr/bin/env bash

res=0
for dir in `awk -F: '{ print $6 }' /etc/passwd`; do
	if [ ! -h "$dir/.forward" -a -f "$dir/.forward" ]; then
		echo ".forward file $dir/.netrc exists"
		res=1
	fi
done
if [ ${res} -ne 0 ];then
	exit 1
fi