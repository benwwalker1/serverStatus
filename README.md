# Server Status Dashboard

Updated: **2026-02-24T16:58:13Z**

## Current Fleet Status

| Server | Ping | CUDA | Mumax3 | CPU util. | GPU util. | CPU(logical/physical) | GPU count |
| ------ | ---- | ---- | ------ | --------- | --------- | -------------------- | --------- |
| nsc1.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 40.60% | 0.00% | 38/20 | 1 |
| nsc2.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 41.30% | 0.00% | 16/8 | 1 |
| nsc3.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 4.20% | 0.00% | 24/12 | 2 |
| nsc4.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 0.40% | 0.00% | 24/12 | 2 |

## Hardware Inventory (latest known)

| Server | Logical CPUs | Physical CPUs | GPU count | GPU model(s) | RAM total (GB) |
| ------ | ------------ | ------------- | --------- | ------------ | -------------- |
| nsc1.utdallas.edu | 38 | 20 | 1 | Tesla P100-PCIE-16GB | 125.16 |
| nsc2.utdallas.edu | 16 | 8 | 1 | NVIDIA GeForce GTX 1080 Ti | 31.02 |
| nsc3.utdallas.edu | 24 | 12 | 2 | NVIDIA GeForce RTX 2080 Ti;NVIDIA GeForce RTX 2080 Ti | 31.01 |
| nsc4.utdallas.edu | 24 | 12 | 2 | NVIDIA GeForce RTX 2080 Ti;NVIDIA GeForce RTX 2080 Ti | 30.96 |

## Reliability & Utilization (all samples)

| Server | Samples | Ping uptime | CUDA healthy | Mumax3 healthy | Avg CPU util. | Avg GPU util. | CPU>85% samples | GPU>90% samples |
| ------ | ------- | ----------- | ------------ | -------------- | ------------- | ------------- | --------------- | --------------- |
| nsc1.utdallas.edu | 3418 | 100.00% | 99.94% | 100.00% | 10.94% | 0.05% | 31 | 0 |
| nsc2.utdallas.edu | 3419 | 100.00% | 99.91% | 99.91% | 13.95% | 0.00% | 369 | 0 |
| nsc3.utdallas.edu | 3419 | 100.00% | 87.77% | 87.77% | 19.93% | 0.00% | 660 | 0 |
| nsc4.utdallas.edu | 3419 | 100.00% | 100.00% | 100.00% | 0.65% | 0.00% | 0 | 0 |

## SLO Rollups

| Server | Window | Ping uptime | CUDA healthy | Mumax3 healthy |
| ------ | ------ | ----------- | ------------ | -------------- |
| nsc1.utdallas.edu | 24h | 100.00% | 100.00% | 100.00% |
| nsc1.utdallas.edu | 7d | 100.00% | 99.95% | 100.00% |
| nsc1.utdallas.edu | 30d | 100.00% | 99.94% | 100.00% |
| nsc2.utdallas.edu | 24h | 100.00% | 100.00% | 100.00% |
| nsc2.utdallas.edu | 7d | 100.00% | 100.00% | 100.00% |
| nsc2.utdallas.edu | 30d | 100.00% | 99.91% | 99.91% |
| nsc3.utdallas.edu | 24h | 100.00% | 100.00% | 100.00% |
| nsc3.utdallas.edu | 7d | 100.00% | 100.00% | 100.00% |
| nsc3.utdallas.edu | 30d | 100.00% | 87.77% | 87.77% |
| nsc4.utdallas.edu | 24h | 100.00% | 100.00% | 100.00% |
| nsc4.utdallas.edu | 7d | 100.00% | 100.00% | 100.00% |
| nsc4.utdallas.edu | 30d | 100.00% | 100.00% | 100.00% |

## Incidents & State Changes (latest 25 transitions)

| Timestamp (UTC) | Server | Signal | Transition |
| --------------- | ------ | ------ | ---------- |
| 2026-02-13T06:24:11Z | nsc3.utdallas.edu | CUDA | error -> ok |
| 2026-02-13T06:24:11Z | nsc3.utdallas.edu | Mumax3 | error -> ok |
| 2026-02-16T10:30:53Z | nsc1.utdallas.edu | CUDA | ok -> error |
| 2026-02-16T10:36:38Z | nsc1.utdallas.edu | CUDA | error -> ok |
| 2026-02-16T23:05:11Z | nsc3.utdallas.edu | CUDA | ok -> error |
| 2026-02-16T23:05:11Z | nsc3.utdallas.edu | Mumax3 | ok -> error |
| 2026-02-16T23:15:02Z | nsc3.utdallas.edu | CUDA | error -> ok |
| 2026-02-16T23:15:02Z | nsc3.utdallas.edu | Mumax3 | error -> ok |
| 2026-02-16T23:20:53Z | nsc2.utdallas.edu | CUDA | ok -> error |
| 2026-02-16T23:20:53Z | nsc2.utdallas.edu | Mumax3 | ok -> error |
| 2026-02-16T23:30:52Z | nsc2.utdallas.edu | CUDA | error -> ok |
| 2026-02-16T23:30:52Z | nsc2.utdallas.edu | Mumax3 | error -> ok |
| 2026-02-16T23:36:25Z | nsc2.utdallas.edu | CUDA | ok -> error |
| 2026-02-16T23:36:25Z | nsc2.utdallas.edu | Mumax3 | ok -> error |
| 2026-02-16T23:36:25Z | nsc3.utdallas.edu | CUDA | ok -> error |
| 2026-02-16T23:36:25Z | nsc3.utdallas.edu | Mumax3 | ok -> error |
| 2026-02-16T23:41:06Z | nsc2.utdallas.edu | CUDA | error -> ok |
| 2026-02-16T23:41:06Z | nsc2.utdallas.edu | Mumax3 | error -> ok |
| 2026-02-16T23:41:06Z | nsc3.utdallas.edu | CUDA | error -> ok |
| 2026-02-16T23:41:06Z | nsc3.utdallas.edu | Mumax3 | error -> ok |
| 2026-02-19T02:14:56Z | nsc1.utdallas.edu | CUDA | ok -> error |
| 2026-02-19T02:21:06Z | nsc1.utdallas.edu | CUDA | error -> ok |

## Historical Plots

![Ping uptime plot](plots/ping.svg)

![CUDA health plot](plots/cuda_ok.svg)

![Mumax3 health plot](plots/mumax3_ok.svg)

![CPU utilization plot](plots/cpu_utilization.svg)

![GPU utilization plot](plots/gpu_utilization.svg)

## Recent Samples

<details>
<summary>Expand to view the latest 60 samples</summary>

| Timestamp (UTC) | Server | Ping | CUDA | Mumax3 | CPU util. | GPU util. | CPU(logical/physical) | GPU count | RAM GB |
| --------------- | ------ | ---- | ---- | ------ | --------- | --------- | -------------------- | --------- | ------ |
| 2026-02-24T15:40:48Z | nsc2.utdallas.edu | online | ok | ok | 57.10% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T15:40:48Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T15:40:48Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T15:46:27Z | nsc1.utdallas.edu | online | ok | ok | 38.10% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T15:46:27Z | nsc2.utdallas.edu | online | ok | ok | 57.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T15:46:27Z | nsc3.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T15:46:27Z | nsc4.utdallas.edu | online | ok | ok | 0.90% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T15:51:56Z | nsc1.utdallas.edu | online | ok | ok | 38.20% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T15:51:56Z | nsc2.utdallas.edu | online | ok | ok | 57.20% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T15:51:56Z | nsc3.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T15:51:56Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T15:57:20Z | nsc1.utdallas.edu | online | ok | ok | 38.40% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T15:57:20Z | nsc2.utdallas.edu | online | ok | ok | 57.50% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T15:57:20Z | nsc3.utdallas.edu | online | ok | ok | 100.00% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T15:57:20Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T16:02:53Z | nsc1.utdallas.edu | online | ok | ok | 35.50% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T16:02:53Z | nsc2.utdallas.edu | online | ok | ok | 57.40% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T16:02:53Z | nsc3.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T16:02:53Z | nsc4.utdallas.edu | online | ok | ok | 1.00% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T16:08:21Z | nsc1.utdallas.edu | online | ok | ok | 38.30% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T16:08:21Z | nsc2.utdallas.edu | online | ok | ok | 55.90% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T16:08:21Z | nsc3.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T16:08:21Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T16:13:46Z | nsc1.utdallas.edu | online | ok | ok | 38.10% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T16:13:46Z | nsc2.utdallas.edu | online | ok | ok | 57.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T16:13:46Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T16:13:46Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T16:19:14Z | nsc1.utdallas.edu | online | ok | ok | 38.10% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T16:19:14Z | nsc2.utdallas.edu | online | ok | ok | 56.50% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T16:19:14Z | nsc3.utdallas.edu | online | ok | ok | 100.00% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T16:19:14Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T16:24:47Z | nsc1.utdallas.edu | online | ok | ok | 38.10% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T16:24:47Z | nsc2.utdallas.edu | online | ok | ok | 56.90% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T16:24:47Z | nsc3.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T16:24:47Z | nsc4.utdallas.edu | online | ok | ok | 0.80% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T16:30:18Z | nsc1.utdallas.edu | online | ok | ok | 37.90% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T16:30:18Z | nsc2.utdallas.edu | online | ok | ok | 56.70% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T16:30:18Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T16:30:18Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T16:35:52Z | nsc1.utdallas.edu | online | ok | ok | 38.00% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T16:35:52Z | nsc2.utdallas.edu | online | ok | ok | 56.90% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T16:35:52Z | nsc3.utdallas.edu | online | ok | ok | 100.00% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T16:35:52Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T16:41:18Z | nsc1.utdallas.edu | online | ok | ok | 38.10% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T16:41:18Z | nsc2.utdallas.edu | online | ok | ok | 59.40% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T16:41:18Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T16:41:18Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T16:47:10Z | nsc1.utdallas.edu | online | ok | ok | 38.00% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T16:47:10Z | nsc2.utdallas.edu | online | ok | ok | 63.80% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T16:47:10Z | nsc3.utdallas.edu | online | ok | ok | 16.90% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T16:47:10Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T16:52:47Z | nsc1.utdallas.edu | online | ok | ok | 38.50% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T16:52:47Z | nsc2.utdallas.edu | online | ok | ok | 68.80% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T16:52:47Z | nsc3.utdallas.edu | online | ok | ok | 4.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T16:52:47Z | nsc4.utdallas.edu | online | ok | ok | 9.00% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T16:58:13Z | nsc1.utdallas.edu | online | ok | ok | 40.60% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T16:58:13Z | nsc2.utdallas.edu | online | ok | ok | 41.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T16:58:13Z | nsc3.utdallas.edu | online | ok | ok | 4.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T16:58:13Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |

</details>

## How checks work

1. **Ping**: ICMP ping from the monitoring host.
2. **CUDA health**: SSH + `nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits`.
3. **Mumax3 health**: SSH + `mumax3 -version` (fallback to `mumax3 -v` / `mumax3`).
4. **CPU utilization**: SSH + `top` (fallback `vmstat`) parsed as active CPU%.
5. **Hardware inventory**: SSH + `nproc`, `lscpu`, `nvidia-smi`, and `/proc/meminfo`.

## GitHub-first rendering notes

- README only uses GitHub-supported Markdown tables and static SVG images.
- Interactive JavaScript charts are intentionally avoided so everything renders directly on GitHub.
