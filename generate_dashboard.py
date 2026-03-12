#!/usr/bin/env python3
"""Data pipeline: reads live server JSON, maintains CSV, generates history.json and incidents.json."""

import csv
import json
import os
import glob
from datetime import datetime, timezone

LIVE_DIR = "data/live"
CSV_FILE = "data/status.csv"
HISTORY_JSON = "data/history.json"
INCIDENTS_JSON = "data/incidents.json"
ARCHIVE_DIR = "data/archive"
SERVERS = ["nsc1", "nsc2", "nsc3", "nsc4"]
HISTORY_DAYS = 7
ARCHIVE_DAYS = 30

CSV_HEADER = [
    "timestamp_utc", "timestamp_epoch", "server", "online",
    "cuda_ok", "mumax3_ok", "gpu_util_pct", "cpu_util_pct",
    "ram_free_gb", "ram_total_gb", "gpu_count", "gpu_free_count", "gpu_names",
    "mumax3_version", "cuda_driver_version",
]


def ensure_dirs():
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            csv.writer(f).writerow(CSV_HEADER)


def load_live():
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
    for r in reversed(rows):
        if r["server"] == server:
            return int(r["timestamp_epoch"])
    return 0


def append_new_reports(live, existing_rows):
    new_rows = []
    for srv_name, data in live.items():
        epoch = int(data["timestamp_epoch"])
        if epoch <= last_csv_epoch(existing_rows, srv_name):
            continue

        def _v(key):
            v = data.get(key)
            return str(v) if v is not None else "NA"

        row = {
            "timestamp_utc": data["timestamp_utc"],
            "timestamp_epoch": str(epoch),
            "server": srv_name,
            "online": "1",
            "cuda_ok": str(data.get("cuda_ok", 0)),
            "mumax3_ok": str(data.get("mumax3_ok", 0)),
            "gpu_util_pct": _v("gpu_util_pct"),
            "cpu_util_pct": _v("cpu_util_pct"),
            "ram_free_gb": _v("ram_free_gb"),
            "ram_total_gb": _v("ram_total_gb"),
            "gpu_count": _v("gpu_count"),
            "gpu_free_count": _v("gpu_free_count"),
            "gpu_names": _v("gpu_names"),
            "mumax3_version": _v("mumax3_version"),
            "cuda_driver_version": _v("cuda_driver_version"),
        }
        new_rows.append(row)
    if new_rows:
        with open(CSV_FILE, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CSV_HEADER)
            for row in new_rows:
                w.writerow(row)
        print(f"Appended {len(new_rows)} new row(s) to CSV")
    return new_rows


def _num(val):
    if val in (None, "NA", "", "null", "None"):
        return None
    try:
        return round(float(val), 1)
    except (ValueError, TypeError):
        return None


def _intval(val):
    if val in (None, "NA", "", "null", "None"):
        return None
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return None


def generate_history_json(rows):
    """Generate history.json: one entry per server per hour, last 7 days."""
    now_epoch = int(datetime.now(timezone.utc).timestamp())
    cutoff = now_epoch - HISTORY_DAYS * 86400

    # Keep latest entry per (server, hour)
    hourly = {}
    for r in rows:
        epoch = int(r["timestamp_epoch"])
        if epoch < cutoff:
            continue
        key = (r["server"], epoch // 3600)
        if key not in hourly or epoch > int(hourly[key]["timestamp_epoch"]):
            hourly[key] = r

    entries = []
    for r in sorted(hourly.values(), key=lambda x: int(x["timestamp_epoch"])):
        entries.append({
            "t": int(r["timestamp_epoch"]),
            "s": r["server"],
            "on": int(r["online"]) if r["online"] not in ("NA", "") else 0,
            "cuda": int(r["cuda_ok"]) if r["cuda_ok"] not in ("NA", "") else 0,
            "mumax": int(r["mumax3_ok"]) if r["mumax3_ok"] not in ("NA", "") else 0,
            "gpu_u": _num(r.get("gpu_util_pct")),
            "cpu_u": _num(r.get("cpu_util_pct")),
            "ram_f": _num(r.get("ram_free_gb")),
            "ram_t": _num(r.get("ram_total_gb")),
            "gpu_c": _intval(r.get("gpu_count")),
            "gpu_fc": _intval(r.get("gpu_free_count")),
            "gpu_n": r.get("gpu_names") if r.get("gpu_names") not in ("NA", "", "None", None) else None,
            "mx_v": r.get("mumax3_version") if r.get("mumax3_version") not in ("NA", "", "None", None) else None,
            "cd_v": r.get("cuda_driver_version") if r.get("cuda_driver_version") not in ("NA", "", "None", None) else None,
        })

    with open(HISTORY_JSON, "w") as f:
        json.dump({
            "generated": now_epoch,
            "start": cutoff,
            "entries": entries,
        }, f, separators=(",", ":"))
    print(f"History JSON: {len(entries)} hourly entries")


STALE_SECONDS = 7200  # 2 hours without a report = server considered down
                      # (matches sparkline: 2+ consecutive null hourly buckets)


def generate_incidents_json(rows):
    """Pre-compute incidents from full CSV history, keep last 200.

    Also generates 'down' incidents when a server stops reporting for >30 min,
    and 'up' incidents when it resumes.
    """
    prev = {}
    last_epoch = {}
    stale_state = {}  # server -> True if currently marked stale
    incidents = []
    for r in rows:
        srv = r["server"]
        epoch = int(r["timestamp_epoch"])

        # Check if this server was stale and is now reporting again
        if srv in stale_state and stale_state[srv]:
            ts = datetime.fromtimestamp(epoch, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            for name in ("Online", "CUDA", "Mumax3"):
                incidents.append({
                    "t": epoch,
                    "ts": ts,
                    "s": srv,
                    "c": name,
                    "d": "up",
                })
            stale_state[srv] = False

        # Check all other servers for staleness at this timestamp
        for other_srv, other_epoch in list(last_epoch.items()):
            if other_srv == srv:
                continue
            if not stale_state.get(other_srv) and (epoch - other_epoch) > STALE_SECONDS:
                stale_ts = datetime.fromtimestamp(
                    other_epoch + STALE_SECONDS, tz=timezone.utc
                ).strftime("%Y-%m-%dT%H:%M:%SZ")
                for name in ("Online", "CUDA", "Mumax3"):
                    incidents.append({
                        "t": other_epoch + STALE_SECONDS,
                        "ts": stale_ts,
                        "s": other_srv,
                        "c": name,
                        "d": "down",
                    })
                stale_state[other_srv] = True

        # Normal state-change detection
        checks = {"Online": r["online"], "CUDA": r["cuda_ok"], "Mumax3": r["mumax3_ok"]}
        if srv in prev:
            for name, val in checks.items():
                if prev[srv][name] != val:
                    incidents.append({
                        "t": epoch,
                        "ts": r["timestamp_utc"],
                        "s": srv,
                        "c": name,
                        "d": "up" if val == "1" else "down",
                    })
        prev[srv] = checks
        last_epoch[srv] = epoch

    # Check for servers still stale at end of history (i.e., right now)
    now_epoch = int(datetime.now(timezone.utc).timestamp())
    for srv, epoch in last_epoch.items():
        if not stale_state.get(srv) and (now_epoch - epoch) > STALE_SECONDS:
            stale_ts = datetime.fromtimestamp(
                epoch + STALE_SECONDS, tz=timezone.utc
            ).strftime("%Y-%m-%dT%H:%M:%SZ")
            for name in ("Online", "CUDA", "Mumax3"):
                incidents.append({
                    "t": epoch + STALE_SECONDS,
                    "ts": stale_ts,
                    "s": srv,
                    "c": name,
                    "d": "down",
                })

    # Sort by timestamp and keep last 200
    incidents.sort(key=lambda x: x["t"])
    incidents = incidents[-200:]
    with open(INCIDENTS_JSON, "w") as f:
        json.dump({"incidents": incidents}, f, separators=(",", ":"))
    print(f"Incidents JSON: {len(incidents)} incidents")


def archive_old_data(rows):
    """Move rows older than ARCHIVE_DAYS to monthly archive files."""
    now_epoch = int(datetime.now(timezone.utc).timestamp())
    cutoff = now_epoch - ARCHIVE_DAYS * 86400

    keep = []
    archive = {}
    for r in rows:
        if int(r["timestamp_epoch"]) < cutoff:
            month_key = r["timestamp_utc"][:7]
            archive.setdefault(month_key, []).append(r)
        else:
            keep.append(r)

    if not archive:
        return

    for month_key, month_rows in archive.items():
        path = os.path.join(ARCHIVE_DIR, f"{month_key}.csv")
        write_header = not os.path.exists(path)
        with open(path, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CSV_HEADER)
            if write_header:
                w.writeheader()
            for row in month_rows:
                w.writerow(row)
        print(f"Archived {len(month_rows)} rows to {path}")

    with open(CSV_FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_HEADER)
        w.writeheader()
        for row in keep:
            w.writerow(row)
    print(f"CSV trimmed to {len(keep)} rows")


if __name__ == "__main__":
    ensure_dirs()
    live = load_live()
    existing = load_csv()
    append_new_reports(live, existing)
    all_rows = load_csv()
    generate_history_json(all_rows)
    generate_incidents_json(all_rows)
    archive_old_data(all_rows)
