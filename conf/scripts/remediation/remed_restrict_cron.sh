#!/usr/bin/env bash

EXIT_CODE=0

if [ -f /etc/cron.deny ];then
    rm -fr /etc/cron.deny
else
    ${EXIT_CODE}=1

fi

if [ ! -f /etc/cron.allow ];then
    touch /etc/cron.allow
    if [ $(echo $?) -eq 0 ];then
        chown root:root /etc/cron.allow
        chmod og-rwx /etc/cron.allow
    else
        ${EXIT_CODE}=1
        break
    fi
else
    ${EXIT_CODE}=1
fi
exit ${EXIT_CODE}
