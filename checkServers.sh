#!/bin/sh

if ping -c 1 -w 1 nsc1.utdallas.edu | grep -q "1 received"; then
	echo -n "online, " >> checkServers.csv
else
	echo -n "offline, " >> checkServers.csv
fi
if ping -c 1 -w 1 nsc2.utdallas.edu | grep -q "1 received"; then
	echo -n "online, " >> checkServers.csv
else
	echo -n "offline, " >> checkServers.csv
fi
if ping -c 1 -w 1 nsc3.utdallas.edu | grep -q "1 received"; then
	echo -n "online, " >> checkServers.csv
else
	echo -n "offline, " >> checkServers.csv
fi
if ping -c 1 -w 1 nsc4.utdallas.edu | grep -q "1 received"; then
	echo "online" >> checkServers.csv
else
	echo "offline" >> checkServers.csv
fi
