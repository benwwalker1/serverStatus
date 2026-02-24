# Server Status Dashboard

Updated: **2026-02-24T06:22:59Z**

## Current Fleet Status

| Server | Ping | CUDA | Mumax3 | CPU util. | GPU util. | CPU(logical/physical) | GPU count |
| ------ | ---- | ---- | ------ | --------- | --------- | -------------------- | --------- |
| nsc1.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 40.80% | 0.00% | 38/20 | 1 |
| nsc2.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 56.50% | 0.00% | 16/8 | 1 |
| nsc3.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 0.20% | 0.00% | 24/12 | 2 |
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
| nsc1.utdallas.edu | 3303 | 100.00% | 99.94% | 100.00% | 10.04% | 0.05% | 31 | 0 |
| nsc2.utdallas.edu | 3304 | 100.00% | 99.91% | 99.91% | 12.59% | 0.00% | 369 | 0 |
| nsc3.utdallas.edu | 3304 | 100.00% | 87.35% | 87.35% | 19.94% | 0.00% | 638 | 0 |
| nsc4.utdallas.edu | 3304 | 100.00% | 100.00% | 100.00% | 0.65% | 0.00% | 0 | 0 |

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
| nsc3.utdallas.edu | 30d | 100.00% | 87.35% | 87.35% |
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
| 2026-02-24T05:05:01Z | nsc2.utdallas.edu | online | ok | ok | 55.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T05:05:01Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T05:05:01Z | nsc4.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T05:10:35Z | nsc1.utdallas.edu | online | ok | ok | 40.50% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T05:10:35Z | nsc2.utdallas.edu | online | ok | ok | 55.90% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T05:10:35Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T05:10:35Z | nsc4.utdallas.edu | online | ok | ok | 0.80% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T05:16:12Z | nsc1.utdallas.edu | online | ok | ok | 43.10% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T05:16:12Z | nsc2.utdallas.edu | online | ok | ok | 55.50% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T05:16:12Z | nsc3.utdallas.edu | online | ok | ok | 100.00% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T05:16:12Z | nsc4.utdallas.edu | online | ok | ok | 1.90% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T05:21:50Z | nsc1.utdallas.edu | online | ok | ok | 40.40% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T05:21:50Z | nsc2.utdallas.edu | online | ok | ok | 55.80% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T05:21:50Z | nsc3.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T05:21:50Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T05:27:22Z | nsc1.utdallas.edu | online | ok | ok | 40.90% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T05:27:22Z | nsc2.utdallas.edu | online | ok | ok | 55.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T05:27:22Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T05:27:22Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T05:32:57Z | nsc1.utdallas.edu | online | ok | ok | 40.70% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T05:32:57Z | nsc2.utdallas.edu | online | ok | ok | 28.00% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T05:32:57Z | nsc3.utdallas.edu | online | ok | ok | 100.00% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T05:32:57Z | nsc4.utdallas.edu | online | ok | ok | 1.10% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T05:38:27Z | nsc1.utdallas.edu | online | ok | ok | 41.10% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T05:38:27Z | nsc2.utdallas.edu | online | ok | ok | 56.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T05:38:27Z | nsc3.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T05:38:27Z | nsc4.utdallas.edu | online | ok | ok | 0.80% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T05:44:01Z | nsc1.utdallas.edu | online | ok | ok | 40.40% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T05:44:01Z | nsc2.utdallas.edu | online | ok | ok | 56.20% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T05:44:01Z | nsc3.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T05:44:01Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T05:49:34Z | nsc1.utdallas.edu | online | ok | ok | 40.70% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T05:49:34Z | nsc2.utdallas.edu | online | ok | ok | 56.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T05:49:34Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T05:49:34Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T05:55:06Z | nsc1.utdallas.edu | online | ok | ok | 40.60% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T05:55:06Z | nsc2.utdallas.edu | online | ok | ok | 59.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T05:55:06Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T05:55:06Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T06:00:39Z | nsc1.utdallas.edu | online | ok | ok | 40.70% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T06:00:39Z | nsc2.utdallas.edu | online | ok | ok | 61.80% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T06:00:39Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T06:00:39Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T06:06:17Z | nsc1.utdallas.edu | online | ok | ok | 40.50% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T06:06:17Z | nsc2.utdallas.edu | online | ok | ok | 58.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T06:06:17Z | nsc3.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T06:06:17Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T06:11:52Z | nsc1.utdallas.edu | online | ok | ok | 40.70% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T06:11:52Z | nsc2.utdallas.edu | online | ok | ok | 56.90% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T06:11:52Z | nsc3.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T06:11:52Z | nsc4.utdallas.edu | online | ok | ok | 0.80% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T06:17:24Z | nsc1.utdallas.edu | online | ok | ok | 40.80% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T06:17:24Z | nsc2.utdallas.edu | online | ok | ok | 56.80% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T06:17:24Z | nsc3.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T06:17:24Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T06:22:59Z | nsc1.utdallas.edu | online | ok | ok | 40.80% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T06:22:59Z | nsc2.utdallas.edu | online | ok | ok | 56.50% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T06:22:59Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T06:22:59Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |

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
