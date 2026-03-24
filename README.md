# Lab Server Status Dashboard

A self-monitoring system for lab GPU servers (nsc1–nsc4) behind a VPN. Servers push health data to GitHub; a static dashboard on GitHub Pages displays it. No external monitoring service, no sudo, no inbound connections required.

**Live dashboard:** [benwwalker1.github.io/serverStatus](https://benwwalker1.github.io/serverStatus)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Shared home directory (NFS)                 │
│                                                             │
│  ~/server_monitor/                                          │
│  ├── state/           ← each server writes its own JSON     │
│  │   ├── nsc1.json                                          │
│  │   ├── nsc2.json                                          │
│  │   └── ...                                                │
│  ├── reachability/    ← each server writes SSH probe results│
│  │   ├── nsc1.json                                          │
│  │   └── ...                                                │
│  ├── data/            ← leader writes CSV history + archive │
│  │   ├── status.csv                                         │
│  │   ├── user_history.csv                                   │
│  │   ├── dashboard.json  ← aggregated output for GitHub     │
│  │   ├── user_stats.json ← per-user stats for GitHub        │
│  │   └── archive/                                           │
│  ├── lock/            ← mkdir-based leader election         │
│  ├── monitor.sh       ← the single script, run via cron    │
│  ├── process_data.py  ← data pipeline, called by leader    │
│  ├── config.sh        ← shared config (token, thresholds)  │
│  └── logs/                                                  │
└─────────────────────────────────────────────────────────────┘

Every 5 minutes, on every server:

  Phase 1: Collect own metrics + per-user usage → write state/<hostname>.json
  Phase 2: SSH-probe peer servers → write reachability/<hostname>.json
  Phase 3: Leader election → one server aggregates + pushes to GitHub
```

The frontend (`index.html`) is a static page on GitHub Pages that fetches `data/dashboard.json` and `data/user_stats.json` from the repo's raw content URL.

## How status is determined

Each server's status is one of **up**, **degraded**, or **down**, determined by combining two signals:

| Self-report fresh? | SSH-reachable from peers? | Status       |
|--------------------|--------------------------|--------------|
| Yes                | (any)                    | **up**       |
| No                 | Yes                      | **degraded** |
| No                 | No                       | **down**     |

- **Fresh self-report** means the server wrote its `state/<hostname>.json` within the last 10 minutes (configurable via `STALE_THRESHOLD`).
- **SSH-reachable** means at least one other server successfully ran `ssh <target> "echo ok"` within the same threshold window.

This two-signal approach prevents false positives: a server with a stuck cron job but working SSH shows as "degraded" rather than falsely "down".

## Metrics collected

Each server reports every 5 minutes:

| Metric | Source |
|--------|--------|
| CUDA status | `nvidia-smi` query |
| GPU utilization, count, free count | `nvidia-smi` (free = <10% util AND <500MB VRAM) |
| GPU names | `nvidia-smi --query-gpu=name` |
| Mumax3 status | `mumax3 -test` output parsing |
| Mumax3 version | Extracted from `mumax3 -test` (`//mumax X.Y`) |
| CUDA driver version | Extracted from `mumax3 -test` (`CUDA Driver X.Y`) |
| CPU utilization | `/proc/stat` delta over 1 second |
| RAM free / total | `/proc/meminfo` |
| Per-user CPU/RAM usage | `ps -eo user:32,%cpu,%mem` aggregated by username |
| Per-user GPU usage | `nvidia-smi pmon -s um -c 1` mapped PID→user via `ps` |
| SSH reachability | `ssh -o BatchMode=yes -o ConnectTimeout=5` to each peer |

### Per-user resource tracking

Each state file includes a `"users"` array with per-user CPU%, GPU%, GPU memory (MB), RAM%, and process count. The collection pipeline:

1. **CPU/RAM:** `ps -eo user:32,%cpu,%mem --no-headers` aggregated per username via `awk`
2. **GPU:** `nvidia-smi pmon -s um -c 1` provides per-process GPU utilization and framebuffer memory. The `fb` column position is detected dynamically from the header (varies by CUDA driver version). Each PID is mapped to a username via `ps -o user:32= -p <PID>`.
3. **Filtering:** Users are filtered through three layers:
   - **Explicit exclusion list:** `root`, `gdm`, `libstoragemgmt`, `nobody`, `dbus`, `polkitd`, `sssd`, `chrony`, `sshd`, and ~20 other system accounts
   - **UID check:** Users with UID < 1000 are excluded
   - **Shell check:** Users with `/sbin/nologin` or `/bin/false` shells are excluded
4. **Merging:** An inline Python script merges CPU/RAM and GPU data per user, applies filtering, and outputs a JSON array.

The same exclusion list is enforced in both `monitor.sh` (collection) and `process_data.py` (aggregation), so system accounts are filtered even from historical CSV data.

## Per-user statistics pipeline

Separate from the main server metrics, a parallel pipeline tracks per-user resource usage over time:

```
state/<host>.json "users" array
        │
        ▼
  data/user_history.csv     ← append-only, one row per user per server per cycle
        │
        ▼
  generate_user_stats()     ← compute averages per time window
        │
        ▼
  data/user_stats.json      ← pushed to GitHub alongside dashboard.json
```

**Time windows:** Current snapshot, 24-hour average, 7-day average, 30-day average, and all-time average.

**Output schema** (`data/user_stats.json`):
```json
{
  "generated_epoch": 1774346412,
  "servers": {
    "nsc2": {
      "current": [
        {"user": "jdoe", "cpu_pct": 12.5, "gpu_pct": 85.0, "gpu_mem_mb": 174, "ram_pct": 3.2, "num_processes": 8}
      ],
      "averages": {
        "24h": [{"user": "jdoe", "cpu_pct": 10.1, "gpu_pct": 72.3, "gpu_mem_mb": 150, "ram_pct": 3.0}],
        "7d":  [],
        "30d": [],
        "all": []
      }
    }
  }
}
```

**Archival:** User CSV rows older than 30 days are moved to `data/archive/users-YYYY-MM.csv`.

## Dashboard features

- **Status cards** with live metrics, version info, and SSH reachability
- **7-day sparkline** per server per check (Online, CUDA, Mumax3) — green/red/gray bars by hour
- **Uptime SLO** percentages: 24h, 7d, 30d, all-time
- **Per-user resource usage** — expandable accordion in each server card showing CPU%, GPU%, GPU memory, and RAM% per user, with tabs to switch between Current / 24h / 7d / 30d / All averages
- **Incident log** with state-change detection (up/down transitions), deduplication of cascading failures, and server grouping
- **Stale data banner** when all monitoring is down
- Auto-refreshes every 5 minutes
- Times shown in US Central, EU Central, and UTC

## Race conditions and leader election

All four servers run the same cron job simultaneously on a shared NFS filesystem. The system handles this cleanly:

### Atomic state writes
Each server writes its own state file via write-to-temp-then-`mv`:
```
write → state/.nsc2.json.tmp
mv    → state/nsc2.json        (atomic on POSIX)
```
No server reads another server's temp file. No partial reads.

### Leader election via `mkdir`
`mkdir` is atomic on both local and NFS filesystems — exactly one process succeeds when multiple try to create the same directory simultaneously. The lock lifecycle:

1. All servers finish Phases 1–2 (metrics + SSH probes), then `sleep 3` to let slower peers finish writing.
2. Each server attempts `mkdir ~/server_monitor/lock/`.
3. **Exactly one succeeds** — it becomes the leader, writes `lock/info` with its hostname and timestamp, runs the data pipeline, and pushes to GitHub.
4. All others see the `mkdir` fail and exit immediately.
5. The leader removes the lock directory on exit (via a `trap EXIT` handler, so it's cleaned up even on crashes).

### Stale lock recovery
If the leader crashes hard enough that the trap doesn't fire (kernel panic, NFS disconnect, `kill -9`), the lock directory persists. Every subsequent cron run checks the lock's age:
- If older than `LOCK_MAX_AGE` (default: 300s = one cron interval), it's forcibly removed and a new leader is elected.
- This means at most one 5-minute cycle is skipped after a hard crash.

### No 409 conflicts
The old system had every server independently pushing to the GitHub API, causing HTTP 409 (conflict) race conditions. The new system has a single push per cycle from one leader, eliminating this entirely.

## What happens when servers go down

### One server goes down
The remaining servers continue the cycle normally. One of them wins leader election, aggregates data, and pushes. The down server's state file becomes stale (>10 min old) and no peer can SSH into it, so the pipeline marks it **down**. The dashboard shows it as offline with its last known metrics.

### Multiple servers go down, one remains
The surviving server:
1. Writes its own state file.
2. SSH-probes all peers (all fail — recorded as unreachable).
3. Wins leader election uncontested.
4. The pipeline sees stale state files + failed SSH probes for the dead servers → marks them **down**.
5. Pushes `dashboard.json` to GitHub showing itself as **up** and the rest as **down**.

As long as one server is alive and can reach the GitHub API, the dashboard stays current.

### All servers go down
No cron jobs run. No pushes happen. The `dashboard.json` on GitHub becomes stale. The frontend detects this:

- The dashboard JSON includes a `generated_epoch` timestamp and the `stale_threshold` value.
- If `dashboard.json` is older than `2 × stale_threshold` (default: 20 minutes), a red banner appears:
  > "Dashboard data is Xm old. All servers may be unreachable or the monitoring system is down."

This is the only way the system can signal total failure — since the servers are behind a VPN and unreachable from outside, GitHub Pages can only display what was last pushed. The staleness of the data itself becomes the signal.

### Servers recover after total outage
When any server comes back, its next cron run:
1. Writes a fresh state file.
2. Probes peers (some may still be down).
3. Wins leader election, aggregates, and pushes.
4. The dashboard immediately reflects the new state; the stale banner disappears.

## What happens when GitHub is unreachable

### Short outage (< 10 minutes)
The leader pushes and gets an HTTP error. The push fails, logged to `~/server_monitor/logs/monitor.log`. On the next cycle (5 min later), a new leader retries. The dashboard on GitHub Pages shows slightly stale data (5–10 min old), which is within the normal threshold — no visible impact.

### Longer outage (30–60+ minutes)
The system continues collecting metrics and probing peers locally every 5 minutes. State files and the local CSV stay current on the shared filesystem. Only the push to GitHub fails.

From the dashboard viewer's perspective:
- After ~20 minutes: the stale banner appears, warning that data is old.
- The stale banner grows ("30m ago", "1h ago") but cannot distinguish between "all servers down" and "GitHub unreachable" — both look the same from the outside.

When GitHub becomes reachable again:
- The next leader push succeeds, uploading a fresh `dashboard.json` with **current** server state (not the stale state from when GitHub went down).
- The local CSV has been accumulating rows the whole time, so history continuity is preserved.
- The stale banner disappears immediately.

No data is lost during a GitHub outage — the shared filesystem acts as a local buffer.

## File overview

| File | Purpose |
|------|---------|
| `index.html` | Static dashboard (vanilla JS, GitHub Pages) |
| `setup/monitor.sh` | Cron script — metrics, per-user stats, SSH probes, leader election, push |
| `setup/process_data.py` | Data pipeline — status determination, CSV, history, incidents, user stats |
| `setup/config.example.sh` | Configuration template |
| `setup/DEPLOY.md` | Step-by-step deployment instructions |
| `data/dashboard.json` | Aggregated server output pushed to GitHub by the leader |
| `data/user_stats.json` | Per-user resource statistics pushed to GitHub by the leader |
| `data/status.csv` | Append-only server history (30-day rolling window) |
| `data/user_history.csv` | Append-only per-user history (30-day rolling window, server-side only) |
| `data/archive/` | Monthly CSV archives for data older than 30 days |
| `.github/workflows/pages.yml` | Deploys `index.html` to GitHub Pages on push |

## Configuration

`~/server_monitor/config.sh` (shared via NFS, deployed once):

| Variable | Default | Description |
|----------|---------|-------------|
| `REPO` | `benwwalker1/serverStatus` | GitHub repository (`owner/repo`) |
| `SERVERS` | `nsc1 nsc2 nsc3 nsc4` | Space-separated list of server hostnames |
| `STALE_THRESHOLD` | `600` | Seconds before a server's self-report is considered stale |
| `REACHABILITY_THRESHOLD` | `600` | Seconds before SSH probe results are ignored |
| `LOCK_MAX_AGE` | `300` | Seconds before a stuck lock is forcibly removed |
| `MUMAX3_BIN` | `/usr/local/bin/mumax3` | Path to mumax3 binary |
| `GITHUB_TOKEN` | — | GitHub personal access token with `repo` scope |

## Setup

See [setup/DEPLOY.md](setup/DEPLOY.md) for full deployment instructions. The short version:

```bash
# From any server (shared home dir):
mkdir -p ~/server_monitor/{state,reachability,data/archive,logs}
cp setup/monitor.sh setup/process_data.py ~/server_monitor/
cp setup/config.example.sh ~/server_monitor/config.sh
chmod +x ~/server_monitor/monitor.sh
chmod 600 ~/server_monitor/config.sh
# Edit config.sh — set GITHUB_TOKEN

# On EACH server:
crontab -e
# Add: */5 * * * * ~/server_monitor/monitor.sh >> ~/server_monitor/logs/cron.log 2>&1
```

### Updating scripts after changes

Since `~/server_monitor/` is shared via NFS, updating from any one server updates all of them:

```bash
curl -sL "https://raw.githubusercontent.com/benwwalker1/serverStatus/main/setup/monitor.sh" \
  -o ~/server_monitor/monitor.sh && chmod +x ~/server_monitor/monitor.sh

curl -sL "https://raw.githubusercontent.com/benwwalker1/serverStatus/main/setup/process_data.py" \
  -o ~/server_monitor/process_data.py
```

Changes take effect on the next cron cycle (within 5 minutes).

## Servers

| Server | OS | GPUs | Mumax3 | CUDA Driver |
|--------|----|------|--------|-------------|
| nsc1 | RHEL | — | — | — |
| nsc2 | RHEL 8.10 | 1x GTX 1080 Ti | 3.11 | 12.9 |
| nsc3 | RHEL | 2x RTX 2080 Ti | 3.10 | 13.1 |
| nsc4 | RHEL 9.7 | 2x RTX 2080 Ti | 3.11 | 13.1 |
