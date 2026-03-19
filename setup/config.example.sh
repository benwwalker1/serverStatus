#!/usr/bin/env bash
# ~/server_monitor/config.sh — Shared configuration for all servers.
# Copy this to ~/server_monitor/config.sh and fill in GITHUB_TOKEN.
# chmod 600 ~/server_monitor/config.sh

REPO="benwwalker1/serverStatus"
SERVERS="nsc1 nsc2 nsc3 nsc4"
STALE_THRESHOLD=600            # seconds — server stale if no self-report in 10 min
REACHABILITY_THRESHOLD=600     # seconds — ignore SSH probe results older than this
LOCK_MAX_AGE=300               # seconds — stale lock timeout (= cron interval)
MUMAX3_BIN="/usr/local/bin/mumax3"
GITHUB_TOKEN="REPLACE_ME"     # GitHub personal access token with repo scope
