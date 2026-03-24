#!/usr/bin/env bash
# ~/server_monitor/monitor.sh — Coordinated server monitoring script.
# Runs on every server via cron. Collects local metrics, SSH-probes peers,
# then one server (the leader) aggregates all data and pushes to GitHub.
#
# Cron entry (identical on all machines):
#   */5 * * * * ~/server_monitor/monitor.sh >> ~/server_monitor/logs/cron.log 2>&1
set -u

MONITOR_DIR="$HOME/server_monitor"
source "$MONITOR_DIR/config.sh"

STATE_DIR="$MONITOR_DIR/state"
REACH_DIR="$MONITOR_DIR/reachability"
DATA_DIR="$MONITOR_DIR/data"
LOG_FILE="$MONITOR_DIR/logs/monitor.log"
LOCK_DIR="$MONITOR_DIR/lock"

HOSTNAME_SHORT=$(hostname -s)

mkdir -p "$STATE_DIR" "$REACH_DIR" "$DATA_DIR" "$DATA_DIR/archive" "$MONITOR_DIR/logs"

# --- Logging ---

log_msg() {
    echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] [$HOSTNAME_SHORT] $1" >> "$LOG_FILE"
}

# Rotate log if > 1MB
if [ -f "$LOG_FILE" ]; then
    _log_size=$(stat -c%s "$LOG_FILE" 2>/dev/null || stat -f%z "$LOG_FILE" 2>/dev/null || echo 0)
    if [ "$_log_size" -gt 1048576 ]; then
        mv "$LOG_FILE" "${LOG_FILE}.old"
    fi
fi

log_msg "=== monitor.sh start ==="

# ============================================================
# PHASE 1: Collect own metrics
# ============================================================

ts_utc=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
ts_epoch=$(date -u +"%s")

# -- CUDA / GPU --
cuda_ok=0
gpu_util="null"
gpu_count="null"
gpu_free="null"
gpu_names="null"

if command -v nvidia-smi >/dev/null 2>&1; then
    gpu_csv=$(nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total,name --format=csv,noheader,nounits 2>/dev/null)
    if [ $? -eq 0 ] && [ -n "$gpu_csv" ]; then
        cuda_ok=1
        _count=0; _free=0; _util_sum=0; _names=""
        while IFS=',' read -r util mem_used mem_total gname; do
            util=$(echo "$util" | tr -d ' ')
            mem_used=$(echo "$mem_used" | tr -d ' ')
            gname=$(echo "$gname" | xargs)
            _count=$((_count + 1))
            _util_sum=$((_util_sum + util))
            if [ "$util" -lt 10 ] && [ "$mem_used" -lt 500 ]; then
                _free=$((_free + 1))
            fi
            if [ -n "$_names" ]; then _names="${_names}, ${gname}"; else _names="$gname"; fi
        done <<< "$gpu_csv"
        if [ "$_count" -gt 0 ]; then
            gpu_util=$((_util_sum / _count))
        fi
        gpu_count=$_count
        gpu_free=$_free
        gpu_names="\"$_names\""
    fi
fi

# -- Mumax3 --
mumax_ok=0
mumax_version="null"
cuda_driver="null"
if [ -x "$MUMAX3_BIN" ]; then
    _mumax_out=$($MUMAX3_BIN -test 2>&1 || true)
    if echo "$_mumax_out" | grep -q "//GPU info:"; then
        mumax_ok=1
        _cd=$(echo "$_mumax_out" | grep -oP 'CUDA Driver \K[0-9]+\.[0-9]+' | head -1)
        if [ -n "$_cd" ]; then cuda_driver="\"$_cd\""; fi
        _mv=$(echo "$_mumax_out" | grep -oP '//mumax \K[0-9]+\.[0-9]+' | head -1)
        if [ -n "$_mv" ]; then mumax_version="\"$_mv\""; fi
    fi
fi

# -- CPU utilization --
cpu_util="null"
if [ -f /proc/stat ]; then
    _s1=$(awk '/^cpu / {total=$2+$3+$4+$5+$6+$7+$8; idle=$5+$6; print total, idle}' /proc/stat)
    sleep 1
    _s2=$(awk '/^cpu / {total=$2+$3+$4+$5+$6+$7+$8; idle=$5+$6; print total, idle}' /proc/stat)
    _dt=$(( $(echo "$_s2" | awk '{print $1}') - $(echo "$_s1" | awk '{print $1}') ))
    _di=$(( $(echo "$_s2" | awk '{print $2}') - $(echo "$_s1" | awk '{print $2}') ))
    if [ "$_dt" -gt 0 ]; then
        cpu_util=$(awk "BEGIN {printf \"%.1f\", 100 * ($_dt - $_di) / $_dt}")
    fi
fi

# -- RAM --
ram_free="null"
ram_total="null"
if [ -f /proc/meminfo ]; then
    _total_kb=$(awk '/MemTotal/ {print $2}' /proc/meminfo)
    _avail_kb=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    if [ -n "$_total_kb" ] && [ -n "$_avail_kb" ]; then
        ram_total=$(awk "BEGIN {printf \"%.1f\", $_total_kb / 1048576}")
        ram_free=$(awk "BEGIN {printf \"%.1f\", $_avail_kb / 1048576}")
    fi
fi

# -- Per-user resource usage --
users_json="[]"
_user_cpu_ram=$(ps -eo user:32,%cpu,%mem --no-headers 2>/dev/null | \
    awk '{cpu[$1]+=$2; mem[$1]+=$3; cnt[$1]++} END {for(u in cpu) print u, cpu[u], mem[u], cnt[u]}')

_user_gpu=""
if [ "$cuda_ok" -eq 1 ] && command -v nvidia-smi >/dev/null 2>&1; then
    _pmon_all=$(nvidia-smi pmon -s um -c 1 2>/dev/null)
    # Find fb column dynamically from header (varies by driver version)
    _fb_col=$(echo "$_pmon_all" | head -1 | awk '{for(i=1;i<=NF;i++) if($i=="fb"){print i-1;exit}}')
    [ -z "$_fb_col" ] && _fb_col=8
    _pmon=$(echo "$_pmon_all" | grep -v '^#')
    if [ -n "$_pmon" ]; then
        _user_gpu=$(echo "$_pmon" | awk -v fb="$_fb_col" '$2 != "-" && $2 != "" {sm=($4=="-"?0:$4); fbv=($fb=="-"?0:$fb); print $2, sm, fbv}' | while read pid sm fbm; do
            _u=$(ps -o user:32= -p "$pid" 2>/dev/null | tr -d ' ')
            [ -z "$_u" ] && continue
            echo "$_u $sm $fbm"
        done | awk '{gpu[$1]+=$2; gmem[$1]+=$3} END {for(u in gpu) print u, gpu[u], gmem[u]}')
    fi
fi

users_json=$(python3 -c "
import os, sys, json
cpu_ram = {}
for line in '''${_user_cpu_ram}'''.strip().split('\n'):
    if not line.strip(): continue
    parts = line.split()
    if len(parts) < 4: continue
    user = parts[0]
    try:
        uid = int(os.popen('id -u ' + user + ' 2>/dev/null').read().strip())
    except (ValueError, OSError):
        continue
    if uid < 1000: continue
    cpu_ram[user] = {'cpu_pct': round(float(parts[1]),1), 'ram_pct': round(float(parts[2]),1), 'num_processes': int(parts[3])}

gpu_data = {}
for line in '''${_user_gpu}'''.strip().split('\n'):
    if not line.strip(): continue
    parts = line.split()
    if len(parts) < 3: continue
    gpu_data[parts[0]] = {'gpu_pct': round(float(parts[1]),1), 'gpu_mem_mb': int(float(parts[2]))}

all_users = sorted(set(list(cpu_ram.keys()) + list(gpu_data.keys())))
result = []
for u in all_users:
    cr = cpu_ram.get(u, {'cpu_pct':0,'ram_pct':0,'num_processes':0})
    gd = gpu_data.get(u, {'gpu_pct':0,'gpu_mem_mb':0})
    result.append({'user':u, 'cpu_pct':cr['cpu_pct'], 'gpu_pct':gd['gpu_pct'], 'gpu_mem_mb':gd['gpu_mem_mb'], 'ram_pct':cr['ram_pct'], 'num_processes':cr['num_processes']})
print(json.dumps(result))
" 2>/dev/null || echo "[]")

# -- Write state file atomically --
_tmp_state="$STATE_DIR/.${HOSTNAME_SHORT}.json.tmp"
cat > "$_tmp_state" <<ENDJSON
{
  "server": "${HOSTNAME_SHORT}",
  "timestamp_utc": "${ts_utc}",
  "timestamp_epoch": ${ts_epoch},
  "cuda_ok": ${cuda_ok},
  "mumax3_ok": ${mumax_ok},
  "gpu_util_pct": ${gpu_util},
  "cpu_util_pct": ${cpu_util},
  "ram_free_gb": ${ram_free},
  "ram_total_gb": ${ram_total},
  "gpu_count": ${gpu_count},
  "gpu_free_count": ${gpu_free},
  "gpu_names": ${gpu_names},
  "mumax3_version": ${mumax_version},
  "cuda_driver_version": ${cuda_driver},
  "users": ${users_json}
}
ENDJSON
mv "$_tmp_state" "$STATE_DIR/${HOSTNAME_SHORT}.json"
log_msg "Phase 1: wrote state/${HOSTNAME_SHORT}.json"

# ============================================================
# PHASE 2: SSH probe peers
# ============================================================

_reach_json="\"observer\": \"${HOSTNAME_SHORT}\", \"timestamp_epoch\": ${ts_epoch}, \"targets\": {"
_first=1

for target in $SERVERS; do
    [ "$target" = "$HOSTNAME_SHORT" ] && continue
    if ssh -o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=accept-new "$target" "echo ok" >/dev/null 2>&1; then
        _ssh_val=1
    else
        _ssh_val=0
    fi
    if [ "$_first" -eq 1 ]; then
        _reach_json="${_reach_json}\"${target}\": ${_ssh_val}"
        _first=0
    else
        _reach_json="${_reach_json}, \"${target}\": ${_ssh_val}"
    fi
done

_reach_json="{${_reach_json}}}"

_tmp_reach="$REACH_DIR/.${HOSTNAME_SHORT}.json.tmp"
echo "$_reach_json" > "$_tmp_reach"
mv "$_tmp_reach" "$REACH_DIR/${HOSTNAME_SHORT}.json"
log_msg "Phase 2: wrote reachability/${HOSTNAME_SHORT}.json"

# ============================================================
# PHASE 3: Leader election + aggregate + push
# ============================================================

# Brief delay to let slower servers finish writing state files
sleep 3

# -- Check for stale lock --
if [ -d "$LOCK_DIR" ]; then
    if [ -f "$LOCK_DIR/info" ]; then
        _lock_ts=$(python3 -c "import json; print(json.load(open('$LOCK_DIR/info'))['ts'])" 2>/dev/null || echo 0)
        _lock_age=$(( $(date +%s) - _lock_ts ))
        if [ "$_lock_age" -gt "$LOCK_MAX_AGE" ]; then
            log_msg "Phase 3: removing stale lock (age=${_lock_age}s)"
            rm -rf "$LOCK_DIR"
        else
            log_msg "Phase 3: lock held (age=${_lock_age}s), exiting"
            exit 0
        fi
    else
        # Lock dir exists but no info file — broken, remove
        rm -rf "$LOCK_DIR"
    fi
fi

# -- Acquire lock (mkdir is atomic on NFS) --
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
    log_msg "Phase 3: lock acquired by another server, exiting"
    exit 0
fi

# Ensure lock is released on exit (normal or crash)
cleanup_lock() {
    rm -rf "$LOCK_DIR"
}
trap cleanup_lock EXIT

echo "{\"holder\": \"${HOSTNAME_SHORT}\", \"ts\": $(date +%s)}" > "$LOCK_DIR/info"
log_msg "Phase 3: acquired lock — this server is the leader"

# -- Run data pipeline --
python3 "$MONITOR_DIR/process_data.py" \
    --state-dir "$STATE_DIR" \
    --reach-dir "$REACH_DIR" \
    --data-dir "$DATA_DIR" \
    --stale-threshold "$STALE_THRESHOLD" \
    --reach-threshold "$REACHABILITY_THRESHOLD" \
    --leader "$HOSTNAME_SHORT"

if [ $? -ne 0 ]; then
    log_msg "Phase 3: process_data.py failed"
    exit 1
fi

# -- Push files to GitHub --
push_to_github() {
    local local_file="$1"
    local repo_path="$2"
    local api_url="https://api.github.com/repos/${REPO}/contents/${repo_path}"
    local content_b64
    content_b64=$(base64 -w 0 "$local_file" 2>/dev/null || base64 "$local_file")

    local sha
    sha=$(curl -sf -H "Authorization: token ${GITHUB_TOKEN}" \
        -H "Accept: application/vnd.github.v3+json" \
        "$api_url" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('sha',''))" 2>/dev/null || true)

    local payload
    if [ -n "$sha" ]; then
        payload="{\"message\":\"dashboard update ${ts_utc}\",\"content\":\"${content_b64}\",\"sha\":\"${sha}\"}"
    else
        payload="{\"message\":\"dashboard update ${ts_utc}\",\"content\":\"${content_b64}\"}"
    fi

    local _resp_body
    _resp_body=$(mktemp)
    local http_code
    http_code=$(curl -s -o "$_resp_body" -w "%{http_code}" -X PUT \
        -H "Authorization: token ${GITHUB_TOKEN}" \
        -H "Accept: application/vnd.github.v3+json" \
        "$api_url" \
        -d "$payload")

    if [ "$http_code" = "200" ] || [ "$http_code" = "201" ]; then
        log_msg "Phase 3: pushed ${repo_path} (HTTP ${http_code})"
    else
        local _err
        _err=$(head -c 200 "$_resp_body" 2>/dev/null)
        log_msg "Phase 3: push FAILED ${repo_path} (HTTP ${http_code}) ${_err}"
    fi
    rm -f "$_resp_body"
}

if [ ! -f "$DATA_DIR/dashboard.json" ]; then
    log_msg "Phase 3: dashboard.json not found"
    exit 1
fi

push_to_github "$DATA_DIR/dashboard.json" "data/dashboard.json"

if [ -f "$DATA_DIR/user_stats.json" ]; then
    push_to_github "$DATA_DIR/user_stats.json" "data/user_stats.json"
fi

echo "[${ts_utc}] Leader ${HOSTNAME_SHORT}: push done"
log_msg "=== monitor.sh done ==="
