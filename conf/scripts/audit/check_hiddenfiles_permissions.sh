#!/usr/bin/env bash

res=0
for dir in `egrep -v '(root|halt|sync|shutdown)' /etc/passwd| awk -F: '($7 !~ "nologin$" || $7 !~ "false$" ){print $6}'`;do
	for file in ${dir}/.[A-Za-z0-9]*; do
		if [ ! -h "$file" -a -f "$file" ]; then
			fileperm=`/bin/ls -ld ${file} | cut -f1 -d" "`
			if [ `echo ${fileperm} |cut -c6` != "-" ];then
				echo "Group Write permission set on file $file"
				res=1
			fi
			if [ `echo ${fileperm} | cut -c9` != "-" ];then
				echo "Other Write permission set on file $file"
				res=1
			fi
		fi
	done
done
if [ ${res} -ne 0 ];then
	exit 1
fi
