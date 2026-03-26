"""Tests for process_data.py — focused on generate_history hourly bucketing."""

import pytest
from process_data import generate_history


def _make_row(epoch, server, status="up", cuda_ok="1", mumax3_ok="1"):
    """Build a minimal CSV-style dict matching process_data's expected format."""
    return {
        "timestamp_utc": f"2026-03-26T00:00:00Z",
        "timestamp_epoch": str(epoch),
        "server": server,
        "status": status,
        "cuda_ok": cuda_ok,
        "mumax3_ok": mumax3_ok,
        "gpu_util_pct": "0",
        "cpu_util_pct": "0",
        "ram_free_gb": "28",
        "ram_total_gb": "31",
        "gpu_count": "1",
        "gpu_free_count": "1",
        "gpu_names": "GTX 1080 Ti",
        "mumax3_version": "3.11",
        "cuda_driver_version": "12.9",
    }


class TestGenerateHistoryWorstPerHour:
    """generate_history should report the WORST on/cuda/mumax per hour bucket,
    not just the latest value. A confirmed-down event that recovers within the
    same hour must still show on=0 in that hour's entry."""

    def test_confirmed_down_and_recovery_same_hour(self):
        """Bug reproduction: nsc2 went confirmed-down at 17:05 and recovered
        at 17:10. The history entry for hour 17 should show on=0."""
        # All timestamps in the same hour bucket (17:00-17:59 UTC, 2026-03-26)
        # hour bucket = epoch // 3600
        base = 1774544400  # 2026-03-26T17:00:00Z exactly

        rows = [
            _make_row(base + 300, "nsc2", status="down"),   # 17:05 — confirmed down
            _make_row(base + 600, "nsc2", status="up"),      # 17:10 — recovered
            _make_row(base + 2700, "nsc2", status="up"),     # 17:45 — regular report
        ]

        history = generate_history(rows)
        nsc2_entries = [e for e in history["entries"] if e["s"] == "nsc2"]

        assert len(nsc2_entries) == 1, "Should have exactly one entry for the hour"
        assert nsc2_entries[0]["on"] == 0, (
            "Hour bucket should show on=0 because server was confirmed down "
            "during this hour, even though it recovered"
        )

    def test_cuda_failure_and_recovery_same_hour(self):
        """If CUDA fails and recovers within the same hour, cuda should be 0."""
        base = 1774544400

        rows = [
            _make_row(base + 300, "nsc2", cuda_ok="0"),
            _make_row(base + 2700, "nsc2", cuda_ok="1"),
        ]

        history = generate_history(rows)
        nsc2_entries = [e for e in history["entries"] if e["s"] == "nsc2"]

        assert len(nsc2_entries) == 1
        assert nsc2_entries[0]["cuda"] == 0, (
            "Hour bucket should show cuda=0 because CUDA failed during this hour"
        )

    def test_mumax_failure_and_recovery_same_hour(self):
        """If mumax3 fails and recovers within the same hour, mumax should be 0."""
        base = 1774544400

        rows = [
            _make_row(base + 300, "nsc2", mumax3_ok="0"),
            _make_row(base + 2700, "nsc2", mumax3_ok="1"),
        ]

        history = generate_history(rows)
        nsc2_entries = [e for e in history["entries"] if e["s"] == "nsc2"]

        assert len(nsc2_entries) == 1
        assert nsc2_entries[0]["mumax"] == 0, (
            "Hour bucket should show mumax=0 because mumax3 failed during this hour"
        )

    def test_all_up_within_hour_stays_up(self):
        """If all reports in an hour are up, the bucket should show on=1."""
        base = 1774544400

        rows = [
            _make_row(base + 300, "nsc2", status="up"),
            _make_row(base + 2700, "nsc2", status="up"),
        ]

        history = generate_history(rows)
        nsc2_entries = [e for e in history["entries"] if e["s"] == "nsc2"]

        assert len(nsc2_entries) == 1
        assert nsc2_entries[0]["on"] == 1

    def test_degraded_does_not_count_as_down(self):
        """Degraded status should still map to on=1 (SSH reachable)."""
        base = 1774544400

        rows = [
            _make_row(base + 300, "nsc2", status="degraded"),
            _make_row(base + 2700, "nsc2", status="up"),
        ]

        history = generate_history(rows)
        nsc2_entries = [e for e in history["entries"] if e["s"] == "nsc2"]

        assert len(nsc2_entries) == 1
        assert nsc2_entries[0]["on"] == 1

    def test_metrics_use_latest_value(self):
        """Non-status fields (gpu_u, cpu_u, etc.) should still use the latest row."""
        base = 1774544400

        rows = [
            _make_row(base + 300, "nsc2", status="down"),
            _make_row(base + 2700, "nsc2", status="up"),
        ]
        # Set different metric values to distinguish which row is used
        rows[0]["cpu_util_pct"] = "50.0"
        rows[1]["cpu_util_pct"] = "10.0"

        history = generate_history(rows)
        nsc2_entries = [e for e in history["entries"] if e["s"] == "nsc2"]

        assert nsc2_entries[0]["cpu_u"] == 10.0, (
            "Metrics should use the latest row's values"
        )
        assert nsc2_entries[0]["on"] == 0, (
            "But status should use worst value"
        )

    def test_na_values_do_not_override_known_failures(self):
        """An NA value for cuda/mumax should not override a known 0."""
        base = 1774544400

        rows = [
            _make_row(base + 300, "nsc2", cuda_ok="0", mumax3_ok="0"),
            _make_row(base + 2700, "nsc2", cuda_ok="NA", mumax3_ok="NA"),
        ]

        history = generate_history(rows)
        nsc2_entries = [e for e in history["entries"] if e["s"] == "nsc2"]

        assert nsc2_entries[0]["cuda"] == 0
        assert nsc2_entries[0]["mumax"] == 0
