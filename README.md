# Server Status Dashboard

Updated: **2026-02-13T02:41:06Z**

## Current Fleet Status

| Server | Ping | CUDA | Mumax3 | CPU util. | GPU util. | CPU(logical/physical) | GPU count |
| ------ | ---- | ---- | ------ | --------- | --------- | -------------------- | --------- |
| nsc1.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 0.40% | 0.00% | 38/20 | 1 |
| nsc2.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 0.60% | 0.00% | 16/8 | 1 |
| nsc3.utdallas.edu | :white_check_mark: online | :x: error | :x: error | 0.20% | NA | 24/12 | 2 |
| nsc4.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 0.40% | 0.00% | 24/12 | 2 |

## Hardware Inventory (latest known)

| Server | Logical CPUs | Physical CPUs | GPU count | GPU model(s) | RAM total (GB) |
| ------ | ------------ | ------------- | --------- | ------------ | -------------- |
| nsc1.utdallas.edu | 38 | 20 | 1 | Tesla P100-PCIE-16GB | 125.16 |
| nsc2.utdallas.edu | 16 | 8 | 1 | NVIDIA GeForce GTX 1080 Ti | 31.02 |
| nsc3.utdallas.edu | 24 | 12 | 2 | Failed to initialize NVML: Driver/library version mismatch;NVML library version: 590.48 | 31.01 |
| nsc4.utdallas.edu | 24 | 12 | 2 | NVIDIA GeForce RTX 2080 Ti;NVIDIA GeForce RTX 2080 Ti | 30.96 |

## Reliability & Utilization (all samples)

| Server | Samples | Ping uptime | CUDA healthy | Mumax3 healthy | Avg CPU util. | Avg GPU util. | CPU>85% samples | GPU>90% samples |
| ------ | ------- | ----------- | ------------ | -------------- | ------------- | ------------- | --------------- | --------------- |
| nsc1.utdallas.edu | 375 | 100.00% | 100.00% | 100.00% | 4.60% | 0.45% | 16 | 0 |
| nsc2.utdallas.edu | 376 | 100.00% | 100.00% | 100.00% | 13.87% | 0.00% | 50 | 0 |
| nsc3.utdallas.edu | 376 | 100.00% | 0.00% | 0.00% | 22.66% | NA | 84 | 0 |
| nsc4.utdallas.edu | 376 | 100.00% | 100.00% | 100.00% | 0.68% | 0.00% | 0 | 0 |

## SLO Rollups

| Server | Window | Ping uptime | CUDA healthy | Mumax3 healthy |
| ------ | ------ | ----------- | ------------ | -------------- |
| nsc1.utdallas.edu | 24h | 100.00% | 100.00% | 100.00% |
| nsc1.utdallas.edu | 7d | 100.00% | 100.00% | 100.00% |
| nsc1.utdallas.edu | 30d | 100.00% | 100.00% | 100.00% |
| nsc2.utdallas.edu | 24h | 100.00% | 100.00% | 100.00% |
| nsc2.utdallas.edu | 7d | 100.00% | 100.00% | 100.00% |
| nsc2.utdallas.edu | 30d | 100.00% | 100.00% | 100.00% |
| nsc3.utdallas.edu | 24h | 100.00% | 0.00% | 0.00% |
| nsc3.utdallas.edu | 7d | 100.00% | 0.00% | 0.00% |
| nsc3.utdallas.edu | 30d | 100.00% | 0.00% | 0.00% |
| nsc4.utdallas.edu | 24h | 100.00% | 100.00% | 100.00% |
| nsc4.utdallas.edu | 7d | 100.00% | 100.00% | 100.00% |
| nsc4.utdallas.edu | 30d | 100.00% | 100.00% | 100.00% |

## Incidents & State Changes (latest 25 transitions)

| Timestamp (UTC) | Server | Signal | Transition |
| --------------- | ------ | ------ | ---------- |

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
| 2026-02-13T01:26:12Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-13T01:26:12Z | nsc3.utdallas.edu | online | error | error | 2.60% | NA | 24/12 | 2 | 31.01 |
| 2026-02-13T01:26:12Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-13T01:31:33Z | nsc1.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-13T01:31:33Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-13T01:31:33Z | nsc3.utdallas.edu | online | error | error | 0.40% | NA | 24/12 | 2 | 31.01 |
| 2026-02-13T01:31:33Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-13T01:36:56Z | nsc1.utdallas.edu | online | ok | ok | 0.10% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-13T01:36:56Z | nsc2.utdallas.edu | online | ok | ok | 0.90% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-13T01:36:56Z | nsc3.utdallas.edu | online | error | error | 0.60% | NA | 24/12 | 2 | 31.01 |
| 2026-02-13T01:36:56Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-13T01:42:19Z | nsc1.utdallas.edu | online | ok | ok | 100.00% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-13T01:42:19Z | nsc2.utdallas.edu | online | ok | ok | 100.00% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-13T01:42:19Z | nsc3.utdallas.edu | online | error | error | 0.20% | NA | 24/12 | 2 | 31.01 |
| 2026-02-13T01:42:19Z | nsc4.utdallas.edu | online | ok | ok | 3.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-13T01:47:40Z | nsc1.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-13T01:47:40Z | nsc2.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-13T01:47:40Z | nsc3.utdallas.edu | online | error | error | 100.00% | NA | 24/12 | 2 | 31.01 |
| 2026-02-13T01:47:40Z | nsc4.utdallas.edu | online | ok | ok | 0.80% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-13T01:53:02Z | nsc1.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-13T01:53:02Z | nsc2.utdallas.edu | online | ok | ok | 6.40% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-13T01:53:02Z | nsc3.utdallas.edu | online | error | error | 0.80% | NA | 24/12 | 2 | 31.01 |
| 2026-02-13T01:53:02Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-13T01:58:24Z | nsc1.utdallas.edu | online | ok | ok | 0.10% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-13T01:58:24Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-13T01:58:24Z | nsc3.utdallas.edu | online | error | error | 0.40% | NA | 24/12 | 2 | 31.01 |
| 2026-02-13T01:58:24Z | nsc4.utdallas.edu | online | ok | ok | 0.80% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-13T02:03:44Z | nsc1.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-13T02:03:44Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-13T02:03:44Z | nsc3.utdallas.edu | online | error | error | 100.00% | NA | 24/12 | 2 | 31.01 |
| 2026-02-13T02:03:44Z | nsc4.utdallas.edu | online | ok | ok | 1.90% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-13T02:09:06Z | nsc1.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-13T02:09:06Z | nsc2.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-13T02:09:06Z | nsc3.utdallas.edu | online | error | error | 100.00% | NA | 24/12 | 2 | 31.01 |
| 2026-02-13T02:09:06Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-13T02:14:24Z | nsc1.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-13T02:14:24Z | nsc2.utdallas.edu | online | ok | ok | 1.20% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-13T02:14:24Z | nsc3.utdallas.edu | online | error | error | 0.40% | NA | 24/12 | 2 | 31.01 |
| 2026-02-13T02:14:24Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-13T02:19:42Z | nsc1.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-13T02:19:42Z | nsc2.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-13T02:19:42Z | nsc3.utdallas.edu | online | error | error | 0.80% | NA | 24/12 | 2 | 31.01 |
| 2026-02-13T02:19:42Z | nsc4.utdallas.edu | online | ok | ok | 0.80% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-13T02:25:04Z | nsc1.utdallas.edu | online | ok | ok | 0.10% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-13T02:25:04Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-13T02:25:04Z | nsc3.utdallas.edu | online | error | error | 0.20% | NA | 24/12 | 2 | 31.01 |
| 2026-02-13T02:25:04Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-13T02:30:25Z | nsc1.utdallas.edu | online | ok | ok | 0.50% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-13T02:30:25Z | nsc2.utdallas.edu | online | ok | ok | 0.90% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-13T02:30:25Z | nsc3.utdallas.edu | online | error | error | 0.60% | NA | 24/12 | 2 | 31.01 |
| 2026-02-13T02:30:25Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-13T02:35:45Z | nsc1.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-13T02:35:45Z | nsc2.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-13T02:35:45Z | nsc3.utdallas.edu | online | error | error | 100.00% | NA | 24/12 | 2 | 31.01 |
| 2026-02-13T02:35:45Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-13T02:41:06Z | nsc1.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-13T02:41:06Z | nsc2.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-13T02:41:06Z | nsc3.utdallas.edu | online | error | error | 0.20% | NA | 24/12 | 2 | 31.01 |
| 2026-02-13T02:41:06Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |

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
