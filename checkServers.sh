#!/usr/bin/env bash

set -u

HOSTS=("nsc1.utdallas.edu" "nsc2.utdallas.edu" "nsc3.utdallas.edu" "nsc4.utdallas.edu")
CSV_FILE="checkServers.csv"
README_FILE="README.md"
LEGACY_PREFIX="checkServers_legacy"
SSH_OPTS=(-o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=accept-new)

init_csv() {
  if [[ ! -f "$CSV_FILE" || ! -s "$CSV_FILE" ]]; then
    echo "timestamp_utc,timestamp_epoch,server,ping,cuda_ok,mumax3_ok,gpu_utilization" > "$CSV_FILE"
    return
  fi

  local first_line
  first_line=$(head -n 1 "$CSV_FILE")

  if [[ "$first_line" != "timestamp_utc,timestamp_epoch,server,ping,cuda_ok,mumax3_ok,gpu_utilization" ]]; then
    local backup_file
    backup_file="${LEGACY_PREFIX}_$(date -u +%Y%m%dT%H%M%SZ).csv"
    mv "$CSV_FILE" "$backup_file"
    echo "timestamp_utc,timestamp_epoch,server,ping,cuda_ok,mumax3_ok,gpu_utilization" > "$CSV_FILE"
    echo "Migrated legacy CSV format to $backup_file"
  fi
}


collect_server_status() {
  local host="$1"
  local timestamp_utc="$2"
  local timestamp_epoch="$3"

  local ping_status="offline"
  local cuda_status="unknown"
  local mumax_status="unknown"
  local gpu_utilization="NA"

  if ping -c 1 -W 1 "$host" >/dev/null 2>&1; then
    ping_status="online"

    local gpu_raw
    gpu_raw=$(ssh "${SSH_OPTS[@]}" "$host" 'command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits' 2>/dev/null || true)
    if [[ -n "$gpu_raw" ]]; then
      gpu_utilization=$(echo "$gpu_raw" | awk '{sum += $1; count += 1} END {if (count > 0) printf "%.2f", sum / count; else print "NA"}')
      if [[ "$gpu_utilization" != "NA" ]]; then
        cuda_status="ok"
      else
        cuda_status="error"
      fi
    else
      cuda_status="error"
    fi

    if ssh "${SSH_OPTS[@]}" "$host" 'command -v mumax3 >/dev/null 2>&1 && (mumax3 -version >/dev/null 2>&1 || mumax3 -v >/dev/null 2>&1 || mumax3 >/dev/null 2>&1)' >/dev/null 2>&1; then
      mumax_status="ok"
    else
      mumax_status="error"
    fi
  fi

  echo "$timestamp_utc,$timestamp_epoch,$host,$ping_status,$cuda_status,$mumax_status,$gpu_utilization"
}

generate_statistics_table() {
  local ordered_hosts
  ordered_hosts=$(printf "%s," "${HOSTS[@]}")
  ordered_hosts=${ordered_hosts%,}

  awk -F',' -v ordered_hosts="$ordered_hosts" '
    BEGIN {
      split(ordered_hosts, host_list, ",")
    }
    NR == 1 { next }
    {
      server = $3
      total[server] += 1
      if ($4 == "online") ping_ok[server] += 1
      if ($5 == "ok") cuda_ok[server] += 1
      if ($6 == "ok") mumax_ok[server] += 1
      if ($7 ~ /^[0-9]+(\.[0-9]+)?$/) {
        gpu_sum[server] += $7
        gpu_count[server] += 1
      }
      seen[server] = 1
    }
    function print_row(server) {
      ping_pct = (total[server] > 0) ? (100 * ping_ok[server] / total[server]) : 0
      cuda_pct = (total[server] > 0) ? (100 * cuda_ok[server] / total[server]) : 0
      mumax_pct = (total[server] > 0) ? (100 * mumax_ok[server] / total[server]) : 0
      gpu_avg = (gpu_count[server] > 0) ? sprintf("%.2f%%", gpu_sum[server] / gpu_count[server]) : "NA"

      printf "| %s | %d | %.2f%% | %.2f%% | %.2f%% | %s |\n", server, total[server], ping_pct, cuda_pct, mumax_pct, gpu_avg
    }
    END {
      print "| Server | Samples | Ping uptime | CUDA healthy | Mumax3 healthy | Avg GPU util. |"
      print "| ------ | ------- | ----------- | ------------ | -------------- | ------------- |"

      for (idx in host_list) {
        server = host_list[idx]
        if (server in seen) {
          print_row(server)
          printed[server] = 1
        }
      }

      for (server in seen) {
        if (!(server in printed)) {
          print_row(server)
        }
      }
    }
  ' "$CSV_FILE"
}

generate_recent_samples() {
  {
    echo "| Timestamp (UTC) | Server | Ping | CUDA | Mumax3 | GPU util. |"
    echo "| --------------- | ------ | ---- | ---- | ------ | --------- |"
    tail -n 40 "$CSV_FILE" | awk -F',' '
      NR == 1 { next }
      {
        printf "| %s | %s | %s | %s | %s | %s |\n", $1, $3, $4, $5, $6, $7
      }
    '
  }
}

generate_readme() {
  local timestamp_utc="$1"
  local cycle_file="$2"

  {
    echo "# Server Status Dashboard"
    echo
    echo "Updated: \
**$timestamp_utc**"
    echo
    echo "## Latest Check"
    echo
    echo "| Server | Ping | CUDA | Mumax3 | GPU util. |"
    echo "| ------ | ---- | ---- | ------ | --------- |"

    awk -F',' -v OFS=',' '
      {
        ping_emoji = ($4 == "online") ? ":+1:" : ":x:"
        cuda_emoji = ($5 == "ok") ? ":+1:" : (($5 == "error") ? ":x:" : ":grey_question:")
        mumax_emoji = ($6 == "ok") ? ":+1:" : (($6 == "error") ? ":x:" : ":grey_question:")
        gpu_cell = ($7 == "NA") ? "NA" : $7 "%"
        printf "| %s | %s (%s) | %s (%s) | %s (%s) | %s |\n", $3, ping_emoji, $4, cuda_emoji, $5, mumax_emoji, $6, gpu_cell
      }
    ' "$cycle_file"

    echo
    echo "## Historical Reliability (all samples)"
    echo
    generate_statistics_table
    echo
    echo "## Recent Samples"
    echo
    echo "<details>"
    echo "<summary>Expand to view the latest 40 samples</summary>"
    echo
    generate_recent_samples
    echo
    echo "</details>"
    echo
    echo "## How checks work"
    echo
    echo "1. **Ping**: ICMP ping from the external monitoring host."
    echo "2. **No CUDA errors**: SSH to the server and execute \
\`nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits\`."
    echo "3. **No mumax3 errors**: SSH to the server and run \
\`mumax3 -version\` (fallback to \
\`mumax3 -v\` / \
\`mumax3\`)."
    echo "4. **GPU utilization**: Average of all GPUs returned by \
\`nvidia-smi\` during each check."
    echo
    echo "## Suggested next improvements"
    echo
    echo "- Add alerting (email/Slack/webhook) when a category fails for N consecutive checks."
    echo "- Keep a separate \`unknown\` state in alert logic to avoid false alarms during SSH outages."
    echo "- Export CSV data to a time-series DB (Prometheus/InfluxDB) for long-term dashboards."
    echo "- Add per-host configuration (SSH user, GPU thresholds, custom mumax3 command)."
  } > "$README_FILE"
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

  generate_readme "$timestamp_utc" "$cycle_file"
  rm -f "$cycle_file"

  if [[ "${SKIP_GIT:-0}" != "1" ]]; then
    git add "$README_FILE" "$CSV_FILE"
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
