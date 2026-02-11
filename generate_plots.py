#!/usr/bin/env python3
import csv
import datetime as dt
import os
from collections import defaultdict

CSV_FILE = "checkServers.csv"
PLOTS_DIR = "plots"

METRICS = [
    ("ping", "Ping Uptime (%)"),
    ("cuda_ok", "CUDA Health (%)"),
    ("mumax3_ok", "Mumax3 Health (%)"),
    ("cpu_utilization", "CPU Utilization (%)"),
    ("gpu_utilization", "GPU Utilization (%)"),
]

PALETTE = [
    "#2563eb",
    "#f59e0b",
    "#16a34a",
    "#dc2626",
    "#7c3aed",
    "#0891b2",
    "#db2777",
    "#4b5563",
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
    return dt.datetime.utcfromtimestamp(ts_ms / 1000).strftime("%m-%d %H:%M")


def build_chart(rows, metric_key, title):
    width, height = 1200, 400
    m_left, m_top, m_right, m_bottom = 72, 40, 24, 75
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
        "<defs>",
        '<linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">',
        '<stop offset="0%" stop-color="#f8fafc"/>',
        '<stop offset="100%" stop-color="#ffffff"/>',
        "</linearGradient>",
        '<filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">',
        '<feDropShadow dx="0" dy="1" stdDeviation="1.4" flood-color="#94a3b8" flood-opacity="0.25"/>',
        "</filter>",
        "</defs>",
        '<rect width="100%" height="100%" fill="url(#bgGrad)"/>',
        f'<text x="{width/2}" y="24" text-anchor="middle" font-size="17" font-family="Inter, Segoe UI, Arial, sans-serif" font-weight="700" fill="#0f172a">{esc(title)}</text>',
        f'<text x="{width/2}" y="42" text-anchor="middle" font-size="11" font-family="Inter, Segoe UI, Arial, sans-serif" fill="#64748b">GitHub static chart · range 0-100%</text>',
    ]

    if not all_points:
        svg.append(
            f'<text x="{width/2}" y="{height/2}" text-anchor="middle" font-size="14" font-family="Inter, Segoe UI, Arial, sans-serif" fill="#334155">No data available.</text>'
        )
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

    svg.append(
        f'<rect x="{m_left}" y="{m_top}" width="{inner_w}" height="{inner_h}" fill="#ffffff" stroke="#e2e8f0" stroke-width="1" rx="8"/>'
    )

    for i in range(6):
        yv = 100 - i * 20
        y = sy(yv)
        stroke = "#cbd5e1" if i in (0, 5) else "#e2e8f0"
        svg.append(
            f'<line x1="{m_left}" y1="{y:.2f}" x2="{width-m_right}" y2="{y:.2f}" stroke="{stroke}" stroke-width="1"/>'
        )
        svg.append(
            f'<text x="{m_left-10}" y="{y+4:.2f}" text-anchor="end" font-size="11" fill="#475569" font-family="Inter, Segoe UI, Arial, sans-serif">{yv}</text>'
        )

    svg.append(
        f'<line x1="{m_left}" y1="{height-m_bottom}" x2="{width-m_right}" y2="{height-m_bottom}" stroke="#94a3b8" stroke-width="1.2"/>'
    )

    for i in range(5):
        ts = int(min_ts + (max_ts - min_ts) * (i / 4))
        x = sx(ts)
        lbl = time_label(ts)
        svg.append(
            f'<line x1="{x:.2f}" y1="{m_top}" x2="{x:.2f}" y2="{height-m_bottom}" stroke="#f1f5f9" stroke-width="1"/>'
        )
        svg.append(
            f'<text x="{x:.2f}" y="{height-m_bottom+18}" text-anchor="middle" font-size="10" fill="#475569" font-family="Inter, Segoe UI, Arial, sans-serif">{esc(lbl)}</text>'
        )

    servers = sorted(server_points.keys())
    for idx, server in enumerate(servers):
        color = PALETTE[idx % len(PALETTE)]
        pts = server_points[server]
        if len(pts) == 1:
            ts, y = pts[0]
            svg.append(f'<circle cx="{sx(ts):.2f}" cy="{sy(y):.2f}" r="3.8" fill="{color}" filter="url(#softShadow)"/>')
            continue

        point_text = " ".join(f"{sx(ts):.2f},{sy(y):.2f}" for ts, y in pts)
        svg.append(
            f'<polyline fill="none" stroke="{color}" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" points="{point_text}" filter="url(#softShadow)"/>'
        )
        for ts, y in pts:
            svg.append(f'<circle cx="{sx(ts):.2f}" cy="{sy(y):.2f}" r="2.6" fill="{color}"/>')
            svg.append(f'<circle cx="{sx(ts):.2f}" cy="{sy(y):.2f}" r="1.2" fill="#ffffff"/>')

    legend_cols = 3
    legend_rows = (len(servers) + legend_cols - 1) // legend_cols
    legend_start_y = height - 45
    for idx, server in enumerate(servers):
        color = PALETTE[idx % len(PALETTE)]
        col = idx % legend_cols
        row = idx // legend_cols
        x = m_left + col * 340
        y = legend_start_y + row * 16
        svg.append(f'<rect x="{x}" y="{y-10}" width="12" height="12" rx="3" fill="{color}"/>')
        svg.append(
            f'<text x="{x+18}" y="{y}" font-size="11" fill="#334155" font-family="Inter, Segoe UI, Arial, sans-serif">{esc(server)}</text>'
        )

    svg.append("</svg>")
    return "\n".join(svg)


def main():
    os.makedirs(PLOTS_DIR, exist_ok=True)
    rows = load_rows(CSV_FILE)
    for key, title in METRICS:
        svg = build_chart(rows, key, title)
        with open(os.path.join(PLOTS_DIR, f"{key}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)


if __name__ == "__main__":
    main()
