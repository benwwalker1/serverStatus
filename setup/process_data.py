#!/usr/bin/env python3
"""Data pipeline for coordinated server monitoring.

Called by monitor.sh on the leader server. Reads state files from the shared
filesystem, determines server status (incorporating SSH reachability),
maintains a local CSV history, and produces a single dashboard.json for GitHub.
"""

import argparse
import csv
import json
import os
import glob
from datetime import datetime, timezone

SERVERS = ["nsc1", "nsc2", "nsc3", "nsc4"]
HISTORY_DAYS = 7
ARCHIVE_DAYS = 30

CSV_HEADER = [
    "timestamp_utc", "timestamp_epoch", "server", "status",
    "cuda_ok", "mumax3_ok", "gpu_util_pct", "cpu_util_pct",
    "ram_free_gb", "ram_total_gb", "gpu_count", "gpu_free_count", "gpu_names",
    "mumax3_version", "cuda_driver_version", "reachable_from",
]

USER_CSV_HEADER = [
    "timestamp_epoch", "server", "user",
    "cpu_pct", "gpu_pct", "gpu_mem_mb", "ram_pct", "num_processes",
]

# Incident detection threshold — matches STALE_THRESHOLD from config
STALE_SECONDS = 600


# ── Helpers ──────────────────────────────────────────────────

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


def _strval(val):
    if val in (None, "NA", "", "null", "None"):
        return None
    return str(val)


# ── State & Reachability ─────────────────────────────────────

def load_state_files(state_dir):
    """Load per-server state JSONs from the shared state directory."""
    states = {}
    for path in glob.glob(os.path.join(state_dir, "*.json")):
        try:
            with open(path) as f:
                data = json.load(f)
            states[data["server"]] = data
        except (json.JSONDecodeError, KeyError, OSError):
            continue
    return states


def load_reachability_files(reach_dir):
    """Load per-server SSH reachability JSONs."""
    reach = {}
    for path in glob.glob(os.path.join(reach_dir, "*.json")):
        try:
            with open(path) as f:
                data = json.load(f)
            reach[data["observer"]] = data
        except (json.JSONDecodeError, KeyError, OSError):
            continue
    return reach


def determine_status(server, now_epoch, states, reach, stale_threshold, reach_threshold):
    """Determine a server's status using self-report freshness + SSH reachability.

    Returns (status, reason, reachable_from):
      - "up"       : fresh self-report
      - "degraded" : SSH-reachable but no fresh self-report
      - "down"     : stale/missing self-report AND unreachable
    """
    state = states.get(server)

    # Check self-report freshness
    if state and (now_epoch - int(state["timestamp_epoch"])) < stale_threshold:
        has_fresh_report = True
    else:
        has_fresh_report = False

    # Check SSH reachability from peers
    reachable_from = []
    for observer, probe in reach.items():
        if observer == server:
            continue
        if (now_epoch - int(probe["timestamp_epoch"])) > reach_threshold:
            continue  # stale probe
        if probe.get("targets", {}).get(server) == 1:
            reachable_from.append(observer)

    if has_fresh_report:
        return "up", "fresh_self_report", reachable_from
    elif reachable_from:
        return "degraded", "ssh_reachable_but_no_self_report", reachable_from
    else:
        if state:
            return "down", "stale_report_and_unreachable", reachable_from
        else:
            return "down", "no_report_and_unreachable", reachable_from


# ── CSV Operations ───────────────────────────────────────────

def ensure_csv(csv_file):
    """Create CSV with header if it doesn't exist, or migrate header if outdated."""
    if not os.path.exists(csv_file):
        with open(csv_file, "w", newline="") as f:
            csv.writer(f).writerow(CSV_HEADER)
        return

    with open(csv_file, newline="") as f:
        reader = csv.reader(f)
        existing_header = next(reader, [])

    if existing_header != CSV_HEADER:
        rows = load_csv(csv_file)
        with open(csv_file, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CSV_HEADER, extrasaction="ignore")
            w.writeheader()
            for row in rows:
                clean = {k: v for k, v in row.items() if k is not None}
                # Map old 'online' column to new 'status' column
                if "online" in clean and "status" not in clean:
                    clean["status"] = "up" if clean["online"] == "1" else "down"
                for col in CSV_HEADER:
                    if col not in clean:
                        clean[col] = ""
                w.writerow(clean)
        print(f"Migrated CSV header: added {set(CSV_HEADER) - set(existing_header)}")


def load_csv(csv_file):
    rows = []
    if not os.path.exists(csv_file):
        return rows
    with open(csv_file, newline="") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def last_csv_epoch(rows, server):
    for r in reversed(rows):
        if r["server"] == server:
            return int(r["timestamp_epoch"])
    return 0


def append_new_reports(csv_file, states, server_statuses, now_epoch, now_utc):
    """Append new rows to CSV for all servers, including explicit down/degraded rows."""
    existing = load_csv(csv_file)
    new_rows = []
    wrote_fresh = set()

    for srv in SERVERS:
        state = states.get(srv)
        status, _, reachable_from = server_statuses.get(srv, ("down", "", []))

        if not state:
            continue

        epoch = int(state["timestamp_epoch"])
        if epoch <= last_csv_epoch(existing, srv):
            continue

        def _v(key):
            v = state.get(key)
            return str(v) if v is not None else "NA"

        row = {
            "timestamp_utc": state["timestamp_utc"],
            "timestamp_epoch": str(epoch),
            "server": srv,
            "status": status,
            "cuda_ok": str(state.get("cuda_ok", 0)),
            "mumax3_ok": str(state.get("mumax3_ok", 0)),
            "gpu_util_pct": _v("gpu_util_pct"),
            "cpu_util_pct": _v("cpu_util_pct"),
            "ram_free_gb": _v("ram_free_gb"),
            "ram_total_gb": _v("ram_total_gb"),
            "gpu_count": _v("gpu_count"),
            "gpu_free_count": _v("gpu_free_count"),
            "gpu_names": _v("gpu_names"),
            "mumax3_version": _v("mumax3_version"),
            "cuda_driver_version": _v("cuda_driver_version"),
            "reachable_from": ",".join(reachable_from),
        }
        new_rows.append(row)
        wrote_fresh.add(srv)

    # Write explicit rows for servers that are down or degraded but had no fresh data.
    # This ensures the CSV (and therefore history) records downtime, not just silence.
    for srv in SERVERS:
        if srv in wrote_fresh:
            continue
        status, _, reachable_from = server_statuses.get(srv, ("down", "", []))
        if status == "up":
            continue

        last_ep = last_csv_epoch(existing + new_rows, srv)
        if now_epoch - last_ep < 120:
            continue  # avoid duplicate rows within the same cycle

        new_rows.append({
            "timestamp_utc": now_utc,
            "timestamp_epoch": str(now_epoch),
            "server": srv,
            "status": status,
            "cuda_ok": "NA",
            "mumax3_ok": "NA",
            "gpu_util_pct": "NA",
            "cpu_util_pct": "NA",
            "ram_free_gb": "NA",
            "ram_total_gb": "NA",
            "gpu_count": "NA",
            "gpu_free_count": "NA",
            "gpu_names": "NA",
            "mumax3_version": "NA",
            "cuda_driver_version": "NA",
            "reachable_from": ",".join(reachable_from),
        })

    if new_rows:
        with open(csv_file, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CSV_HEADER)
            for row in new_rows:
                w.writerow(row)
        print(f"Appended {len(new_rows)} new row(s) to CSV")
    return new_rows


# ── History Generation ───────────────────────────────────────

def generate_history(rows):
    """Generate 7-day hourly history entries."""
    now_epoch = int(datetime.now(timezone.utc).timestamp())
    cutoff = now_epoch - HISTORY_DAYS * 86400

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
        # Handle both old 'online' column and new 'status' column
        if "status" in r and r["status"]:
            on_val = 1 if r["status"] in ("up", "degraded") else 0
        elif "online" in r:
            on_val = int(r["online"]) if r.get("online") not in ("NA", "") else 0
        else:
            on_val = 0

        entries.append({
            "t": int(r["timestamp_epoch"]),
            "s": r["server"],
            "on": on_val,
            "cuda": _intval(r.get("cuda_ok")),
            "mumax": _intval(r.get("mumax3_ok")),
            "gpu_u": _num(r.get("gpu_util_pct")),
            "cpu_u": _num(r.get("cpu_util_pct")),
            "ram_f": _num(r.get("ram_free_gb")),
            "ram_t": _num(r.get("ram_total_gb")),
            "gpu_c": _intval(r.get("gpu_count")),
            "gpu_fc": _intval(r.get("gpu_free_count")),
            "gpu_n": _strval(r.get("gpu_names")),
            "mx_v": _strval(r.get("mumax3_version")),
            "cd_v": _strval(r.get("cuda_driver_version")),
        })

    return {"start": cutoff, "entries": entries}


# ── Incident Detection ───────────────────────────────────────

def generate_incidents(rows):
    """Detect state-change incidents from CSV history. Keeps last 200."""
    prev = {}
    last_epoch = {}
    stale_state = {}
    incidents = []

    for r in rows:
        srv = r["server"]
        epoch = int(r["timestamp_epoch"])

        # Check if this server was stale and is now reporting again
        if srv in stale_state and stale_state[srv]:
            ts = datetime.fromtimestamp(epoch, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            for name in ("Online", "CUDA", "Mumax3"):
                incidents.append({"t": epoch, "ts": ts, "s": srv, "c": name, "d": "up"})
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
        # Handle both old 'online' column and new 'status' column
        if "status" in r and r["status"]:
            online_val = "1" if r["status"] in ("up", "degraded") else "0"
        else:
            online_val = r.get("online", "1")

        checks = {
            "Online": online_val,
            "CUDA": r.get("cuda_ok", "NA"),
            "Mumax3": r.get("mumax3_ok", "NA"),
        }

        if srv in prev:
            for name, val in checks.items():
                if val == "NA":
                    checks[name] = prev[srv][name]
                    continue
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

    # Check for servers still stale at end of history
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

    # Sort and deduplicate
    incidents.sort(key=lambda x: x["t"])

    filtered = []
    groups = {}
    for inc in incidents:
        key = (inc["t"], inc["s"], inc["d"])
        groups.setdefault(key, set()).add(inc["c"])
    for inc in incidents:
        key = (inc["t"], inc["s"], inc["d"])
        cats = groups[key]
        if inc["c"] == "Mumax3" and ("Online" in cats or "CUDA" in cats):
            continue
        if inc["c"] == "CUDA" and "Online" in cats:
            continue
        filtered.append(inc)

    return filtered[-200:]


# ── Archival ─────────────────────────────────────────────────

def archive_old_data(csv_file, data_dir):
    """Move rows older than ARCHIVE_DAYS to monthly archive files."""
    rows = load_csv(csv_file)
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

    archive_dir = os.path.join(data_dir, "archive")
    os.makedirs(archive_dir, exist_ok=True)

    for month_key, month_rows in archive.items():
        path = os.path.join(archive_dir, f"{month_key}.csv")
        write_header = not os.path.exists(path)
        with open(path, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CSV_HEADER, extrasaction="ignore")
            if write_header:
                w.writeheader()
            for row in month_rows:
                w.writerow(row)
        print(f"Archived {len(month_rows)} rows to {path}")

    with open(csv_file, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_HEADER)
        w.writeheader()
        for row in keep:
            w.writerow(row)
    print(f"CSV trimmed to {len(keep)} rows")


# ── User Stats Pipeline ───────────────────────────────────────

USER_WINDOWS = {"24h": 86400, "7d": 604800, "30d": 2592000, "all": None}


def ensure_user_csv(csv_file):
    """Create user CSV with header if it doesn't exist."""
    if not os.path.exists(csv_file):
        with open(csv_file, "w", newline="") as f:
            csv.writer(f).writerow(USER_CSV_HEADER)


def load_user_csv(csv_file):
    rows = []
    if not os.path.exists(csv_file):
        return rows
    with open(csv_file, newline="") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def append_user_reports(csv_file, states, now_epoch):
    """Append per-user rows from state files to user CSV."""
    existing = load_user_csv(csv_file)
    # Find last recorded epoch per server
    last_epoch = {}
    for r in existing:
        srv = r["server"]
        ep = int(r["timestamp_epoch"])
        if ep > last_epoch.get(srv, 0):
            last_epoch[srv] = ep

    new_rows = []
    for srv in SERVERS:
        state = states.get(srv)
        if not state:
            continue
        epoch = int(state["timestamp_epoch"])
        if epoch <= last_epoch.get(srv, 0):
            continue
        users = state.get("users", [])
        for u in users:
            new_rows.append({
                "timestamp_epoch": str(epoch),
                "server": srv,
                "user": u.get("user", ""),
                "cpu_pct": str(u.get("cpu_pct", 0)),
                "gpu_pct": str(u.get("gpu_pct", 0)),
                "gpu_mem_mb": str(u.get("gpu_mem_mb", 0)),
                "ram_pct": str(u.get("ram_pct", 0)),
                "num_processes": str(u.get("num_processes", 0)),
            })

    if new_rows:
        with open(csv_file, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=USER_CSV_HEADER)
            for row in new_rows:
                w.writerow(row)
        print(f"Appended {len(new_rows)} user row(s) to CSV")


def generate_user_stats(user_rows, states, now_epoch):
    """Compute per-server, per-user averages for each time window."""
    result = {"generated_epoch": now_epoch, "servers": {}}

    for srv in SERVERS:
        # Current snapshot from state
        state = states.get(srv)
        current = state.get("users", []) if state else []

        averages = {}
        for window_name, window_secs in USER_WINDOWS.items():
            cutoff = (now_epoch - window_secs) if window_secs else 0
            filtered = [
                r for r in user_rows
                if r["server"] == srv and int(r["timestamp_epoch"]) >= cutoff
            ]

            by_user = {}
            for r in filtered:
                u = r["user"]
                if u not in by_user:
                    by_user[u] = {"cpu": [], "gpu": [], "gmem": [], "ram": []}
                by_user[u]["cpu"].append(float(r["cpu_pct"] or 0))
                by_user[u]["gpu"].append(float(r["gpu_pct"] or 0))
                by_user[u]["gmem"].append(float(r["gpu_mem_mb"] or 0))
                by_user[u]["ram"].append(float(r["ram_pct"] or 0))

            avg_list = []
            for u in sorted(by_user):
                data = by_user[u]
                avg_list.append({
                    "user": u,
                    "cpu_pct": round(sum(data["cpu"]) / len(data["cpu"]), 1),
                    "gpu_pct": round(sum(data["gpu"]) / len(data["gpu"]), 1),
                    "gpu_mem_mb": int(sum(data["gmem"]) / len(data["gmem"])),
                    "ram_pct": round(sum(data["ram"]) / len(data["ram"]), 1),
                })
            averages[window_name] = avg_list

        result["servers"][srv] = {"current": current, "averages": averages}

    return result


def archive_user_data(csv_file, data_dir):
    """Move user CSV rows older than ARCHIVE_DAYS to monthly archives."""
    rows = load_user_csv(csv_file)
    now_epoch = int(datetime.now(timezone.utc).timestamp())
    cutoff = now_epoch - ARCHIVE_DAYS * 86400

    keep = []
    archive = {}
    for r in rows:
        ep = int(r["timestamp_epoch"])
        if ep < cutoff:
            dt = datetime.fromtimestamp(ep, tz=timezone.utc)
            month_key = dt.strftime("%Y-%m")
            archive.setdefault(month_key, []).append(r)
        else:
            keep.append(r)

    if not archive:
        return

    archive_dir = os.path.join(data_dir, "archive")
    os.makedirs(archive_dir, exist_ok=True)

    for month_key, month_rows in archive.items():
        path = os.path.join(archive_dir, f"users-{month_key}.csv")
        write_header = not os.path.exists(path)
        with open(path, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=USER_CSV_HEADER, extrasaction="ignore")
            if write_header:
                w.writeheader()
            for row in month_rows:
                w.writerow(row)
        print(f"Archived {len(month_rows)} user rows to {path}")

    with open(csv_file, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=USER_CSV_HEADER)
        w.writeheader()
        for row in keep:
            w.writerow(row)
    print(f"User CSV trimmed to {len(keep)} rows")


# ── Main ─────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-dir", required=True)
    parser.add_argument("--reach-dir", required=True)
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--stale-threshold", type=int, default=600)
    parser.add_argument("--reach-threshold", type=int, default=600)
    parser.add_argument("--leader", required=True)
    args = parser.parse_args()

    global STALE_SECONDS
    STALE_SECONDS = args.stale_threshold

    now_epoch = int(datetime.now(timezone.utc).timestamp())
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Load shared state
    states = load_state_files(args.state_dir)
    reach = load_reachability_files(args.reach_dir)

    # Determine status for each server
    server_statuses = {}
    servers_json = {}
    for srv in SERVERS:
        status, reason, reachable_from = determine_status(
            srv, now_epoch, states, reach, args.stale_threshold, args.reach_threshold
        )
        server_statuses[srv] = (status, reason, reachable_from)

        state_data = states.get(srv)
        servers_json[srv] = {
            "status": status,
            "status_reason": reason,
            "state": state_data,
            "last_seen_epoch": int(state_data["timestamp_epoch"]) if state_data else 0,
            "reachable_from": reachable_from,
        }

    # Update CSV
    csv_file = os.path.join(args.data_dir, "status.csv")
    ensure_csv(csv_file)
    append_new_reports(csv_file, states, server_statuses, now_epoch, now_utc)

    # Generate history and incidents from full CSV
    all_rows = load_csv(csv_file)
    history = generate_history(all_rows)
    incidents = generate_incidents(all_rows)

    # Archive old data
    archive_old_data(csv_file, args.data_dir)

    # User stats pipeline
    user_csv_file = os.path.join(args.data_dir, "user_history.csv")
    ensure_user_csv(user_csv_file)
    append_user_reports(user_csv_file, states, now_epoch)
    user_rows = load_user_csv(user_csv_file)
    user_stats = generate_user_stats(user_rows, states, now_epoch)
    archive_user_data(user_csv_file, args.data_dir)

    user_stats_file = os.path.join(args.data_dir, "user_stats.json")
    with open(user_stats_file, "w") as f:
        json.dump(user_stats, f, separators=(",", ":"))
    print(f"User stats: {sum(len(v['current']) for v in user_stats['servers'].values())} active users across {len(user_stats['servers'])} servers")

    # Build dashboard.json
    dashboard = {
        "generated_epoch": now_epoch,
        "generated_utc": now_utc,
        "generated_by": args.leader,
        "stale_threshold": args.stale_threshold,
        "servers": servers_json,
        "history": history,
        "incidents": incidents,
    }

    dashboard_file = os.path.join(args.data_dir, "dashboard.json")
    with open(dashboard_file, "w") as f:
        json.dump(dashboard, f, separators=(",", ":"))

    print(f"Dashboard: {len(servers_json)} servers, {len(history['entries'])} history entries, {len(incidents)} incidents")


if __name__ == "__main__":
    main()
