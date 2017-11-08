#!/usr/bin/env bash
awk -F: '{ print $1" "$3" "$6 }' /etc/passwd |while read user uid dir; do
	if [ ${uid} -ge 1000 -a ! -d "$dir" -a ${user} != "nfsnobody" ];then
		echo "The home directory ($dir) of user $user does not exist."
		exit 1
	fi
done
