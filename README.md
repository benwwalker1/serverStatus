# Server Status Dashboard

Updated: **2026-02-12T23:44:19Z**

## Current Fleet Status

| Server | Ping | CUDA | Mumax3 | CPU util. | GPU util. | CPU(logical/physical) | GPU count |
| ------ | ---- | ---- | ------ | --------- | --------- | -------------------- | --------- |
| nsc1.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 0.30% | 0.00% | 38/20 | 1 |
| nsc2.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 0.30% | 0.00% | 16/8 | 1 |
| nsc3.utdallas.edu | :white_check_mark: online | :x: error | :x: error | 0.40% | NA | 24/12 | 2 |
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
| nsc1.utdallas.edu | 342 | 100.00% | 100.00% | 100.00% | 4.43% | 0.49% | 14 | 0 |
| nsc2.utdallas.edu | 343 | 100.00% | 100.00% | 100.00% | 14.27% | 0.00% | 47 | 0 |
| nsc3.utdallas.edu | 343 | 100.00% | 0.00% | 0.00% | 22.46% | NA | 76 | 0 |
| nsc4.utdallas.edu | 343 | 100.00% | 100.00% | 100.00% | 0.67% | 0.00% | 0 | 0 |

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
| 2026-02-12T22:22:52Z | nsc2.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-12T22:22:52Z | nsc3.utdallas.edu | online | error | error | 0.20% | NA | 24/12 | 2 | 31.01 |
| 2026-02-12T22:22:52Z | nsc4.utdallas.edu | online | ok | ok | 1.70% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-12T22:29:12Z | nsc1.utdallas.edu | online | ok | ok | 94.90% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-12T22:29:12Z | nsc2.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-12T22:29:12Z | nsc3.utdallas.edu | online | error | error | 0.40% | NA | 24/12 | 2 | 31.01 |
| 2026-02-12T22:29:12Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-12T22:35:34Z | nsc1.utdallas.edu | online | ok | ok | 95.00% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-12T22:35:34Z | nsc2.utdallas.edu | online | ok | ok | 1.50% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-12T22:35:34Z | nsc3.utdallas.edu | online | error | error | 0.20% | NA | 24/12 | 2 | 31.01 |
| 2026-02-12T22:35:34Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-12T22:41:49Z | nsc1.utdallas.edu | online | ok | ok | 95.10% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-12T22:41:49Z | nsc2.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-12T22:41:49Z | nsc3.utdallas.edu | online | error | error | 0.20% | NA | 24/12 | 2 | 31.01 |
| 2026-02-12T22:41:49Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-12T22:47:58Z | nsc1.utdallas.edu | online | ok | ok | 95.00% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-12T22:47:58Z | nsc2.utdallas.edu | online | ok | ok | 0.90% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-12T22:47:58Z | nsc3.utdallas.edu | online | error | error | 0.60% | NA | 24/12 | 2 | 31.01 |
| 2026-02-12T22:47:58Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-12T22:54:10Z | nsc1.utdallas.edu | online | ok | ok | 95.00% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-12T22:54:10Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-12T22:54:10Z | nsc3.utdallas.edu | online | error | error | 0.40% | NA | 24/12 | 2 | 31.01 |
| 2026-02-12T22:54:10Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-12T23:00:32Z | nsc1.utdallas.edu | online | ok | ok | 94.90% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-12T23:00:32Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-12T23:00:32Z | nsc3.utdallas.edu | online | error | error | 0.40% | NA | 24/12 | 2 | 31.01 |
| 2026-02-12T23:00:32Z | nsc4.utdallas.edu | online | ok | ok | 0.80% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-12T23:06:48Z | nsc1.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-12T23:06:48Z | nsc2.utdallas.edu | online | ok | ok | 100.00% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-12T23:06:48Z | nsc3.utdallas.edu | online | error | error | 0.20% | NA | 24/12 | 2 | 31.01 |
| 2026-02-12T23:06:48Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-12T23:12:12Z | nsc1.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-12T23:12:12Z | nsc2.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-12T23:12:12Z | nsc3.utdallas.edu | online | error | error | 100.00% | NA | 24/12 | 2 | 31.01 |
| 2026-02-12T23:12:12Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-12T23:17:31Z | nsc1.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-12T23:17:31Z | nsc2.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-12T23:17:31Z | nsc3.utdallas.edu | online | error | error | 100.00% | NA | 24/12 | 2 | 31.01 |
| 2026-02-12T23:17:31Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-12T23:22:53Z | nsc1.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-12T23:22:53Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-12T23:22:53Z | nsc3.utdallas.edu | online | error | error | 0.20% | NA | 24/12 | 2 | 31.01 |
| 2026-02-12T23:22:53Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-12T23:28:15Z | nsc1.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-12T23:28:15Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-12T23:28:15Z | nsc3.utdallas.edu | online | error | error | 0.20% | NA | 24/12 | 2 | 31.01 |
| 2026-02-12T23:28:15Z | nsc4.utdallas.edu | online | ok | ok | 0.80% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-12T23:33:38Z | nsc1.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-12T23:33:38Z | nsc2.utdallas.edu | online | ok | ok | 0.90% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-12T23:33:38Z | nsc3.utdallas.edu | online | error | error | 0.40% | NA | 24/12 | 2 | 31.01 |
| 2026-02-12T23:33:38Z | nsc4.utdallas.edu | online | ok | ok | 0.80% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-12T23:38:58Z | nsc1.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-12T23:38:58Z | nsc2.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-12T23:38:58Z | nsc3.utdallas.edu | online | error | error | 0.20% | NA | 24/12 | 2 | 31.01 |
| 2026-02-12T23:38:58Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-12T23:44:19Z | nsc1.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-12T23:44:19Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-12T23:44:19Z | nsc3.utdallas.edu | online | error | error | 0.40% | NA | 24/12 | 2 | 31.01 |
| 2026-02-12T23:44:19Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |

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
