# Server Status Dashboard

Updated: **2026-02-11T15:13:35Z**

## Latest Check

| Server | Ping | CUDA | Mumax3 | GPU util. |
| ------ | ---- | ---- | ------ | --------- |
| nsc1.utdallas.edu | :+1: (online) | :+1: (ok) | :+1: (ok) | 0.00% |
| nsc2.utdallas.edu | :+1: (online) | :+1: (ok) | :+1: (ok) | 0.00% |
| nsc3.utdallas.edu | :+1: (online) | :+1: (ok) | :x: (error) | 0.00% |
| nsc4.utdallas.edu | :+1: (online) | :+1: (ok) | :+1: (ok) | 0.00% |

## Historical Reliability (all samples)

| Server | Samples | Ping uptime | CUDA healthy | Mumax3 healthy | Avg GPU util. |
| ------ | ------- | ----------- | ------------ | -------------- | ------------- |
| nsc1.utdallas.edu | 5 | 20.00% | 20.00% | 20.00% | 0.00% |
| nsc2.utdallas.edu | 5 | 20.00% | 20.00% | 20.00% | 0.00% |
| nsc3.utdallas.edu | 5 | 20.00% | 20.00% | 0.00% | 0.00% |
| nsc4.utdallas.edu | 5 | 20.00% | 20.00% | 20.00% | 0.00% |

## Recent Samples

<details>
<summary>Expand to view the latest 40 samples</summary>

| Timestamp (UTC) | Server | Ping | CUDA | Mumax3 | GPU util. |
| --------------- | ------ | ---- | ---- | ------ | --------- |
| 2026-02-11T15:08:35Z | nsc1.utdallas.edu | offline | unknown | unknown | NA |
| 2026-02-11T15:08:35Z | nsc2.utdallas.edu | offline | unknown | unknown | NA |
| 2026-02-11T15:08:35Z | nsc3.utdallas.edu | offline | unknown | unknown | NA |
| 2026-02-11T15:08:35Z | nsc4.utdallas.edu | offline | unknown | unknown | NA |
| 2026-02-11T15:08:58Z | nsc1.utdallas.edu | offline | unknown | unknown | NA |
| 2026-02-11T15:08:58Z | nsc2.utdallas.edu | offline | unknown | unknown | NA |
| 2026-02-11T15:08:58Z | nsc3.utdallas.edu | offline | unknown | unknown | NA |
| 2026-02-11T15:08:58Z | nsc4.utdallas.edu | offline | unknown | unknown | NA |
| 2026-02-11T15:09:12Z | nsc1.utdallas.edu | offline | unknown | unknown | NA |
| 2026-02-11T15:09:12Z | nsc2.utdallas.edu | offline | unknown | unknown | NA |
| 2026-02-11T15:09:12Z | nsc3.utdallas.edu | offline | unknown | unknown | NA |
| 2026-02-11T15:09:12Z | nsc4.utdallas.edu | offline | unknown | unknown | NA |
| 2026-02-11T15:09:30Z | nsc1.utdallas.edu | offline | unknown | unknown | NA |
| 2026-02-11T15:09:30Z | nsc2.utdallas.edu | offline | unknown | unknown | NA |
| 2026-02-11T15:09:30Z | nsc3.utdallas.edu | offline | unknown | unknown | NA |
| 2026-02-11T15:09:30Z | nsc4.utdallas.edu | offline | unknown | unknown | NA |
| 2026-02-11T15:13:35Z | nsc1.utdallas.edu | online | ok | ok | 0.00 |
| 2026-02-11T15:13:35Z | nsc2.utdallas.edu | online | ok | ok | 0.00 |
| 2026-02-11T15:13:35Z | nsc3.utdallas.edu | online | ok | error | 0.00 |
| 2026-02-11T15:13:35Z | nsc4.utdallas.edu | online | ok | ok | 0.00 |

</details>

## How checks work

1. **Ping**: ICMP ping from the external monitoring host.
2. **No CUDA errors**: SSH to the server and execute `nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits`.
3. **No mumax3 errors**: SSH to the server and run `mumax3 -version` (fallback to `mumax3 -v` / `mumax3`).
4. **GPU utilization**: Average of all GPUs returned by `nvidia-smi` during each check.

## Suggested next improvements

- Add alerting (email/Slack/webhook) when a category fails for N consecutive checks.
- Keep a separate `unknown` state in alert logic to avoid false alarms during SSH outages.
- Export CSV data to a time-series DB (Prometheus/InfluxDB) for long-term dashboards.
- Add per-host configuration (SSH user, GPU thresholds, custom mumax3 command).
