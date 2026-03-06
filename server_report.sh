#!/usr/bin/env bash
# Runs ON each server via cron. Checks local health, uploads to GitHub.
# Usage: SERVER_NAME=nsc1 GITHUB_TOKEN=ghp_xxx bash server_report.sh
set -u

REPO="benwwalker1/serverStatus"
SERVER_NAME="${SERVER_NAME:?Set SERVER_NAME (e.g. nsc1)}"
GITHUB_TOKEN="${GITHUB_TOKEN:?Set GITHUB_TOKEN}"
FILE_PATH="data/live/${SERVER_NAME}.json"
API_URL="https://api.github.com/repos/${REPO}/contents/${FILE_PATH}"

# --- Collect metrics ---

ts_utc=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
ts_epoch=$(date -u +"%s")

# CUDA / GPU
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

# Mumax3
mumax_ok=0
if command -v mumax3 >/dev/null 2>&1; then
  if mumax3 -test >/dev/null 2>&1; then
    mumax_ok=1
  fi
fi

# CPU utilization
cpu_util="null"
if command -v top >/dev/null 2>&1; then
  idle=$(top -bn2 -d 0.3 2>/dev/null | awk '/Cpu\(s\)/ {idle=$8} END {if (idle != "") print idle}')
  if [ -n "$idle" ]; then
    cpu_util=$(awk "BEGIN {printf \"%.1f\", 100 - $idle}")
  fi
fi

# RAM
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

# --- Build JSON ---

json=$(cat <<ENDJSON
{
  "server": "${SERVER_NAME}",
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
  "gpu_names": ${gpu_names}
}
ENDJSON
)

# --- Upload to GitHub ---

content_b64=$(echo "$json" | base64 -w 0 2>/dev/null || echo "$json" | base64)

# Get current file SHA (needed for updates, empty for new files)
sha=$(curl -sf -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  "$API_URL" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('sha',''))" 2>/dev/null || true)

if [ -n "$sha" ]; then
  payload="{\"message\":\"${SERVER_NAME} report ${ts_utc}\",\"content\":\"${content_b64}\",\"sha\":\"${sha}\"}"
else
  payload="{\"message\":\"${SERVER_NAME} report ${ts_utc}\",\"content\":\"${content_b64}\"}"
fi

http_code=$(curl -s -o /dev/null -w "%{http_code}" -X PUT \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  "$API_URL" \
  -d "$payload")

if [ "$http_code" = "200" ] || [ "$http_code" = "201" ]; then
  echo "[${ts_utc}] ${SERVER_NAME}: uploaded OK"
else
  echo "[${ts_utc}] ${SERVER_NAME}: upload failed (HTTP ${http_code})" >&2
  exit 1
fi
