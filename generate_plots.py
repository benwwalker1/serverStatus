#!/usr/bin/env python3
import csv
import datetime as dt
import math
import os
from collections import defaultdict

CSV_FILE = "checkServers.csv"
PLOTS_DIR = "plots"

METRICS = [
    ("ping", "Ping Uptime (%)", "#1f77b4"),
    ("cuda_ok", "CUDA Health (%)", "#ff7f0e"),
    ("mumax3_ok", "Mumax3 Health (%)", "#2ca02c"),
    ("cpu_utilization", "CPU Utilization (%)", "#d62728"),
    ("gpu_utilization", "GPU Utilization (%)", "#9467bd"),
]


def parse_float(value):
    if value in (None, "", "NA", "unknown"):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def load_rows(path):
    rows = []
    if not os.path.exists(path):
        return rows

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                ts = int(row.get("timestamp_epoch", "0")) * 1000
            except ValueError:
                continue
            rows.append(
                {
                    "ts": ts,
                    "server": row.get("server", "unknown"),
                    "ping": 100.0 if row.get("ping") == "online" else 0.0,
                    "cuda_ok": 100.0 if row.get("cuda_ok") == "ok" else 0.0,
                    "mumax3_ok": 100.0 if row.get("mumax3_ok") == "ok" else 0.0,
                    "cpu_utilization": parse_float(row.get("cpu_utilization")),
                    "gpu_utilization": parse_float(row.get("gpu_utilization")),
                }
            )
    rows.sort(key=lambda r: (r["ts"], r["server"]))
    return rows


def esc(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def time_label(ts_ms):
    return dt.datetime.utcfromtimestamp(ts_ms / 1000).strftime("%Y-%m-%d %H:%M")


def build_chart(rows, metric_key, title, color):
    width, height = 1200, 360
    m_left, m_top, m_right, m_bottom = 70, 35, 20, 55
    inner_w = width - m_left - m_right
    inner_h = height - m_top - m_bottom

    server_points = defaultdict(list)
    for row in rows:
        y = row[metric_key]
        if y is None:
            continue
        server_points[row["server"]].append((row["ts"], y))

    all_points = [p for points in server_points.values() for p in points]

    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{width/2}" y="22" text-anchor="middle" font-size="16" font-family="Arial, Helvetica, sans-serif" font-weight="bold">{esc(title)}</text>',
    ]

    if not all_points:
        svg.append(f'<text x="{width/2}" y="{height/2}" text-anchor="middle" font-size="14" font-family="Arial, Helvetica, sans-serif">No data available.</text>')
        svg.append("</svg>")
        return "\n".join(svg)

    min_ts = min(p[0] for p in all_points)
    max_ts = max(p[0] for p in all_points)
    if min_ts == max_ts:
        max_ts += 1

    def sx(ts):
        return m_left + ((ts - min_ts) / (max_ts - min_ts)) * inner_w

    def sy(y):
        return m_top + (1 - (max(0.0, min(100.0, y)) / 100.0)) * inner_h

    for i in range(6):
        yv = 100 - i * 20
        y = sy(yv)
        svg.append(f'<line x1="{m_left}" y1="{y:.2f}" x2="{width-m_right}" y2="{y:.2f}" stroke="#e3e3e3" stroke-width="1"/>')
        svg.append(f'<text x="{m_left-8}" y="{y+4:.2f}" text-anchor="end" font-size="11" fill="#444" font-family="Arial, Helvetica, sans-serif">{yv}</text>')

    svg.append(f'<line x1="{m_left}" y1="{m_top}" x2="{m_left}" y2="{height-m_bottom}" stroke="#999"/>')
    svg.append(f'<line x1="{m_left}" y1="{height-m_bottom}" x2="{width-m_right}" y2="{height-m_bottom}" stroke="#999"/>')

    for i in range(5):
        ts = int(min_ts + (max_ts - min_ts) * (i / 4))
        x = sx(ts)
        lbl = time_label(ts)
        svg.append(f'<text x="{x:.2f}" y="{height-m_bottom+18}" text-anchor="middle" font-size="10" fill="#444" font-family="Arial, Helvetica, sans-serif">{esc(lbl)}</text>')

    servers = sorted(server_points.keys())
    for idx, server in enumerate(servers):
        pts = server_points[server]
        if len(pts) < 2:
            ts, y = pts[0]
            svg.append(f'<circle cx="{sx(ts):.2f}" cy="{sy(y):.2f}" r="3" fill="{color}"/>')
            continue
        path = " ".join(f"{sx(ts):.2f},{sy(y):.2f}" for ts, y in pts)
        op = 0.95 - idx * 0.15
        svg.append(f'<polyline fill="none" stroke="{color}" stroke-opacity="{max(0.3, op):.2f}" stroke-width="2" points="{path}"/>')

    legend_x = m_left
    legend_y = height - 18
    servers = sorted(server_points.keys())
    for idx, server in enumerate(servers):
        op = 0.95 - idx * 0.15
        x = legend_x + idx * 280
        svg.append(f'<rect x="{x}" y="{legend_y-10}" width="12" height="12" fill="{color}" fill-opacity="{max(0.3, op):.2f}"/>')
        svg.append(f'<text x="{x+18}" y="{legend_y}" font-size="11" fill="#333" font-family="Arial, Helvetica, sans-serif">{esc(server)}</text>')

    svg.append("</svg>")
    return "\n".join(svg)


def main():
    os.makedirs(PLOTS_DIR, exist_ok=True)
    rows = load_rows(CSV_FILE)
    for key, title, color in METRICS:
        svg = build_chart(rows, key, title, color)
        with open(os.path.join(PLOTS_DIR, f"{key}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)


if __name__ == "__main__":
    main()
