#!/usr/bin/env bash
res=0
for dir in $(egrep -v '(root|halt|sync|shutdown)' /etc/passwd | awk -F: '($3 > 1000 && ( $7 !~ "nologin$" || $7 !~ "false$") ){ print $6}');do
	if [ -d ${dir} ];then
 	dirperm=`/bin/ls -ld ${dir} | cut -f1 -d" "`
		if [ `echo ${dirperm} | cut -c6 ` != "-" ]; then
			echo "Group Write permission set on directory $dir"
			res=1
		fi
		if [ `echo ${dirperm} | cut -c8 ` != "-" ]; then
			echo "Other Read permission set on directory $dir"
			res=1
		fi
		if [ `echo ${dirperm} | cut -c9 ` != "-" ]; then
			echo "Other Write permission set on directory $dir"
			res=1
		fi
		if [ `echo ${dirperm} | cut -c10 ` != "-" ]; then
			echo "Other Execute permission set on directory $dir"
			res=1
		fi
	fi
done
if [ ${res} -ne 0 ];then
	exit 1
fi
