#!/usr/bin/env bash

EXIT_CODE=0

if [ -f /etc/at.deny ];then
    rm -fr /etc/at.deny
else
    ${EXIT_CODE}=1

fi

if [ ! -f /etc/at.allow ];then
    touch /etc/at.allow
    if [ $(echo $?) -eq 0 ];then
        chown root:root /etc/at.allow
        chmod og-rwx /etc/at.allow
    else
        ${EXIT_CODE}=1
        break
    fi
else
    ${EXIT_CODE}=1
fi
exit ${EXIT_CODE}
