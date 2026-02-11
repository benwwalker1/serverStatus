#!/usr/bin/env bash

set -u

HOSTS=("nsc1.utdallas.edu" "nsc2.utdallas.edu" "nsc3.utdallas.edu" "nsc4.utdallas.edu")
CSV_FILE="checkServers.csv"
README_FILE="README.md"
PLOTS_DIR="plots"
LEGACY_PREFIX="checkServers_legacy"
CSV_HEADER="timestamp_utc,timestamp_epoch,server,ping,cuda_ok,mumax3_ok,gpu_utilization,cpu_utilization,cpu_count_logical,cpu_count_physical,gpu_count,gpu_names,memory_total_gb"
SSH_OPTS=(-o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=accept-new)

init_csv() {
  if [[ ! -f "$CSV_FILE" || ! -s "$CSV_FILE" ]]; then
    echo "$CSV_HEADER" > "$CSV_FILE"
    return
  fi

  local first_line
  first_line=$(head -n 1 "$CSV_FILE")

  if [[ "$first_line" != "$CSV_HEADER" ]]; then
    local backup_file
    backup_file="${LEGACY_PREFIX}_$(date -u +%Y%m%dT%H%M%SZ).csv"
    mv "$CSV_FILE" "$backup_file"
    echo "$CSV_HEADER" > "$CSV_FILE"
    echo "Migrated legacy CSV format to $backup_file"
  fi
}

sanitize_csv_field() {
  local value="$1"
  value=${value//$'\n'/ }
  value=${value//$'\r'/ }
  value=${value//,/;}
  echo "$value"
}

is_numeric() {
  [[ "$1" =~ ^[0-9]+(\.[0-9]+)?$ ]]
}

collect_server_status() {
  local host="$1"
  local timestamp_utc="$2"
  local timestamp_epoch="$3"

  local ping_status="offline"
  local cuda_status="unknown"
  local mumax_status="unknown"
  local gpu_utilization="NA"
  local cpu_utilization="NA"
  local cpu_count_logical="NA"
  local cpu_count_physical="NA"
  local gpu_count="NA"
  local gpu_names="NA"
  local memory_total_gb="NA"

  if ping -c 1 -W 1 "$host" >/dev/null 2>&1; then
    ping_status="online"

    local gpu_probe
    gpu_probe=$(ssh "${SSH_OPTS[@]}" "$host" '
      if ! command -v nvidia-smi >/dev/null 2>&1; then
        echo "__STATUS__:missing"
        exit 0
      fi
      out=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits 2>&1)
      rc=$?
      if [ "$rc" -ne 0 ]; then
        echo "__STATUS__:error"
        echo "$out"
        exit 0
      fi
      valid=$(echo "$out" | awk "NF > 0 && \$1 ~ /^[0-9]+(\\.[0-9]+)?$/ {count += 1} END {print count + 0}")
      if [ "$valid" -gt 0 ]; then
        echo "__STATUS__:ok"
        echo "$out"
      else
        echo "__STATUS__:error"
        echo "$out"
      fi
    ' 2>/dev/null || true)

    local gpu_probe_status
    gpu_probe_status=$(echo "$gpu_probe" | head -n1)
    local gpu_raw
    gpu_raw=$(echo "$gpu_probe" | tail -n +2)

    if [[ "$gpu_probe_status" == "__STATUS__:ok" ]]; then
      gpu_utilization=$(echo "$gpu_raw" | awk 'NF > 0 && $1 ~ /^[0-9]+(\.[0-9]+)?$/ {sum += $1; count += 1} END {if (count > 0) printf "%.2f", sum / count; else print "NA"}')
      if is_numeric "$gpu_utilization"; then
        cuda_status="ok"
      else
        cuda_status="error"
        gpu_utilization="NA"
      fi
    elif [[ "$gpu_probe_status" == "__STATUS__:missing" ]]; then
      cuda_status="error"
      gpu_utilization="NA"
    else
      cuda_status="error"
      gpu_utilization="NA"
    fi

    if ssh "${SSH_OPTS[@]}" "$host" 'command -v mumax3 >/dev/null 2>&1 && (mumax3 -version >/dev/null 2>&1 || mumax3 -v >/dev/null 2>&1 || mumax3 >/dev/null 2>&1)' >/dev/null 2>&1; then
      mumax_status="ok"
    else
      mumax_status="error"
    fi

    cpu_utilization=$(ssh "${SSH_OPTS[@]}" "$host" '
      if command -v top >/dev/null 2>&1; then
        top -bn2 -d 0.2 2>/dev/null | awk "/Cpu\\(s\\)/ {idle=\$8} END {if (idle != \"\") printf \"%.2f\", 100-idle}"
      elif command -v vmstat >/dev/null 2>&1; then
        vmstat 1 2 2>/dev/null | tail -n1 | awk "{printf \"%.2f\", 100-\$15}"
      fi
    ' 2>/dev/null || true)
    if ! is_numeric "$cpu_utilization"; then
      cpu_utilization="NA"
    fi

    cpu_count_logical=$(ssh "${SSH_OPTS[@]}" "$host" 'command -v nproc >/dev/null 2>&1 && nproc' 2>/dev/null || true)
    if ! [[ "$cpu_count_logical" =~ ^[0-9]+$ ]]; then
      cpu_count_logical="NA"
    fi

    cpu_count_physical=$(ssh "${SSH_OPTS[@]}" "$host" '
      if command -v lscpu >/dev/null 2>&1; then
        lscpu -p=Core,Socket 2>/dev/null | awk -F, "!/^#/ {seen[\$1\",\"\$2]=1} END {print length(seen)}"
      fi
    ' 2>/dev/null || true)
    if ! [[ "$cpu_count_physical" =~ ^[0-9]+$ ]]; then
      cpu_count_physical="NA"
    fi

    local gpu_names_probe
    gpu_names_probe=$(ssh "${SSH_OPTS[@]}" "$host" '
      if ! command -v nvidia-smi >/dev/null 2>&1; then
        echo "__STATUS__:missing"
        exit 0
      fi
      out=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>&1)
      rc=$?
      if [ "$rc" -ne 0 ]; then
        echo "__STATUS__:error"
        echo "$out"
        exit 0
      fi
      valid=$(echo "$out" | awk "NF > 0 {count += 1} END {print count + 0}")
      if [ "$valid" -gt 0 ]; then
        echo "__STATUS__:ok"
        echo "$out"
      else
        echo "__STATUS__:error"
        echo "$out"
      fi
    ' 2>/dev/null || true)

    local gpu_names_status
    gpu_names_status=$(echo "$gpu_names_probe" | head -n1)
    local gpu_names_raw
    gpu_names_raw=$(echo "$gpu_names_probe" | tail -n +2)

    if [[ "$gpu_names_status" == "__STATUS__:ok" ]]; then
      gpu_count=$(echo "$gpu_names_raw" | awk 'NF>0 {count+=1} END {print count+0}')
      gpu_names=$(echo "$gpu_names_raw" | awk 'NF>0 {gsub(/^[[:space:]]+|[[:space:]]+$/, "", $0); names[++n]=$0} END {for (i=1; i<=n; i++) printf "%s%s", names[i], (i<n?";":"")}')
      [[ -z "$gpu_names" ]] && gpu_names="NA"
    elif [[ "$gpu_names_status" == "__STATUS__:missing" ]]; then
      gpu_count="0"
      gpu_names="nvidia-smi-missing"
    else
      gpu_count="NA"
      gpu_names="nvidia-smi-error"
    fi

    memory_total_gb=$(ssh "${SSH_OPTS[@]}" "$host" 'awk "/MemTotal/ {printf \"%.2f\", \$2/1024/1024}" /proc/meminfo 2>/dev/null' 2>/dev/null || true)
    if ! is_numeric "$memory_total_gb"; then
      memory_total_gb="NA"
    fi
  fi

  gpu_names=$(sanitize_csv_field "$gpu_names")

  echo "$timestamp_utc,$timestamp_epoch,$host,$ping_status,$cuda_status,$mumax_status,$gpu_utilization,$cpu_utilization,$cpu_count_logical,$cpu_count_physical,$gpu_count,$gpu_names,$memory_total_gb"
}

generate_statistics_table() {
  local ordered_hosts
  ordered_hosts=$(printf "%s," "${HOSTS[@]}")
  ordered_hosts=${ordered_hosts%,}

  awk -F',' -v ordered_hosts="$ordered_hosts" '
    BEGIN { split(ordered_hosts, host_list, ",") }
    NR == 1 { next }
    {
      server = $3
      total[server] += 1
      if ($4 == "online") ping_ok[server] += 1
      if ($5 == "ok") cuda_ok[server] += 1
      if ($6 == "ok") mumax_ok[server] += 1
      if ($7 ~ /^[0-9]+(\.[0-9]+)?$/) { gpu_sum[server] += $7; gpu_count[server] += 1; if ($7 > 90) gpu_hot[server] += 1 }
      if ($8 ~ /^[0-9]+(\.[0-9]+)?$/) { cpu_sum[server] += $8; cpu_count[server] += 1; if ($8 > 85) cpu_hot[server] += 1 }
      seen[server] = 1
    }
    function print_row(server) {
      ping_pct = (total[server] > 0) ? (100 * ping_ok[server] / total[server]) : 0
      cuda_pct = (total[server] > 0) ? (100 * cuda_ok[server] / total[server]) : 0
      mumax_pct = (total[server] > 0) ? (100 * mumax_ok[server] / total[server]) : 0
      gpu_avg = (gpu_count[server] > 0) ? sprintf("%.2f%%", gpu_sum[server] / gpu_count[server]) : "NA"
      cpu_avg = (cpu_count[server] > 0) ? sprintf("%.2f%%", cpu_sum[server] / cpu_count[server]) : "NA"

      printf "| %s | %d | %.2f%% | %.2f%% | %.2f%% | %s | %s | %d | %d |\n", server, total[server], ping_pct, cuda_pct, mumax_pct, cpu_avg, gpu_avg, cpu_hot[server] + 0, gpu_hot[server] + 0
    }
    END {
      print "| Server | Samples | Ping uptime | CUDA healthy | Mumax3 healthy | Avg CPU util. | Avg GPU util. | CPU>85% samples | GPU>90% samples |"
      print "| ------ | ------- | ----------- | ------------ | -------------- | ------------- | ------------- | --------------- | --------------- |"
      for (idx in host_list) {
        server = host_list[idx]
        if (server in seen) { print_row(server); printed[server] = 1 }
      }
      for (server in seen) {
        if (!(server in printed)) print_row(server)
      }
    }
  ' "$CSV_FILE"
}

generate_hardware_inventory_table() {
  local ordered_hosts
  ordered_hosts=$(printf "%s," "${HOSTS[@]}")
  ordered_hosts=${ordered_hosts%,}

  awk -F',' -v ordered_hosts="$ordered_hosts" '
    BEGIN { split(ordered_hosts, host_list, ",") }
    NR == 1 { next }
    {
      server = $3
      if (!(server in last_ts) || $2 >= last_ts[server]) {
        last_ts[server] = $2
        cpu_l[server] = $9
        cpu_p[server] = $10
        gpu_c[server] = $11
        gpu_n[server] = $12
        mem[server] = $13
      }
      seen[server] = 1
    }
    END {
      print "| Server | Logical CPUs | Physical CPUs | GPU count | GPU model(s) | RAM total (GB) |"
      print "| ------ | ------------ | ------------- | --------- | ------------ | -------------- |"
      for (idx in host_list) {
        server = host_list[idx]
        if (server in seen) {
          printf "| %s | %s | %s | %s | %s | %s |\n", server, cpu_l[server], cpu_p[server], gpu_c[server], gpu_n[server], mem[server]
          printed[server] = 1
        }
      }
      for (server in seen) {
        if (!(server in printed)) {
          printf "| %s | %s | %s | %s | %s | %s |\n", server, cpu_l[server], cpu_p[server], gpu_c[server], gpu_n[server], mem[server]
        }
      }
    }
  ' "$CSV_FILE"
}

generate_slo_table() {
  local now
  local ordered_hosts
  now=$(date -u +%s)
  ordered_hosts=$(printf "%s," "${HOSTS[@]}")
  ordered_hosts=${ordered_hosts%,}

  awk -F',' -v now="$now" -v ordered_hosts="$ordered_hosts" '
    BEGIN {
      split(ordered_hosts, host_list, ",")
      windows[1] = 24*3600; names[1] = "24h"
      windows[2] = 7*24*3600; names[2] = "7d"
      windows[3] = 30*24*3600; names[3] = "30d"
    }
    NR == 1 { next }
    {
      server = $3
      ts = $2 + 0
      for (i=1; i<=3; i++) {
        if (ts >= now - windows[i]) {
          total[server, i] += 1
          if ($4 == "online") ping_ok[server, i] += 1
          if ($5 == "ok") cuda_ok[server, i] += 1
          if ($6 == "ok") mumax_ok[server, i] += 1
        }
      }
      seen[server] = 1
    }
    END {
      print "| Server | Window | Ping uptime | CUDA healthy | Mumax3 healthy |"
      print "| ------ | ------ | ----------- | ------------ | -------------- |"
      for (idx in host_list) {
        server = host_list[idx]
        if (!(server in seen)) continue
        for (i=1; i<=3; i++) {
          t = total[server, i] + 0
          ping = (t > 0) ? sprintf("%.2f%%", 100 * ping_ok[server, i] / t) : "NA"
          cuda = (t > 0) ? sprintf("%.2f%%", 100 * cuda_ok[server, i] / t) : "NA"
          mumax = (t > 0) ? sprintf("%.2f%%", 100 * mumax_ok[server, i] / t) : "NA"
          printf "| %s | %s | %s | %s | %s |\n", server, names[i], ping, cuda, mumax
        }
        printed[server] = 1
      }
      for (server in seen) {
        if (server in printed) continue
        for (i=1; i<=3; i++) {
          t = total[server, i] + 0
          ping = (t > 0) ? sprintf("%.2f%%", 100 * ping_ok[server, i] / t) : "NA"
          cuda = (t > 0) ? sprintf("%.2f%%", 100 * cuda_ok[server, i] / t) : "NA"
          mumax = (t > 0) ? sprintf("%.2f%%", 100 * mumax_ok[server, i] / t) : "NA"
          printf "| %s | %s | %s | %s | %s |\n", server, names[i], ping, cuda, mumax
        }
      }
    }
  ' "$CSV_FILE"
}

generate_incidents_table() {
  awk -F',' '
    NR == 1 { next }
    {
      server = $3
      ts = $1
      ping = $4
      cuda = $5
      mumax = $6

      if (server in prev_ping && prev_ping[server] != ping) {
        printf "| %s | %s | Ping | %s -> %s |\n", ts, server, prev_ping[server], ping
      }
      if (server in prev_cuda && prev_cuda[server] != cuda) {
        printf "| %s | %s | CUDA | %s -> %s |\n", ts, server, prev_cuda[server], cuda
      }
      if (server in prev_mumax && prev_mumax[server] != mumax) {
        printf "| %s | %s | Mumax3 | %s -> %s |\n", ts, server, prev_mumax[server], mumax
      }

      prev_ping[server] = ping
      prev_cuda[server] = cuda
      prev_mumax[server] = mumax
    }
  ' "$CSV_FILE" | tail -n 25
}

generate_recent_samples() {
  {
    echo "| Timestamp (UTC) | Server | Ping | CUDA | Mumax3 | CPU util. | GPU util. | CPU(logical/physical) | GPU count | RAM GB |"
    echo "| --------------- | ------ | ---- | ---- | ------ | --------- | --------- | -------------------- | --------- | ------ |"
    tail -n 60 "$CSV_FILE" | awk -F',' '
      NR == 1 { next }
      {
        cpu = ($8 == "NA") ? "NA" : $8 "%"
        gpu = ($7 == "NA") ? "NA" : $7 "%"
        cpuc = $9 "/" $10
        printf "| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |\n", $1, $3, $4, $5, $6, cpu, gpu, cpuc, $11, $13
      }
    '
  }
}

generate_current_status_table() {
  local cycle_file="$1"
  echo "| Server | Ping | CUDA | Mumax3 | CPU util. | GPU util. | CPU(logical/physical) | GPU count |"
  echo "| ------ | ---- | ---- | ------ | --------- | --------- | -------------------- | --------- |"
  awk -F',' '
    {
      ping = ($4 == "online") ? ":white_check_mark: online" : ":x: offline"
      cuda = ($5 == "ok") ? ":white_check_mark: ok" : (($5 == "error") ? ":x: error" : ":grey_question: unknown")
      mumax = ($6 == "ok") ? ":white_check_mark: ok" : (($6 == "error") ? ":x: error" : ":grey_question: unknown")
      cpu = ($8 == "NA") ? "NA" : $8 "%"
      gpu = ($7 == "NA") ? "NA" : $7 "%"
      cpuc = $9 "/" $10
      printf "| %s | %s | %s | %s | %s | %s | %s | %s |\n", $3, ping, cuda, mumax, cpu, gpu, cpuc, $11
    }
  ' "$cycle_file"
}

generate_readme() {
  local timestamp_utc="$1"
  local timestamp_epoch="$2"
  local cycle_file="$3"
  local timestamp_central_us
  local timestamp_central_eu

  timestamp_central_us=$(TZ=America/Chicago date -d "@$timestamp_epoch" +"%Y-%m-%d %H:%M:%S %Z")
  timestamp_central_eu=$(TZ=Europe/Berlin date -d "@$timestamp_epoch" +"%Y-%m-%d %H:%M:%S %Z")

  {
    echo "# Server Status Dashboard"
    echo
    echo "Updated (Central US): **$timestamp_central_us**"
    echo "Updated (Central EU): **$timestamp_central_eu**"
    echo "Updated (UTC): **$timestamp_utc**"
    echo
    echo "## Current Fleet Status"
    echo
    generate_current_status_table "$cycle_file"
    echo
    echo "## Hardware Inventory (latest known)"
    echo
    generate_hardware_inventory_table
    echo
    echo "## Reliability & Utilization (all samples)"
    echo
    generate_statistics_table
    echo
    echo "## SLO Rollups"
    echo
    generate_slo_table
    echo
    echo "## Incidents & State Changes (latest 25 transitions)"
    echo
    echo "| Timestamp (UTC) | Server | Signal | Transition |"
    echo "| --------------- | ------ | ------ | ---------- |"
    generate_incidents_table
    echo
    echo "## Historical Plots"
    echo
    echo "![Ping uptime plot](plots/ping.svg)"
    echo
    echo "![CUDA health plot](plots/cuda_ok.svg)"
    echo
    echo "![Mumax3 health plot](plots/mumax3_ok.svg)"
    echo
    echo "![CPU utilization plot](plots/cpu_utilization.svg)"
    echo
    echo "![GPU utilization plot](plots/gpu_utilization.svg)"
    echo
    echo "## Recent Samples"
    echo
    echo "<details>"
    echo "<summary>Expand to view the latest 60 samples</summary>"
    echo
    generate_recent_samples
    echo
    echo "</details>"
    echo
    echo "## How checks work"
    echo
    echo "1. **Ping**: ICMP ping from the monitoring host."
    echo "2. **CUDA health**: SSH + \
\`nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits\`; command stderr/failure now marks CUDA as error."
    echo "3. **No mumax3 errors**: SSH + \
\`mumax3 -version\` (fallback to \
\`mumax3 -v\` / \
\`mumax3\`)."
    echo "4. **CPU utilization**: SSH + \
\`top\` (fallback \
\`vmstat\`) parsed as active CPU%."
    echo "5. **Hardware inventory**: SSH + \
\`nproc\`, \
\`lscpu\`, \
\`nvidia-smi\`, and \
\`/proc/meminfo\`."
    echo
    echo "## GitHub-first rendering notes"
    echo
    echo "- README only uses GitHub-supported Markdown tables and static SVG images."
    echo "- Interactive JavaScript charts are intentionally avoided so everything renders directly on GitHub."
  } > "$README_FILE"
}

generate_plots() {
  mkdir -p "$PLOTS_DIR"
  python3 generate_plots.py
}

run_cycle() {
  local timestamp_utc
  local timestamp_epoch
  local cycle_file

  timestamp_utc=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  timestamp_epoch=$(date -u +"%s")
  cycle_file=$(mktemp)

  for host in "${HOSTS[@]}"; do
    collect_server_status "$host" "$timestamp_utc" "$timestamp_epoch" | tee -a "$cycle_file" >> "$CSV_FILE"
  done

  generate_plots
  generate_readme "$timestamp_utc" "$timestamp_epoch" "$cycle_file"
  rm -f "$cycle_file"

  if [[ "${SKIP_GIT:-0}" != "1" ]]; then
    git add "$README_FILE" "$CSV_FILE" "$PLOTS_DIR"/*.svg generate_plots.py dashboard.html
    if ! git diff --cached --quiet; then
      git commit -m "Update server health snapshot: $timestamp_utc"
      git push
    fi
  fi
}

main() {
  init_csv

  if [[ "${1:-}" == "--once" ]]; then
    run_cycle
    exit 0
  fi

  while true; do
    run_cycle
    sleep 60
  done
}

main "$@"
