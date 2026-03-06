#!/usr/bin/env bash
set -u

HOSTS=("nsc1.utdallas.edu" "nsc2.utdallas.edu" "nsc3.utdallas.edu" "nsc4.utdallas.edu")
CSV_FILE="data/status.csv"
SSH_USER="${SSH_USER:-$(whoami)}"
SSH_OPTS=(-o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new -o ServerAliveInterval=5 -o ServerAliveCountMax=2)

CSV_HEADER="timestamp_utc,timestamp_epoch,server,ping,ssh,cuda_ok,mumax3_ok,gpu_util_pct,cpu_util_pct,ram_free_gb,ram_total_gb,gpu_count,gpu_free_count,gpu_names"

mkdir -p "$(dirname "$CSV_FILE")"

if [[ ! -f "$CSV_FILE" || "$(head -n1 "$CSV_FILE" 2>/dev/null)" != "$CSV_HEADER" ]]; then
  echo "$CSV_HEADER" > "$CSV_FILE"
fi

check_server() {
  local host="$1"
  local ts_utc ts_epoch
  ts_utc=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  ts_epoch=$(date -u +"%s")

  local ping_ok="0" ssh_ok="0" cuda_ok="0" mumax_ok="0"
  local gpu_util="NA" cpu_util="NA" ram_free="NA" ram_total="NA"
  local gpu_count="NA" gpu_free="NA" gpu_names="NA"

  # 1) Ping
  if ping -c 2 -W 3 "$host" >/dev/null 2>&1; then
    ping_ok="1"
  fi

  # 2-6) SSH-based checks (only if ping works)
  if [[ "$ping_ok" == "1" ]]; then
    local ssh_output
    ssh_output=$(ssh "${SSH_OPTS[@]}" "${SSH_USER}@${host}" 'bash -s' <<'REMOTE_SCRIPT' 2>/dev/null) && ssh_ok="1" || true
echo "---SSH_OK---"

# GPU info via nvidia-smi
if command -v nvidia-smi >/dev/null 2>&1; then
  gpu_csv=$(nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total,name --format=csv,noheader,nounits 2>/dev/null)
  if [ $? -eq 0 ] && [ -n "$gpu_csv" ]; then
    echo "---CUDA_OK---"
    gpu_count=0
    gpu_free=0
    gpu_util_sum=0
    gpu_name_list=""
    while IFS=',' read -r util mem_used mem_total gname; do
      util=$(echo "$util" | tr -d ' ')
      mem_used=$(echo "$mem_used" | tr -d ' ')
      gname=$(echo "$gname" | tr -d ' ' | tr ',' ';')
      gpu_count=$((gpu_count + 1))
      gpu_util_sum=$((gpu_util_sum + util))
      # GPU is "free" if utilization < 10% and memory used < 500 MiB
      if [ "$util" -lt 10 ] && [ "$mem_used" -lt 500 ]; then
        gpu_free=$((gpu_free + 1))
      fi
      if [ -n "$gpu_name_list" ]; then
        gpu_name_list="${gpu_name_list};${gname}"
      else
        gpu_name_list="$gname"
      fi
    done <<< "$gpu_csv"
    if [ "$gpu_count" -gt 0 ]; then
      gpu_util_avg=$((gpu_util_sum / gpu_count))
    else
      gpu_util_avg="NA"
    fi
    echo "GPU_UTIL=${gpu_util_avg}"
    echo "GPU_COUNT=${gpu_count}"
    echo "GPU_FREE=${gpu_free}"
    echo "GPU_NAMES=${gpu_name_list}"
  else
    echo "---CUDA_FAIL---"
  fi
else
  echo "---CUDA_MISSING---"
fi

# mumax3 check
if command -v mumax3 >/dev/null 2>&1; then
  if mumax3 -version >/dev/null 2>&1 || mumax3 -v >/dev/null 2>&1; then
    echo "---MUMAX_OK---"
  else
    echo "---MUMAX_FAIL---"
  fi
else
  echo "---MUMAX_MISSING---"
fi

# CPU utilization
if command -v top >/dev/null 2>&1; then
  cpu_idle=$(top -bn2 -d 0.3 2>/dev/null | awk '/Cpu\(s\)/ {idle=$8} END {if (idle != "") print idle}')
  if [ -n "$cpu_idle" ]; then
    echo "CPU_UTIL=$(awk "BEGIN {printf \"%.1f\", 100 - $cpu_idle}")"
  fi
fi

# RAM info
if [ -f /proc/meminfo ]; then
  mem_total_kb=$(awk '/MemTotal/ {print $2}' /proc/meminfo)
  mem_avail_kb=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
  if [ -n "$mem_total_kb" ] && [ -n "$mem_avail_kb" ]; then
    echo "RAM_TOTAL=$(awk "BEGIN {printf \"%.1f\", $mem_total_kb / 1048576}")"
    echo "RAM_FREE=$(awk "BEGIN {printf \"%.1f\", $mem_avail_kb / 1048576}")"
  fi
fi
REMOTE_SCRIPT

    # Parse ssh_output
    if echo "$ssh_output" | grep -q "---SSH_OK---"; then
      ssh_ok="1"

      if echo "$ssh_output" | grep -q "---CUDA_OK---"; then
        cuda_ok="1"
        gpu_util=$(echo "$ssh_output" | sed -n 's/^GPU_UTIL=//p' | tail -1)
        gpu_count=$(echo "$ssh_output" | sed -n 's/^GPU_COUNT=//p' | tail -1)
        gpu_free=$(echo "$ssh_output" | sed -n 's/^GPU_FREE=//p' | tail -1)
        gpu_names=$(echo "$ssh_output" | sed -n 's/^GPU_NAMES=//p' | tail -1)
      fi

      if echo "$ssh_output" | grep -q "---MUMAX_OK---"; then
        mumax_ok="1"
      fi

      local cpu_val
      cpu_val=$(echo "$ssh_output" | sed -n 's/^CPU_UTIL=//p' | tail -1)
      [[ -n "$cpu_val" ]] && cpu_util="$cpu_val"

      local ram_t ram_f
      ram_t=$(echo "$ssh_output" | sed -n 's/^RAM_TOTAL=//p' | tail -1)
      ram_f=$(echo "$ssh_output" | sed -n 's/^RAM_FREE=//p' | tail -1)
      [[ -n "$ram_t" ]] && ram_total="$ram_t"
      [[ -n "$ram_f" ]] && ram_free="$ram_f"
    fi
  fi

  # Sanitize gpu_names (remove commas)
  gpu_names=$(echo "$gpu_names" | tr ',' ';')

  echo "${ts_utc},${ts_epoch},${host},${ping_ok},${ssh_ok},${cuda_ok},${mumax_ok},${gpu_util},${cpu_util},${ram_free},${ram_total},${gpu_count},${gpu_free},${gpu_names}" >> "$CSV_FILE"
  echo "  ${host}: ping=${ping_ok} ssh=${ssh_ok} cuda=${cuda_ok} mumax=${mumax_ok} gpu_util=${gpu_util}% cpu=${cpu_util}% ram_free=${ram_free}GB gpus_free=${gpu_free}/${gpu_count}"
}

main() {
  echo "=== Server check: $(date -u) ==="
  for host in "${HOSTS[@]}"; do
    check_server "$host"
  done
  echo "=== Done ==="
}

main
