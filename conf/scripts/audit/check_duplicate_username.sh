#!/usr/bin/env bash

res=0
cut -f1 -d":" /etc/passwd | sort -n | uniq -c | while read x ; do
    [ -z "${x}" ] && break
    set - ${x}
    if [ $1 -gt 1 ]; then
        users=`gawk -F: '($1 == n) { print $3 }' n=$2 /etc/passwd | xargs`
        echo "Duplicate User Name ($2): ${users}"
        exit 1
    fi
done