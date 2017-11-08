#!/usr/bin/env bash
cut -f1 -d":" /etc/group | sort -n | uniq -c | while read x ; do
    [ -z "${x}" ] && break
    set - ${x}
    if [ $1 -gt 1 ]; then
        groups=`gawk -F: '($1 == n) { print $3 }' n=$2 /etc/group | xargs`
        echo "Duplicate Group Name ($2): ${groups}"
        exit 1
    fi
done