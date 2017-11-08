#!/usr/bin/env bash

res=0
if [ -f /etc/at.allow ];then
    fileperm=`/bin/ls -ld ${file} | cut -f1 -d" "`
	
	if [ `echo ${fileperm} | cut -c2 ` != "r" ];then
	    echo "User Read NOT set on $file"
	    res=1
	fi
	if [ `echo ${fileperm} | cut -c3 ` != "w" ];then
	    echo "User Write NOT set on $file"
	    res=1
	fi
	if [ `echo ${fileperm} | cut -c4 ` == "x" ];then
	    echo "User Execute set on $file"
	    res=1
	fi
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
else
    if [ -z /etc/at.deny ];then
        echo "/etc/at.allow do not exist AND /etc/at.deny do not exist !"
        res=1
    fi
fi

if [ ${res} -ne 0 ];then
	exit 1
fi




