#!/usr/bin/env bash

ips=`ip link show|awk -F': ' '/wlan/ {print $2}'`
for ip in ${ips};do
	ip link set ${ip} down
	file_if="/etc/sysconfig/network-scripts/ifcfg-$ip"
	if -f ${file_if};then
	    rm -f /etc/sysconfig/network-scripts/ifcfg-${ip}
	else
	    echo "$file_if doesnt exist, exiting"
	    exit 2
	fi
done
