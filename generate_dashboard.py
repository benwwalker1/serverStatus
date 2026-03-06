#!/usr/bin/env python3
"""Generate a static HTML dashboard from data/status.csv."""

import csv
import os
from datetime import datetime, timezone, timedelta
from collections import defaultdict

CSV_FILE = "data/status.csv"
OUT_FILE = "index.html"

def load_data():
    rows = []
    if not os.path.exists(CSV_FILE):
        return rows
    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows

def latest_per_server(rows):
    """Return dict of server -> most recent row."""
    latest = {}
    for r in rows:
        srv = r["server"]
        if srv not in latest or int(r["timestamp_epoch"]) > int(latest[srv]["timestamp_epoch"]):
            latest[srv] = r
    return latest

def uptime_stats(rows, window_hours=None):
    """Compute per-server uptime stats, optionally within a time window."""
    now_epoch = int(datetime.now(timezone.utc).timestamp())
    stats = defaultdict(lambda: {"total": 0, "ping": 0, "ssh": 0, "cuda": 0, "mumax": 0})
    for r in rows:
        epoch = int(r["timestamp_epoch"])
        if window_hours and (now_epoch - epoch) > window_hours * 3600:
            continue
        srv = r["server"]
        stats[srv]["total"] += 1
        if r["ping"] == "1": stats[srv]["ping"] += 1
        if r["ssh"] == "1": stats[srv]["ssh"] += 1
        if r["cuda_ok"] == "1": stats[srv]["cuda"] += 1
        if r["mumax3_ok"] == "1": stats[srv]["mumax"] += 1
    return stats

def pct(num, den):
    if den == 0: return "N/A"
    return f"{100 * num / den:.1f}%"

def status_dot(val, ok_val="1"):
    if val == ok_val:
        return '<span class="dot green"></span>'
    return '<span class="dot red"></span>'

def val_or_na(val):
    if not val or val == "NA":
        return "N/A"
    return val

def history_rows_html(rows, limit=80):
    """Last N rows as HTML table rows, newest first."""
    recent = rows[-limit:]
    recent.reverse()
    lines = []
    for r in recent:
        lines.append(f"""<tr>
            <td>{r['timestamp_utc']}</td>
            <td>{r['server'].split('.')[0]}</td>
            <td>{status_dot(r['ping'])}</td>
            <td>{status_dot(r['ssh'])}</td>
            <td>{status_dot(r['cuda_ok'])}</td>
            <td>{status_dot(r['mumax3_ok'])}</td>
            <td>{val_or_na(r['gpu_util_pct'])}</td>
            <td>{val_or_na(r['cpu_util_pct'])}</td>
            <td>{val_or_na(r['ram_free_gb'])}/{val_or_na(r['ram_total_gb'])}</td>
            <td>{val_or_na(r['gpu_free_count'])}/{val_or_na(r['gpu_count'])}</td>
        </tr>""")
    return "\n".join(lines)

def incident_rows_html(rows, limit=30):
    """Detect state transitions in ping/ssh/cuda/mumax."""
    prev = {}
    incidents = []
    for r in rows:
        srv = r["server"]
        checks = {"Ping": r["ping"], "SSH": r["ssh"], "CUDA": r["cuda_ok"], "Mumax3": r["mumax3_ok"]}
        if srv in prev:
            for name, val in checks.items():
                if prev[srv][name] != val:
                    direction = "up" if val == "1" else "down"
                    incidents.append((r["timestamp_utc"], srv.split('.')[0], name, direction))
        prev[srv] = checks
    incidents = incidents[-limit:]
    incidents.reverse()
    lines = []
    for ts, srv, check, direction in incidents:
        arrow = '<span class="dot green"></span> recovered' if direction == "up" else '<span class="dot red"></span> down'
        lines.append(f"<tr><td>{ts}</td><td>{srv}</td><td>{check}</td><td>{arrow}</td></tr>")
    return "\n".join(lines)

def generate_sparkline_data(rows, server, field, ok_val="1", max_points=48):
    """Get last N data points for a server as 1/0 array."""
    server_rows = [r for r in rows if r["server"] == server][-max_points:]
    return [1 if r[field] == ok_val else 0 for r in server_rows]

def sparkline_svg(data, width=120, height=20):
    """Tiny inline SVG sparkline of 1/0 values."""
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

def generate_html(rows):
    if not rows:
        updated = "No data yet"
        server_cards = '<p>No data collected yet. Waiting for first check...</p>'
        history_table = ""
        incident_table = ""
    else:
        latest = latest_per_server(rows)
        updated = rows[-1]["timestamp_utc"]
        stats_24h = uptime_stats(rows, 24)
        stats_7d = uptime_stats(rows, 168)
        stats_all = uptime_stats(rows)

        server_order = ["nsc1.utdallas.edu", "nsc2.utdallas.edu", "nsc3.utdallas.edu", "nsc4.utdallas.edu"]
        cards = []
        for srv in server_order:
            if srv not in latest:
                continue
            r = latest[srv]
            short = srv.split('.')[0]
            is_up = r["ping"] == "1" and r["ssh"] == "1"
            card_class = "card up" if is_up else "card down"

            gpu_util = val_or_na(r["gpu_util_pct"])
            if gpu_util != "N/A": gpu_util += "%"
            cpu_util = val_or_na(r["cpu_util_pct"])
            if cpu_util != "N/A": cpu_util += "%"
            ram_free = val_or_na(r["ram_free_gb"])
            ram_total = val_or_na(r["ram_total_gb"])
            if ram_free != "N/A" and ram_total != "N/A":
                ram_str = f"{ram_free} / {ram_total} GB"
            else:
                ram_str = "N/A"
            gpu_free = val_or_na(r["gpu_free_count"])
            gpu_total = val_or_na(r["gpu_count"])
            if gpu_free != "N/A" and gpu_total != "N/A":
                gpu_str = f"{gpu_free} / {gpu_total} free"
            else:
                gpu_str = "N/A"
            gpu_names = val_or_na(r["gpu_names"]).replace(";", ", ")

            # Sparklines for last 48 checks
            ping_spark = sparkline_svg(generate_sparkline_data(rows, srv, "ping"))
            ssh_spark = sparkline_svg(generate_sparkline_data(rows, srv, "ssh"))
            cuda_spark = sparkline_svg(generate_sparkline_data(rows, srv, "cuda_ok"))
            mumax_spark = sparkline_svg(generate_sparkline_data(rows, srv, "mumax3_ok"))

            # SLO badges
            s24 = stats_24h[srv]
            s7d = stats_7d[srv]
            ping_24 = pct(s24["ping"], s24["total"])
            ping_7d = pct(s7d["ping"], s7d["total"])

            cards.append(f"""
            <div class="{card_class}">
                <div class="card-header">
                    <h2>{short}</h2>
                    <span class="badge {"badge-up" if is_up else "badge-down"}">{"UP" if is_up else "DOWN"}</span>
                </div>
                <div class="card-body">
                    <table class="checks">
                        <tr><td>Ping</td><td>{status_dot(r['ping'])}</td><td>{ping_spark}</td></tr>
                        <tr><td>SSH</td><td>{status_dot(r['ssh'])}</td><td>{ssh_spark}</td></tr>
                        <tr><td>CUDA</td><td>{status_dot(r['cuda_ok'])}</td><td>{cuda_spark}</td></tr>
                        <tr><td>Mumax3</td><td>{status_dot(r['mumax3_ok'])}</td><td>{mumax_spark}</td></tr>
                    </table>
                    <div class="metrics">
                        <div class="metric"><span class="label">CPU</span><span class="value">{cpu_util}</span></div>
                        <div class="metric"><span class="label">GPU Util</span><span class="value">{gpu_util}</span></div>
                        <div class="metric"><span class="label">RAM Free</span><span class="value">{ram_str}</span></div>
                        <div class="metric"><span class="label">GPUs</span><span class="value">{gpu_str}</span></div>
                    </div>
                    <div class="hw-info">{gpu_names}</div>
                    <div class="slo">
                        <span>24h ping: <b>{ping_24}</b></span>
                        <span>7d ping: <b>{ping_7d}</b></span>
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
        <span class="updated">Updated: {updated}</span>
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
                        <th>Time</th><th>Server</th><th>Ping</th><th>SSH</th><th>CUDA</th><th>Mumax3</th>
                        <th>GPU %</th><th>CPU %</th><th>RAM (free/total)</th><th>GPUs (free/total)</th>
                    </tr></thead>
                    <tbody>{history_table}</tbody>
                </table>
            </div>
        </details>
    </section>

    <footer>
        Checked every 30 minutes via GitHub Actions &middot; Data stored in <a href="data/status.csv" style="color:var(--blue)">status.csv</a>
    </footer>
</div>
</body>
</html>"""
    with open(OUT_FILE, "w") as f:
        f.write(html)
    print(f"Dashboard written to {OUT_FILE} ({len(rows)} total samples)")

if __name__ == "__main__":
    rows = load_data()
    generate_html(rows)
