#!/usr/bin/env bash
cut -f3 -d":" /etc/group | sort -n | uniq -c | while read x ; do
        [ -z "${x}" ] && break
        set - ${x}
        if [ $1 -gt 1 ]; then
            gid=`gawk -F: '($3 == n) { print $1 }' n=$2 /etc/group |xargs`
            echo "Duplicate GID ($2): ${gid}"
            exit 1
        fi
done
