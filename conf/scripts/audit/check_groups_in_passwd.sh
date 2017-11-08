#!/usr/bin/env bash

res=0
for i in $(cut -s -d: -f4 /etc/passwd | sort -u );do
	grep -q -P "^.*?:x:$i:" /etc/group
	if [ $? -ne 0 ]; then
		echo "Group $i is referenced by /etc/passwd but does not exist in /etc/group"
		res=1
	fi
done
if [ ${res} -ne 0 ];then
	exit 1
fi
