# Server Status Dashboard

Updated: **2026-02-24T07:24:08Z**

## Current Fleet Status

| Server | Ping | CUDA | Mumax3 | CPU util. | GPU util. | CPU(logical/physical) | GPU count |
| ------ | ---- | ---- | ------ | --------- | --------- | -------------------- | --------- |
| nsc1.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 40.60% | 0.00% | 38/20 | 1 |
| nsc2.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 57.10% | 0.00% | 16/8 | 1 |
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
| nsc1.utdallas.edu | 3314 | 100.00% | 99.94% | 100.00% | 10.13% | 0.05% | 31 | 0 |
| nsc2.utdallas.edu | 3315 | 100.00% | 99.91% | 99.91% | 12.72% | 0.00% | 369 | 0 |
| nsc3.utdallas.edu | 3315 | 100.00% | 87.39% | 87.39% | 19.96% | 0.00% | 641 | 0 |
| nsc4.utdallas.edu | 3315 | 100.00% | 100.00% | 100.00% | 0.65% | 0.00% | 0 | 0 |

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
| nsc3.utdallas.edu | 30d | 100.00% | 87.39% | 87.39% |
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
| 2026-02-24T06:28:33Z | nsc1.utdallas.edu | online | ok | ok | 40.60% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T06:28:33Z | nsc2.utdallas.edu | online | ok | ok | 7.50% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T06:28:33Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T06:28:33Z | nsc4.utdallas.edu | online | ok | ok | 0.80% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T06:33:56Z | nsc1.utdallas.edu | online | ok | ok | 40.50% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T06:33:56Z | nsc2.utdallas.edu | online | ok | ok | 56.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T06:33:56Z | nsc3.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T06:33:56Z | nsc4.utdallas.edu | online | ok | ok | 0.80% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T06:39:29Z | nsc1.utdallas.edu | online | ok | ok | 35.60% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T06:39:29Z | nsc2.utdallas.edu | online | ok | ok | 55.80% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T06:39:29Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T06:39:29Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T06:45:01Z | nsc1.utdallas.edu | online | ok | ok | 40.70% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T06:45:01Z | nsc2.utdallas.edu | online | ok | ok | 55.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T06:45:01Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T06:45:01Z | nsc4.utdallas.edu | online | ok | ok | 1.30% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T06:50:38Z | nsc1.utdallas.edu | online | ok | ok | 35.60% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T06:50:38Z | nsc2.utdallas.edu | online | ok | ok | 56.00% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T06:50:38Z | nsc3.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T06:50:38Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T06:56:10Z | nsc1.utdallas.edu | online | ok | ok | 40.50% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T06:56:10Z | nsc2.utdallas.edu | online | ok | ok | 55.00% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T06:56:10Z | nsc3.utdallas.edu | online | ok | ok | 100.00% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T06:56:10Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T07:01:46Z | nsc1.utdallas.edu | online | ok | ok | 18.30% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T07:01:46Z | nsc2.utdallas.edu | online | ok | ok | 56.20% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T07:01:46Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T07:01:46Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T07:07:22Z | nsc1.utdallas.edu | online | ok | ok | 40.40% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T07:07:22Z | nsc2.utdallas.edu | online | ok | ok | 56.70% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T07:07:22Z | nsc3.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T07:07:22Z | nsc4.utdallas.edu | online | ok | ok | 0.90% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T07:12:59Z | nsc1.utdallas.edu | online | ok | ok | 40.50% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T07:12:59Z | nsc2.utdallas.edu | online | ok | ok | 56.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T07:12:59Z | nsc3.utdallas.edu | online | ok | ok | 100.00% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T07:12:59Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T07:18:35Z | nsc1.utdallas.edu | online | ok | ok | 30.40% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T07:18:35Z | nsc2.utdallas.edu | online | ok | ok | 57.20% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T07:18:35Z | nsc3.utdallas.edu | online | ok | ok | 100.00% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T07:18:35Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-24T07:24:08Z | nsc1.utdallas.edu | online | ok | ok | 40.60% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-24T07:24:08Z | nsc2.utdallas.edu | online | ok | ok | 57.10% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-24T07:24:08Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-24T07:24:08Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |

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
