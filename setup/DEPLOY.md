# Deployment Guide: Coordinated Server Monitoring

## Overview

This system replaces the old per-server push model with a coordinated approach.
All servers share `~/server_monitor/` via NFS. Each server collects its own
metrics and SSH-probes peers. One server (the "leader", elected via NFS-safe
`mkdir` lock) aggregates all data and pushes a single `dashboard.json` to GitHub.

## Prerequisites

- `~/` is shared across nsc1-4 (NFS)
- Python 3 on all servers (RHEL 8+ has it)
- GitHub personal access token with `repo` scope
- SSH keys set up between all servers (BatchMode)

## Step 1: Create directory structure (run once, from any server)

```bash
mkdir -p ~/server_monitor/{state,reachability,data/archive,logs}
```

## Step 2: Deploy scripts (run once, from any server)

Copy the scripts from this repo's `setup/` directory:

```bash
# From your local checkout of the repo:
cp setup/monitor.sh ~/server_monitor/monitor.sh
cp setup/process_data.py ~/server_monitor/process_data.py
chmod +x ~/server_monitor/monitor.sh
```

## Step 3: Create config (run once, from any server)

```bash
cp setup/config.example.sh ~/server_monitor/config.sh
chmod 600 ~/server_monitor/config.sh
```

Edit `~/server_monitor/config.sh` and set `GITHUB_TOKEN` to your actual token:

```bash
vi ~/server_monitor/config.sh
# Change: GITHUB_TOKEN="REPLACE_ME"
# To:     GITHUB_TOKEN="ghp_your_actual_token"
```

## Step 4: Seed historical data (run once, from any server)

Copy the existing CSV history so the dashboard has continuity:

```bash
cp /path/to/serverStatus/data/status.csv ~/server_monitor/data/status.csv
```

## Step 5: Test manually (from any server)

```bash
bash ~/server_monitor/monitor.sh
```

Check that:
- `~/server_monitor/state/$(hostname -s).json` was created with metrics
- `~/server_monitor/reachability/$(hostname -s).json` was created with SSH results
- `~/server_monitor/data/dashboard.json` was generated
- The push to GitHub succeeded (check `~/server_monitor/logs/monitor.log`)

## Step 6: Remove old cron entries (on each server)

```bash
crontab -e
# Remove the old line that looks like:
# */5 * * * * SERVER_NAME=nscX GITHUB_TOKEN=ghp_xxx bash /path/to/server_report.sh ...
```

## Step 7: Add new cron entry (on each server)

The cron entry is identical on all machines — the script auto-detects hostname:

```bash
crontab -e
# Add:
*/5 * * * * ~/server_monitor/monitor.sh >> ~/server_monitor/logs/cron.log 2>&1
```

## Step 8: Verify

After 5-10 minutes:

1. Check `~/server_monitor/logs/monitor.log` — should show one "leader" per cycle
2. Check `~/server_monitor/state/` — should have a fresh JSON per active server
3. Visit the GitHub Pages dashboard — should show all servers with correct status
4. Check the stale banner — if you stop all crons for 20 min, the frontend shows a warning

## Troubleshooting

### Lock is stuck
If the lock directory persists beyond 5 min (LOCK_MAX_AGE), the next cron run
will clean it up automatically. To manually clear:
```bash
rm -rf ~/server_monitor/lock
```

### Push failures
Check `~/server_monitor/logs/monitor.log` for HTTP error codes.
Common causes:
- Token expired: regenerate and update `config.sh`
- Rate limited: GitHub API allows 5000 requests/hour, this uses ~12/hour

### Server shows "degraded"
The server is SSH-reachable from peers but not self-reporting metrics.
Check if cron is running on that server:
```bash
ssh nscX "crontab -l | grep monitor"
```

### CSV migration
The first run may auto-migrate the CSV header from the old format (with `online`
column) to the new format (with `status` column). This is handled automatically.
