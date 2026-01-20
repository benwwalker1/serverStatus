#!/bin/sh


echo "| server | status |" > README.md
echo "| ------ | ------ |" >> README.md

if ping -c 1 -w 1 nsc1.utdallas.edu | grep -q "1 received"; then
	echo -n "online, " >> checkServers.csv
	echo "| nsc1 | :+1: |" >> README.md
else
	echo -n "offline, " >> checkServers.csv
	echo "| nsc1 | :stop_sign: |" >> README.md
fi
if ping -c 1 -w 1 nsc2.utdallas.edu | grep -q "1 received"; then
	echo -n "online, " >> checkServers.csv
	echo "| nsc2 | :+1: |" >> README.md
else
	echo -n "offline, " >> checkServers.csv
	echo "| nsc2 | :stop_sign: |" >> README.md
fi
if ping -c 1 -w 1 nsc3.utdallas.edu | grep -q "1 received"; then
	echo -n "online, " >> checkServers.csv
	echo "| nsc2 | :+1: |" >> README.md
else
	echo -n "offline, " >> checkServers.csv
	echo "| nsc3 | :stop_sign: |" >> README.md
fi
if ping -c 1 -w 1 nsc4.utdallas.edu | grep -q "1 received"; then
	echo "online" >> checkServers.csv
	echo "| nsc4 | :+1: |" >> README.md
else
	echo "offline" >> checkServers.csv
	echo "| nsc4 | :stop_sign: |" >> README.md
fi

git add README.md
git commit -m "update status"
git push
