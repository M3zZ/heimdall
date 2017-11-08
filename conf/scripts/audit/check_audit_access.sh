#!/bin/bash

BIN=`find / -xdev \( -perm -4000 -o -perm -2000 \) -type f`

if [ ! -a /etc/audit/audit.rules ];then
	echo "Can't check /etc/audit/audit.rule, file doesn't exist!" 
	exit 1
fi
for bin in ${BIN};do
	grep -- "-a always,exit -F path='$bin' -F perm=x -F auid>=1000 -F auid!=4294967295 -k privileged" /etc/audit/audit.rules
	if [ $? ne 0 ];then
		echo "$bin not in not in audit.rules"
		res=1
	fi
done
if [ ${res} -ne 0 ];then
	exit 1
fi
