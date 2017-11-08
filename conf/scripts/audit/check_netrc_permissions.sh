#!/usr/bin/env bash

res=0
for dir in `/bin/egrep -v '(root|sync|halt|shutdown)' /etc/passwd|awk -F: '($7 !~ "nologin$" || $7 !~ "false$") { print $6 }'`; do
	for file in ${dir}/.netrc; do
        if [ ! -h "$file" -a -f "$file" ]; then
            fileperm=`/bin/ls -ld ${file} | cut -f1 -d" "`
            if [ `echo ${fileperm} | cut -c5 ` != "-" ];then
                echo "Group Read set on $file"
                res=1
            fi
            if [ `echo ${fileperm} | cut -c6 ` != "-" ];then
                echo "Group Write set on $file"
                res=1
            fi
            if [ `echo ${fileperm} | cut -c7 ` != "-" ];then
                echo "Group Execute set on $file"
                res=1
            fi
            if [ `echo ${fileperm} | cut -c8 ` != "-" ];then
                echo "Other Read set on $file"
                res=1
            fi
            if [ `echo ${fileperm} | cut -c9 ` != "-" ];then
                echo "Other Write set on $file"
                res=1
            fi
            if [ `echo ${fileperm} | cut -c10 ` != "-" ];then
                echo "Other Execute set on $file"
                res=1
            fi
		fi
	done
done
if [ ${res} -ne 0 ];then
	exit 1
fi