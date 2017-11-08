#!/usr/bin/env bash
awk -F: '{ print $1" "$3" "$6 }' /etc/passwd |while read user uid dir; do
	if [ ${uid} -ge 1000 -a -d "$dir" -a ${user} != "nfsnobody" ]; then
		owner=$(stat -L -c "%U" "$dir")
		if [ "$owner" != "$user" ]; then
			echo "The home directory ($dir) of user $user is owned by $owner."
			exit 1
		fi
	fi
done
