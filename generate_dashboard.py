#!/usr/bin/env python3
"""Read per-server JSON files from data/live/, append to CSV history, generate HTML dashboard."""

import csv
import json
import os
import glob
from datetime import datetime, timezone
from collections import defaultdict

LIVE_DIR = "data/live"
CSV_FILE = "data/status.csv"
OUT_FILE = "index.html"
SERVERS = ["nsc1", "nsc2", "nsc3", "nsc4"]
# If a server hasn't reported in this many seconds, consider it offline
STALE_THRESHOLD = 600  # 10 minutes

CSV_HEADER = [
    "timestamp_utc", "timestamp_epoch", "server", "online",
    "cuda_ok", "mumax3_ok", "gpu_util_pct", "cpu_util_pct",
    "ram_free_gb", "ram_total_gb", "gpu_count", "gpu_free_count", "gpu_names",
]

def ensure_csv():
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            csv.writer(f).writerow(CSV_HEADER)

def load_live():
    """Load latest JSON report from each server."""
    live = {}
    for path in glob.glob(os.path.join(LIVE_DIR, "*.json")):
        try:
            with open(path) as f:
                data = json.load(f)
            live[data["server"]] = data
        except (json.JSONDecodeError, KeyError):
            continue
    return live

def load_csv():
    rows = []
    if not os.path.exists(CSV_FILE):
        return rows
    with open(CSV_FILE, newline="") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows

def last_csv_epoch(rows, server):
    """Find the most recent epoch in CSV for a given server."""
    for r in reversed(rows):
        if r["server"] == server:
            return int(r["timestamp_epoch"])
    return 0

def append_new_reports(live, existing_rows):
    """Append live reports to CSV if they're newer than the last entry."""
    new_rows = []
    for srv_name, data in live.items():
        epoch = int(data["timestamp_epoch"])
        if epoch <= last_csv_epoch(existing_rows, srv_name):
            continue  # Already recorded
        row = {
            "timestamp_utc": data["timestamp_utc"],
            "timestamp_epoch": str(epoch),
            "server": srv_name,
            "online": "1",  # It reported in, so it's online
            "cuda_ok": str(data.get("cuda_ok", 0)),
            "mumax3_ok": str(data.get("mumax3_ok", 0)),
            "gpu_util_pct": str(data.get("gpu_util_pct", "NA")) if data.get("gpu_util_pct") is not None else "NA",
            "cpu_util_pct": str(data.get("cpu_util_pct", "NA")) if data.get("cpu_util_pct") is not None else "NA",
            "ram_free_gb": str(data.get("ram_free_gb", "NA")) if data.get("ram_free_gb") is not None else "NA",
            "ram_total_gb": str(data.get("ram_total_gb", "NA")) if data.get("ram_total_gb") is not None else "NA",
            "gpu_count": str(data.get("gpu_count", "NA")) if data.get("gpu_count") is not None else "NA",
            "gpu_free_count": str(data.get("gpu_free_count", "NA")) if data.get("gpu_free_count") is not None else "NA",
            "gpu_names": str(data.get("gpu_names", "NA")) if data.get("gpu_names") is not None else "NA",
        }
        new_rows.append(row)
    if new_rows:
        with open(CSV_FILE, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CSV_HEADER)
            for row in new_rows:
                w.writerow(row)
        print(f"Appended {len(new_rows)} new row(s) to CSV")
    return new_rows

# --- HTML helpers ---

def pct(num, den):
    if den == 0: return "N/A"
    return f"{100 * num / den:.1f}%"

def status_dot(val, ok_val="1"):
    return '<span class="dot green"></span>' if val == ok_val else '<span class="dot red"></span>'

def val_or_na(val):
    if val is None or val == "NA" or val == "null" or val == "None" or val == "":
        return "N/A"
    return str(val)

def sparkline_svg(data, width=120, height=20):
    if not data:
        return '<span class="na">N/A</span>'
    n = len(data)
    bar_w = max(width / n, 2)
    rects = []
    for i, v in enumerate(data):
        color = "#22c55e" if v else "#ef4444"
        x = i * bar_w
        rects.append(f'<rect x="{x:.1f}" y="0" width="{bar_w:.1f}" height="{height}" fill="{color}" />')
    return f'<svg width="{width}" height="{height}" class="sparkline">{"".join(rects)}</svg>'

def get_sparkline(rows, server, field, ok_val="1", max_points=48):
    server_rows = [r for r in rows if r["server"] == server][-max_points:]
    data = [1 if r[field] == ok_val else 0 for r in server_rows]
    return sparkline_svg(data)

def uptime_stats(rows, window_hours=None):
    now_epoch = int(datetime.now(timezone.utc).timestamp())
    stats = defaultdict(lambda: {"total": 0, "online": 0, "cuda": 0, "mumax": 0})
    for r in rows:
        epoch = int(r["timestamp_epoch"])
        if window_hours and (now_epoch - epoch) > window_hours * 3600:
            continue
        srv = r["server"]
        stats[srv]["total"] += 1
        if r["online"] == "1": stats[srv]["online"] += 1
        if r["cuda_ok"] == "1": stats[srv]["cuda"] += 1
        if r["mumax3_ok"] == "1": stats[srv]["mumax"] += 1
    return stats

def history_rows_html(rows, limit=80):
    recent = list(reversed(rows[-limit:]))
    lines = []
    for r in recent:
        lines.append(f"""<tr>
            <td>{r['timestamp_utc']}</td>
            <td>{r['server']}</td>
            <td>{status_dot(r['online'])}</td>
            <td>{status_dot(r['cuda_ok'])}</td>
            <td>{status_dot(r['mumax3_ok'])}</td>
            <td>{val_or_na(r['gpu_util_pct'])}</td>
            <td>{val_or_na(r['cpu_util_pct'])}</td>
            <td>{val_or_na(r['ram_free_gb'])}/{val_or_na(r['ram_total_gb'])}</td>
            <td>{val_or_na(r['gpu_free_count'])}/{val_or_na(r['gpu_count'])}</td>
        </tr>""")
    return "\n".join(lines)

def incident_rows_html(rows, limit=30):
    prev = {}
    incidents = []
    for r in rows:
        srv = r["server"]
        checks = {"Online": r["online"], "CUDA": r["cuda_ok"], "Mumax3": r["mumax3_ok"]}
        if srv in prev:
            for name, val in checks.items():
                if prev[srv][name] != val:
                    direction = "up" if val == "1" else "down"
                    incidents.append((r["timestamp_utc"], srv, name, direction))
        prev[srv] = checks
    incidents = incidents[-limit:]
    incidents.reverse()
    lines = []
    for ts, srv, check, direction in incidents:
        arrow = '<span class="dot green"></span> recovered' if direction == "up" else '<span class="dot red"></span> down'
        lines.append(f"<tr><td>{ts}</td><td>{srv}</td><td>{check}</td><td>{arrow}</td></tr>")
    return "\n".join(lines)

def generate_html(live, rows):
    now_epoch = int(datetime.now(timezone.utc).timestamp())
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if not rows and not live:
        server_cards = '<p style="color:var(--text-dim)">No data collected yet. Waiting for first server report...</p>'
        history_table = ""
        incident_table = ""
    else:
        cards = []
        for srv in SERVERS:
            data = live.get(srv)
            # Determine if online: reported within threshold
            if data:
                age = now_epoch - int(data["timestamp_epoch"])
                is_online = age < STALE_THRESHOLD
            else:
                is_online = False
                age = None

            card_class = "card up" if is_online else "card down"
            badge = '<span class="badge badge-up">ONLINE</span>' if is_online else '<span class="badge badge-down">OFFLINE</span>'

            if data and is_online:
                cuda_ok = str(data.get("cuda_ok", 0))
                mumax_ok = str(data.get("mumax3_ok", 0))
                gpu_util = val_or_na(data.get("gpu_util_pct"))
                if gpu_util != "N/A": gpu_util += "%"
                cpu_util = val_or_na(data.get("cpu_util_pct"))
                if cpu_util != "N/A": cpu_util += "%"
                ram_f = val_or_na(data.get("ram_free_gb"))
                ram_t = val_or_na(data.get("ram_total_gb"))
                ram_str = f"{ram_f} / {ram_t} GB" if ram_f != "N/A" and ram_t != "N/A" else "N/A"
                gpu_f = val_or_na(data.get("gpu_free_count"))
                gpu_c = val_or_na(data.get("gpu_count"))
                gpu_str = f"{gpu_f} / {gpu_c} free" if gpu_f != "N/A" and gpu_c != "N/A" else "N/A"
                gpu_names = val_or_na(data.get("gpu_names")).replace(";", ", ")
                last_seen = data["timestamp_utc"]
            else:
                cuda_ok = "0"
                mumax_ok = "0"
                gpu_util = cpu_util = ram_str = gpu_str = "N/A"
                gpu_names = "N/A"
                # Find last seen from CSV
                srv_rows = [r for r in rows if r["server"] == srv and r["online"] == "1"]
                last_seen = srv_rows[-1]["timestamp_utc"] if srv_rows else "Never"

            online_spark = get_sparkline(rows, srv, "online")
            cuda_spark = get_sparkline(rows, srv, "cuda_ok")
            mumax_spark = get_sparkline(rows, srv, "mumax3_ok")

            s24 = uptime_stats(rows, 24)
            s7d = uptime_stats(rows, 168)
            up_24 = pct(s24[srv]["online"], s24[srv]["total"])
            up_7d = pct(s7d[srv]["online"], s7d[srv]["total"])

            age_str = ""
            if age is not None:
                if age < 60:
                    age_str = f"{age}s ago"
                elif age < 3600:
                    age_str = f"{age // 60}m ago"
                elif age < 86400:
                    age_str = f"{age // 3600}h ago"
                else:
                    age_str = f"{age // 86400}d ago"

            cards.append(f"""
            <div class="{card_class}">
                <div class="card-header">
                    <h2>{srv}</h2>
                    {badge}
                </div>
                <div class="card-body">
                    <div class="last-seen">Last report: {last_seen} <span class="age">({age_str})</span></div>
                    <table class="checks">
                        <tr><td>Online</td><td>{status_dot("1" if is_online else "0")}</td><td>{online_spark}</td></tr>
                        <tr><td>CUDA</td><td>{status_dot(cuda_ok)}</td><td>{cuda_spark}</td></tr>
                        <tr><td>Mumax3</td><td>{status_dot(mumax_ok)}</td><td>{mumax_spark}</td></tr>
                    </table>
                    <div class="metrics">
                        <div class="metric"><span class="label">CPU</span><span class="value">{cpu_util}</span></div>
                        <div class="metric"><span class="label">GPU Util</span><span class="value">{gpu_util}</span></div>
                        <div class="metric"><span class="label">RAM Free</span><span class="value">{ram_str}</span></div>
                        <div class="metric"><span class="label">GPUs</span><span class="value">{gpu_str}</span></div>
                    </div>
                    <div class="hw-info">{gpu_names}</div>
                    <div class="slo">
                        <span>24h uptime: <b>{up_24}</b></span>
                        <span>7d uptime: <b>{up_7d}</b></span>
                    </div>
                </div>
            </div>""")
        server_cards = "\n".join(cards)
        history_table = history_rows_html(rows)
        incident_table = incident_rows_html(rows)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lab Server Status</title>
<style>
:root {{
    --bg: #0f172a;
    --surface: #1e293b;
    --border: #334155;
    --text: #e2e8f0;
    --text-dim: #94a3b8;
    --green: #22c55e;
    --red: #ef4444;
    --yellow: #eab308;
    --blue: #3b82f6;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 24px 16px; }}
header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 8px; }}
header h1 {{ font-size: 1.5rem; font-weight: 700; }}
.updated {{ color: var(--text-dim); font-size: 0.85rem; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-bottom: 32px; }}
.card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 16px; transition: border-color 0.2s; }}
.card.up {{ border-left: 3px solid var(--green); }}
.card.down {{ border-left: 3px solid var(--red); }}
.card-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
.card-header h2 {{ font-size: 1.2rem; font-weight: 600; }}
.badge {{ font-size: 0.7rem; font-weight: 700; padding: 3px 10px; border-radius: 999px; text-transform: uppercase; letter-spacing: 0.05em; }}
.badge-up {{ background: rgba(34,197,94,0.15); color: var(--green); }}
.badge-down {{ background: rgba(239,68,68,0.15); color: var(--red); }}
.last-seen {{ font-size: 0.75rem; color: var(--text-dim); margin-bottom: 10px; }}
.age {{ opacity: 0.7; }}
.checks {{ width: 100%; margin-bottom: 12px; }}
.checks td {{ padding: 3px 0; font-size: 0.85rem; }}
.checks td:first-child {{ color: var(--text-dim); width: 60px; }}
.checks td:nth-child(2) {{ width: 24px; text-align: center; }}
.dot {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; }}
.dot.green {{ background: var(--green); box-shadow: 0 0 6px rgba(34,197,94,0.4); }}
.dot.red {{ background: var(--red); box-shadow: 0 0 6px rgba(239,68,68,0.4); }}
.sparkline {{ vertical-align: middle; border-radius: 3px; overflow: hidden; }}
.metrics {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 10px; }}
.metric {{ background: rgba(255,255,255,0.03); border-radius: 8px; padding: 8px; text-align: center; }}
.metric .label {{ display: block; font-size: 0.7rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px; }}
.metric .value {{ display: block; font-size: 1rem; font-weight: 600; }}
.hw-info {{ font-size: 0.75rem; color: var(--text-dim); margin-bottom: 8px; text-align: center; }}
.slo {{ display: flex; justify-content: space-around; font-size: 0.8rem; color: var(--text-dim); padding-top: 8px; border-top: 1px solid var(--border); }}
.na {{ color: var(--text-dim); }}
section {{ margin-bottom: 32px; }}
section h2 {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }}
table.data {{ width: 100%; border-collapse: collapse; font-size: 0.8rem; }}
table.data th {{ text-align: left; padding: 8px 6px; color: var(--text-dim); font-weight: 500; border-bottom: 1px solid var(--border); position: sticky; top: 0; background: var(--surface); }}
table.data td {{ padding: 6px; border-bottom: 1px solid rgba(51,65,85,0.5); }}
.table-wrap {{ background: var(--surface); border-radius: 12px; padding: 16px; overflow-x: auto; max-height: 500px; overflow-y: auto; }}
details summary {{ cursor: pointer; color: var(--blue); font-size: 0.9rem; margin-bottom: 8px; }}
details summary:hover {{ text-decoration: underline; }}
footer {{ text-align: center; color: var(--text-dim); font-size: 0.75rem; padding: 24px 0; }}
@media (max-width: 600px) {{
    .grid {{ grid-template-columns: 1fr; }}
    .metrics {{ grid-template-columns: 1fr 1fr; }}
}}
</style>
</head>
<body>
<div class="container">
    <header>
        <h1>Lab Server Status</h1>
        <span class="updated">Dashboard built: {updated}</span>
    </header>

    <div class="grid">
        {server_cards}
    </div>

    <section>
        <h2>Incidents</h2>
        <div class="table-wrap">
            <table class="data">
                <thead><tr><th>Time (UTC)</th><th>Server</th><th>Check</th><th>Status</th></tr></thead>
                <tbody>{incident_table}</tbody>
            </table>
            {('<p style="color:var(--text-dim);padding:12px;">No incidents recorded yet.</p>' if not incident_table else '')}
        </div>
    </section>

    <section>
        <h2>History</h2>
        <details>
            <summary>Show last 80 checks</summary>
            <div class="table-wrap">
                <table class="data">
                    <thead><tr>
                        <th>Time</th><th>Server</th><th>Online</th><th>CUDA</th><th>Mumax3</th>
                        <th>GPU %</th><th>CPU %</th><th>RAM (free/total)</th><th>GPUs (free/total)</th>
                    </tr></thead>
                    <tbody>{history_table}</tbody>
                </table>
            </div>
        </details>
    </section>

    <footer>
        Servers self-report every 5 min &middot; Dashboard rebuilt by GitHub Actions &middot; <a href="data/status.csv" style="color:var(--blue)">Historical CSV</a>
    </footer>
</div>
</body>
</html>"""
    with open(OUT_FILE, "w") as f:
        f.write(html)
    print(f"Dashboard written to {OUT_FILE}")

if __name__ == "__main__":
    ensure_csv()
    live = load_live()
    existing_rows = load_csv()
    append_new_reports(live, existing_rows)
    all_rows = load_csv()  # Reload with new data
    generate_html(live, all_rows)
