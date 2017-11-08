#!/usr/bin/env bash

res=0
cut -f3 -d":" /etc/passwd | sort -n | uniq -c | while read x ; do
        [ -z "${x}" ] && break
        set - ${x}
        if [ $1 -gt 1 ]; then
            uid=`gawk -F: '($3 == n) { print $1 }' n=$2 /etc/passwd |xargs`
            echo "Duplicate GID ($2): ${uid}"
            exit 1
        fi
done
