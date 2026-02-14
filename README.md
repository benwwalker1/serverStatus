# Server Status Dashboard

Updated: **2026-02-14T13:15:43Z**

## Current Fleet Status

| Server | Ping | CUDA | Mumax3 | CPU util. | GPU util. | CPU(logical/physical) | GPU count |
| ------ | ---- | ---- | ------ | --------- | --------- | -------------------- | --------- |
| nsc1.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 25.50% | 0.00% | 38/20 | 1 |
| nsc2.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 0.60% | 0.00% | 16/8 | 1 |
| nsc3.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 4.40% | 0.00% | 24/12 | 2 |
| nsc4.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 0.60% | 0.00% | 24/12 | 2 |

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
| nsc1.utdallas.edu | 757 | 100.00% | 100.00% | 100.00% | 10.21% | 0.22% | 26 | 0 |
| nsc2.utdallas.edu | 758 | 100.00% | 100.00% | 100.00% | 13.93% | 0.00% | 101 | 0 |
| nsc3.utdallas.edu | 758 | 100.00% | 45.25% | 45.25% | 20.33% | 0.00% | 148 | 0 |
| nsc4.utdallas.edu | 758 | 100.00% | 100.00% | 100.00% | 0.66% | 0.00% | 0 | 0 |

## SLO Rollups

| Server | Window | Ping uptime | CUDA healthy | Mumax3 healthy |
| ------ | ------ | ----------- | ------------ | -------------- |
| nsc1.utdallas.edu | 24h | 100.00% | 100.00% | 100.00% |
| nsc1.utdallas.edu | 7d | 100.00% | 100.00% | 100.00% |
| nsc1.utdallas.edu | 30d | 100.00% | 100.00% | 100.00% |
| nsc2.utdallas.edu | 24h | 100.00% | 100.00% | 100.00% |
| nsc2.utdallas.edu | 7d | 100.00% | 100.00% | 100.00% |
| nsc2.utdallas.edu | 30d | 100.00% | 100.00% | 100.00% |
| nsc3.utdallas.edu | 24h | 100.00% | 100.00% | 100.00% |
| nsc3.utdallas.edu | 7d | 100.00% | 45.25% | 45.25% |
| nsc3.utdallas.edu | 30d | 100.00% | 45.25% | 45.25% |
| nsc4.utdallas.edu | 24h | 100.00% | 100.00% | 100.00% |
| nsc4.utdallas.edu | 7d | 100.00% | 100.00% | 100.00% |
| nsc4.utdallas.edu | 30d | 100.00% | 100.00% | 100.00% |

## Incidents & State Changes (latest 25 transitions)

| Timestamp (UTC) | Server | Signal | Transition |
| --------------- | ------ | ------ | ---------- |
| 2026-02-13T06:24:11Z | nsc3.utdallas.edu | CUDA | error -> ok |
| 2026-02-13T06:24:11Z | nsc3.utdallas.edu | Mumax3 | error -> ok |

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
| 2026-02-14T11:59:44Z | nsc2.utdallas.edu | online | ok | ok | 100.00% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-14T11:59:44Z | nsc3.utdallas.edu | online | ok | ok | 4.80% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-14T11:59:44Z | nsc4.utdallas.edu | online | ok | ok | 1.30% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-14T12:05:10Z | nsc1.utdallas.edu | online | ok | ok | 25.30% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-14T12:05:10Z | nsc2.utdallas.edu | online | ok | ok | 100.00% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-14T12:05:10Z | nsc3.utdallas.edu | online | ok | ok | 4.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-14T12:05:10Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-14T12:10:36Z | nsc1.utdallas.edu | online | ok | ok | 25.30% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-14T12:10:36Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-14T12:10:36Z | nsc3.utdallas.edu | online | ok | ok | 4.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-14T12:10:36Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-14T12:16:04Z | nsc1.utdallas.edu | online | ok | ok | 25.70% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-14T12:16:04Z | nsc2.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-14T12:16:04Z | nsc3.utdallas.edu | online | ok | ok | 4.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-14T12:16:04Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-14T12:21:29Z | nsc1.utdallas.edu | online | ok | ok | 25.40% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-14T12:21:29Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-14T12:21:29Z | nsc3.utdallas.edu | online | ok | ok | 4.00% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-14T12:21:29Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-14T12:26:57Z | nsc1.utdallas.edu | online | ok | ok | 25.80% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-14T12:26:57Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-14T12:26:57Z | nsc3.utdallas.edu | online | ok | ok | 4.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-14T12:26:57Z | nsc4.utdallas.edu | online | ok | ok | 0.80% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-14T12:32:21Z | nsc1.utdallas.edu | online | ok | ok | 25.20% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-14T12:32:21Z | nsc2.utdallas.edu | online | ok | ok | 1.20% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-14T12:32:21Z | nsc3.utdallas.edu | online | ok | ok | 4.00% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-14T12:32:21Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-14T12:37:47Z | nsc1.utdallas.edu | online | ok | ok | 25.70% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-14T12:37:47Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-14T12:37:47Z | nsc3.utdallas.edu | online | ok | ok | 4.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-14T12:37:47Z | nsc4.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-14T12:43:13Z | nsc1.utdallas.edu | online | ok | ok | 25.30% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-14T12:43:13Z | nsc2.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-14T12:43:13Z | nsc3.utdallas.edu | online | ok | ok | 4.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-14T12:43:13Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-14T12:48:37Z | nsc1.utdallas.edu | online | ok | ok | 25.30% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-14T12:48:37Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-14T12:48:37Z | nsc3.utdallas.edu | online | ok | ok | 8.50% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-14T12:48:37Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-14T12:54:00Z | nsc1.utdallas.edu | online | ok | ok | 25.50% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-14T12:54:00Z | nsc2.utdallas.edu | online | ok | ok | 1.20% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-14T12:54:00Z | nsc3.utdallas.edu | online | ok | ok | 4.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-14T12:54:00Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-14T12:59:26Z | nsc1.utdallas.edu | online | ok | ok | 25.40% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-14T12:59:26Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-14T12:59:26Z | nsc3.utdallas.edu | online | ok | ok | 4.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-14T12:59:26Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-14T13:04:49Z | nsc1.utdallas.edu | online | ok | ok | 25.40% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-14T13:04:49Z | nsc2.utdallas.edu | online | ok | ok | 0.90% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-14T13:04:49Z | nsc3.utdallas.edu | online | ok | ok | 4.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-14T13:04:49Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-14T13:10:16Z | nsc1.utdallas.edu | online | ok | ok | 3.00% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-14T13:10:16Z | nsc2.utdallas.edu | online | ok | ok | 0.90% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-14T13:10:16Z | nsc3.utdallas.edu | online | ok | ok | 4.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-14T13:10:16Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-14T13:15:43Z | nsc1.utdallas.edu | online | ok | ok | 25.50% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-14T13:15:43Z | nsc2.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-14T13:15:43Z | nsc3.utdallas.edu | online | ok | ok | 4.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-14T13:15:43Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |

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
