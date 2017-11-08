#!/usr/bin/env bash

res=0
for dir in `/bin/egrep -v '(root|halt|sync|shutdown)' /etc/passwd |/bin/awk -F: '($7 !~ "nologin$" || $7 !~ "false$") { print $6 }'`; do
	for file in ${dir}/.rhosts; do
		if [ ! -h "$file" -a -f "$file" ]; then
			echo ".rhosts file in $dir"
			res=1
		fi
	done
done
if [ ${res} -ne 0 ];then
	exit 1
fi
