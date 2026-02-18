# Server Status Dashboard

Updated: **2026-02-18T22:11:59Z**

## Current Fleet Status

| Server | Ping | CUDA | Mumax3 | CPU util. | GPU util. | CPU(logical/physical) | GPU count |
| ------ | ---- | ---- | ------ | --------- | --------- | -------------------- | --------- |
| nsc1.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 2.90% | 0.00% | 38/20 | 1 |
| nsc2.utdallas.edu | :white_check_mark: online | :white_check_mark: ok | :white_check_mark: ok | 100.00% | 0.00% | 16/8 | 1 |
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
| nsc1.utdallas.edu | 1914 | 100.00% | 99.95% | 100.00% | 9.68% | 0.09% | 31 | 0 |
| nsc2.utdallas.edu | 1915 | 100.00% | 99.84% | 99.84% | 14.68% | 0.00% | 269 | 0 |
| nsc3.utdallas.edu | 1915 | 100.00% | 78.17% | 78.17% | 19.76% | 0.00% | 363 | 0 |
| nsc4.utdallas.edu | 1915 | 100.00% | 100.00% | 100.00% | 0.66% | 0.00% | 0 | 0 |

## SLO Rollups

| Server | Window | Ping uptime | CUDA healthy | Mumax3 healthy |
| ------ | ------ | ----------- | ------------ | -------------- |
| nsc1.utdallas.edu | 24h | 100.00% | 100.00% | 100.00% |
| nsc1.utdallas.edu | 7d | 100.00% | 99.95% | 100.00% |
| nsc1.utdallas.edu | 30d | 100.00% | 99.95% | 100.00% |
| nsc2.utdallas.edu | 24h | 100.00% | 100.00% | 100.00% |
| nsc2.utdallas.edu | 7d | 100.00% | 99.84% | 99.84% |
| nsc2.utdallas.edu | 30d | 100.00% | 99.84% | 99.84% |
| nsc3.utdallas.edu | 24h | 100.00% | 100.00% | 100.00% |
| nsc3.utdallas.edu | 7d | 100.00% | 80.79% | 80.79% |
| nsc3.utdallas.edu | 30d | 100.00% | 78.17% | 78.17% |
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
| 2026-02-18T20:54:54Z | nsc2.utdallas.edu | online | ok | ok | 0.90% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-18T20:54:54Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-18T20:54:54Z | nsc4.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-18T21:00:22Z | nsc1.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-18T21:00:22Z | nsc2.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-18T21:00:22Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-18T21:00:22Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-18T21:05:49Z | nsc1.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-18T21:05:49Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-18T21:05:49Z | nsc3.utdallas.edu | online | ok | ok | 4.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-18T21:05:49Z | nsc4.utdallas.edu | online | ok | ok | 0.80% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-18T21:11:07Z | nsc1.utdallas.edu | online | ok | ok | 0.10% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-18T21:11:07Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-18T21:11:07Z | nsc3.utdallas.edu | online | ok | ok | 4.60% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-18T21:11:07Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-18T21:16:31Z | nsc1.utdallas.edu | online | ok | ok | 7.70% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-18T21:16:31Z | nsc2.utdallas.edu | online | ok | ok | 6.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-18T21:16:31Z | nsc3.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-18T21:16:31Z | nsc4.utdallas.edu | online | ok | ok | 0.80% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-18T21:21:59Z | nsc1.utdallas.edu | online | ok | ok | 18.10% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-18T21:21:59Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-18T21:21:59Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-18T21:21:59Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-18T21:27:29Z | nsc1.utdallas.edu | online | ok | ok | 17.80% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-18T21:27:29Z | nsc2.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-18T21:27:29Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-18T21:27:29Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-18T21:33:01Z | nsc1.utdallas.edu | online | ok | ok | 15.40% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-18T21:33:01Z | nsc2.utdallas.edu | online | ok | ok | 0.30% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-18T21:33:01Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-18T21:33:01Z | nsc4.utdallas.edu | online | ok | ok | 0.80% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-18T21:38:32Z | nsc1.utdallas.edu | online | ok | ok | 15.20% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-18T21:38:32Z | nsc2.utdallas.edu | online | ok | ok | 0.90% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-18T21:38:32Z | nsc3.utdallas.edu | online | ok | ok | 12.70% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-18T21:38:32Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-18T21:44:04Z | nsc1.utdallas.edu | online | ok | ok | 12.80% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-18T21:44:04Z | nsc2.utdallas.edu | online | ok | ok | 100.00% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-18T21:44:04Z | nsc3.utdallas.edu | online | ok | ok | 12.90% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-18T21:44:04Z | nsc4.utdallas.edu | online | ok | ok | 1.00% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-18T21:49:41Z | nsc1.utdallas.edu | online | ok | ok | 10.30% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-18T21:49:41Z | nsc2.utdallas.edu | online | ok | ok | 0.90% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-18T21:49:41Z | nsc3.utdallas.edu | online | ok | ok | 16.70% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-18T21:49:41Z | nsc4.utdallas.edu | online | ok | ok | 1.10% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-18T21:55:07Z | nsc1.utdallas.edu | online | ok | ok | 5.40% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-18T21:55:07Z | nsc2.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-18T21:55:07Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-18T21:55:07Z | nsc4.utdallas.edu | online | ok | ok | 0.60% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-18T22:00:41Z | nsc1.utdallas.edu | online | ok | ok | 5.40% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-18T22:00:41Z | nsc2.utdallas.edu | online | ok | ok | 0.90% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-18T22:00:41Z | nsc3.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-18T22:00:41Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-18T22:06:23Z | nsc1.utdallas.edu | online | ok | ok | 2.80% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-18T22:06:23Z | nsc2.utdallas.edu | online | ok | ok | 0.90% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-18T22:06:23Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-18T22:06:23Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |
| 2026-02-18T22:11:59Z | nsc1.utdallas.edu | online | ok | ok | 2.90% | 0.00% | 38/20 | 1 | 125.16 |
| 2026-02-18T22:11:59Z | nsc2.utdallas.edu | online | ok | ok | 100.00% | 0.00% | 16/8 | 1 | 31.02 |
| 2026-02-18T22:11:59Z | nsc3.utdallas.edu | online | ok | ok | 0.20% | 0.00% | 24/12 | 2 | 31.01 |
| 2026-02-18T22:11:59Z | nsc4.utdallas.edu | online | ok | ok | 0.40% | 0.00% | 24/12 | 2 | 30.96 |

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
