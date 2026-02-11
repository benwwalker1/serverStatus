#!/usr/bin/env bash

set -u

HOSTS=("nsc1.utdallas.edu" "nsc2.utdallas.edu" "nsc3.utdallas.edu" "nsc4.utdallas.edu")
CSV_FILE="checkServers.csv"
README_FILE="README.md"
DASHBOARD_FILE="dashboard.html"
LEGACY_PREFIX="checkServers_legacy"
SSH_OPTS=(-o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=accept-new)

CSV_HEADER="timestamp_utc,timestamp_epoch,server,ping,cuda_ok,mumax3_ok,cpu_count,cpu_utilization,gpu_count,gpu_utilization"

DEBUG_MODE=0
RUN_ONCE=0

usage() {
  cat <<USAGE
Usage: ./checkServers.sh [--once] [--debug]

Options:
  --once   Run exactly one monitoring cycle.
  --debug  Print detailed per-server results each cycle and skip git commit/push.
  --help   Show this help message.
USAGE
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --once) RUN_ONCE=1 ;;
      --debug) DEBUG_MODE=1 ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        echo "Unknown option: $1" >&2
        usage >&2
        exit 1
        ;;
    esac
    shift
  done

  if [[ "$DEBUG_MODE" == "1" ]]; then
    SKIP_GIT=1
  fi
}

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
    echo "Migrated incompatible CSV schema to $backup_file"
  fi
}

collect_server_status() {
  local host="$1"
  local timestamp_utc="$2"
  local timestamp_epoch="$3"

  local ping_status="offline"
  local cuda_status="unknown"
  local mumax_status="unknown"
  local cpu_count="NA"
  local cpu_utilization="NA"
  local gpu_count="NA"
  local gpu_utilization="NA"

  if ping -c 1 -W 1 "$host" >/dev/null 2>&1; then
    ping_status="online"

    cpu_count=$(ssh "${SSH_OPTS[@]}" "$host" 'command -v nproc >/dev/null 2>&1 && nproc || echo NA' 2>/dev/null || echo NA)
    cpu_utilization=$(ssh "${SSH_OPTS[@]}" "$host" '
      read cpu a b c idle rest < /proc/stat
      t1=$((a+b+c+idle))
      i1=$idle
      sleep 0.5
      read cpu a b c idle rest < /proc/stat
      t2=$((a+b+c+idle))
      i2=$idle
      dt=$((t2-t1)); di=$((i2-i1))
      if [ "$dt" -gt 0 ]; then
        awk -v dt="$dt" -v di="$di" "BEGIN {printf \"%.2f\", ((dt-di)/dt)*100}"
      else
        echo NA
      fi
    ' 2>/dev/null || echo NA)

    local gpu_raw
    gpu_raw=$(ssh "${SSH_OPTS[@]}" "$host" 'command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits' 2>/dev/null || true)
    if [[ -n "$gpu_raw" ]]; then
      gpu_count=$(echo "$gpu_raw" | awk 'NF{count+=1} END{if(count>0) print count; else print "NA"}')
      gpu_utilization=$(echo "$gpu_raw" | awk '{sum+=$1; count+=1} END{if(count>0) printf "%.2f", sum/count; else print "NA"}')
      [[ "$gpu_utilization" != "NA" ]] && cuda_status="ok" || cuda_status="error"
    else
      cuda_status="error"
    fi

    if ssh "${SSH_OPTS[@]}" "$host" 'command -v mumax3 >/dev/null 2>&1 && (mumax3 -version >/dev/null 2>&1 || mumax3 -v >/dev/null 2>&1 || mumax3 >/dev/null 2>&1)' >/dev/null 2>&1; then
      mumax_status="ok"
    else
      mumax_status="error"
    fi
  fi

  echo "$timestamp_utc,$timestamp_epoch,$host,$ping_status,$cuda_status,$mumax_status,$cpu_count,$cpu_utilization,$gpu_count,$gpu_utilization"
}

generate_range_uptime_tables() {
  python3 - "$CSV_FILE" <<'PY'
import csv, sys, time
from collections import defaultdict

csv_path=sys.argv[1]
rows=list(csv.DictReader(open(csv_path, newline='')))
if not rows:
    print("No data yet.")
    raise SystemExit

ranges=[("1 day",86400),("1 week",604800),("1 month",2592000),("6 months",15552000)]
now=max(int(r["timestamp_epoch"]) for r in rows)
servers=sorted(set(r["server"] for r in rows))

for label,seconds in ranges:
    cutoff=now-seconds
    filt=[r for r in rows if int(r["timestamp_epoch"])>=cutoff]
    print(f"### {label} uptime")
    print("| Server | Samples | Ping uptime | CUDA healthy | Mumax3 healthy | CPU avg util. | GPU avg util. |")
    print("| ------ | ------- | ----------- | ------------ | -------------- | ------------- | ------------- |")
    grouped=defaultdict(list)
    for r in filt:
      grouped[r['server']].append(r)
    for s in servers:
      g=grouped.get(s,[])
      n=len(g)
      if n==0:
        print(f"| {s} | 0 | NA | NA | NA | NA | NA |")
        continue
      ping=sum(1 for r in g if r['ping']=='online')/n*100
      cuda=sum(1 for r in g if r['cuda_ok']=='ok')/n*100
      mumax=sum(1 for r in g if r['mumax3_ok']=='ok')/n*100
      cpu_vals=[float(r['cpu_utilization']) for r in g if r['cpu_utilization'].replace('.','',1).isdigit()]
      gpu_vals=[float(r['gpu_utilization']) for r in g if r['gpu_utilization'].replace('.','',1).isdigit()]
      cpu_avg=f"{sum(cpu_vals)/len(cpu_vals):.2f}%" if cpu_vals else "NA"
      gpu_avg=f"{sum(gpu_vals)/len(gpu_vals):.2f}%" if gpu_vals else "NA"
      print(f"| {s} | {n} | {ping:.2f}% | {cuda:.2f}% | {mumax:.2f}% | {cpu_avg} | {gpu_avg} |")
    print()
PY
}

generate_recent_samples() {
  {
    echo "| Timestamp (UTC) | Server | Ping | CUDA | Mumax3 | CPU count | CPU util. | GPU count | GPU util. |"
    echo "| --------------- | ------ | ---- | ---- | ------ | --------- | --------- | --------- | --------- |"
    tail -n 60 "$CSV_FILE" | awk -F',' '
      NR == 1 { next }
      {
        cpu_u=($8=="NA")?"NA":$8 "%"
        gpu_u=($10=="NA")?"NA":$10 "%"
        printf "| %s | %s | %s | %s | %s | %s | %s | %s | %s |\n", $1,$3,$4,$5,$6,$7,cpu_u,$9,gpu_u
      }
    '
  }
}

generate_dashboard_html() {
  python3 - "$CSV_FILE" "$DASHBOARD_FILE" <<'PY'
import csv, json, sys
from collections import defaultdict

csv_file, out_file = sys.argv[1], sys.argv[2]
rows=list(csv.DictReader(open(csv_file, newline='')))
servers=sorted({r['server'] for r in rows})

def numeric(v):
    try: return float(v)
    except: return None

data=defaultdict(lambda: defaultdict(list))
for r in rows:
    s=r['server']
    ts=int(r['timestamp_epoch'])*1000
    data[s]['time'].append(ts)
    data[s]['ping'].append(100 if r['ping']=='online' else 0)
    data[s]['cuda'].append(100 if r['cuda_ok']=='ok' else 0)
    data[s]['mumax3'].append(100 if r['mumax3_ok']=='ok' else 0)
    data[s]['cpu_utilization'].append(numeric(r['cpu_utilization']))
    data[s]['gpu_utilization'].append(numeric(r['gpu_utilization']))

html=f'''<!doctype html>
<html><head><meta charset="utf-8"><title>Server Uptime Dashboard</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>body{{font-family:Arial,Helvetica,sans-serif;margin:20px}} #chart{{height:70vh}}</style>
</head><body>
<h1>Server Uptime & Utilization Dashboard</h1>
<p>Interactive ranges: 1 day, 1 week, 1 month, 6 months.</p>
<label>Metric:</label>
<select id="metric">
  <option value="ping">Ping uptime</option>
  <option value="cuda">CUDA health uptime</option>
  <option value="mumax3">Mumax3 health uptime</option>
  <option value="cpu_utilization">CPU utilization</option>
  <option value="gpu_utilization">GPU utilization</option>
</select>
<div id="chart"></div>
<script>
const data={json.dumps(data)};
const servers={json.dumps(servers)};

function traces(metric){{
  return servers.map(s => ({{
    x: data[s].time.map(t => new Date(t)),
    y: data[s][metric],
    mode: 'lines+markers',
    name: s,
    connectgaps: false
  }}));
}}

function draw(metric){{
  const isUptime = ['ping','cuda','mumax3'].includes(metric);
  Plotly.newPlot('chart', traces(metric), {{
    title: metric,
    yaxis: {{title: isUptime ? 'Percent (0/100 per sample)' : 'Percent utilization', range: isUptime ? [0,100] : [0,100]}},
    xaxis: {{
      title: 'Time (UTC)',
      rangeselector: {{buttons: [
        {{count:1,step:'day',stepmode:'backward',label:'1d'}},
        {{count:7,step:'day',stepmode:'backward',label:'1w'}},
        {{count:1,step:'month',stepmode:'backward',label:'1m'}},
        {{count:6,step:'month',stepmode:'backward',label:'6m'}},
        {{step:'all',label:'all'}}
      ]}},
      rangeslider: {{visible:true}},
      type:'date'
    }}
  }}, {{responsive:true}});
}}

draw('ping');
document.getElementById('metric').addEventListener('change', e => draw(e.target.value));
</script>
</body></html>'''

open(out_file,'w').write(html)
PY
}

generate_readme() {
  local timestamp_utc="$1"
  local cycle_file="$2"

  {
    echo "# Server Status Dashboard"
    echo
    echo "Updated: **$timestamp_utc**"
    echo
    echo "Interactive dashboard: [dashboard.html](./dashboard.html)"
    echo
    echo "## Latest Check"
    echo
    echo "| Server | Ping | CUDA | Mumax3 | CPU count | CPU util. | GPU count | GPU util. |"
    echo "| ------ | ---- | ---- | ------ | --------- | --------- | --------- | --------- |"

    awk -F',' '
      {
        ping_emoji = ($4 == "online") ? ":+1:" : ":x:"
        cuda_emoji = ($5 == "ok") ? ":+1:" : (($5 == "error") ? ":x:" : ":grey_question:")
        mumax_emoji = ($6 == "ok") ? ":+1:" : (($6 == "error") ? ":x:" : ":grey_question:")
        cpu_u = ($8 == "NA") ? "NA" : $8 "%"
        gpu_u = ($10 == "NA") ? "NA" : $10 "%"
        printf "| %s | %s (%s) | %s (%s) | %s (%s) | %s | %s | %s | %s |\n", $3, ping_emoji, $4, cuda_emoji, $5, mumax_emoji, $6, $7, cpu_u, $9, gpu_u
      }
    ' "$cycle_file"

    echo
    echo "## Uptime over time windows"
    echo
    generate_range_uptime_tables

    echo "## Recent Samples"
    echo
    echo "<details>"
    echo "<summary>Expand to view latest 60 samples</summary>"
    echo
    generate_recent_samples
    echo
    echo "</details>"
    echo
    echo "## Definitions"
    echo
    echo "- **Ping uptime**: percentage of samples in which ICMP ping succeeded."
    echo "- **CUDA healthy uptime**: percentage of samples in which \`nvidia-smi\` returned valid GPU utilization data."
    echo "- **Mumax3 healthy uptime**: percentage of samples in which \`mumax3\` command check succeeded."
    echo "- **CPU utilization**: average active CPU percentage computed from \`/proc/stat\` over ~0.5s during each sample."
    echo "- **GPU utilization**: mean \`%utilization.gpu\` across all GPUs reported by \`nvidia-smi\` at sample time."
    echo "- **CPU/GPU counts**: \`nproc\` for CPU logical cores, and number of GPUs returned by \`nvidia-smi\`."
  } > "$README_FILE"
}

print_debug_cycle() {
  local timestamp_utc="$1"
  local cycle_file="$2"
  echo "[debug] Cycle timestamp: $timestamp_utc"
  awk -F',' '
    {
      cpu_u=($8=="NA")?"NA":$8 "%"
      gpu_u=($10=="NA")?"NA":$10 "%"
      printf "  - %s | ping=%s | cuda=%s | mumax3=%s | cpu_count=%s | cpu_util=%s | gpu_count=%s | gpu_util=%s\n", $3,$4,$5,$6,$7,cpu_u,$9,gpu_u
    }
  ' "$cycle_file"
}

run_cycle() {
  local timestamp_utc timestamp_epoch cycle_file
  timestamp_utc=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  timestamp_epoch=$(date -u +"%s")
  cycle_file=$(mktemp)

  for host in "${HOSTS[@]}"; do
    collect_server_status "$host" "$timestamp_utc" "$timestamp_epoch" | tee -a "$cycle_file" >> "$CSV_FILE"
  done

  [[ "$DEBUG_MODE" == "1" ]] && print_debug_cycle "$timestamp_utc" "$cycle_file"

  generate_readme "$timestamp_utc" "$cycle_file"
  generate_dashboard_html
  rm -f "$cycle_file"

  if [[ "${SKIP_GIT:-0}" != "1" ]]; then
    git add "$README_FILE" "$CSV_FILE" "$DASHBOARD_FILE"
    if ! git diff --cached --quiet; then
      git commit -m "Update server health snapshot: $timestamp_utc"
      git push
    fi
  elif [[ "$DEBUG_MODE" == "1" ]]; then
    echo "[debug] SKIP_GIT=1 active; skipping git commit/push"
  fi
}

main() {
  parse_args "$@"
  init_csv

  if [[ "$RUN_ONCE" == "1" ]]; then
    run_cycle
    exit 0
  fi

  while true; do
    run_cycle
    sleep 60
  done
}

main "$@"
