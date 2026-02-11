# Server Status Dashboard

Updated: **2026-02-11T15:55:27Z**

## Current Fleet Status

| Server | Ping | CUDA | Mumax3 | CPU util. | GPU util. | CPU(logical/physical) | GPU count |
| ------ | ---- | ---- | ------ | --------- | --------- | -------------------- | --------- |
| nsc1.utdallas.edu | :x: offline | :grey_question: unknown | :grey_question: unknown | NA | NA | NA/NA | NA |
| nsc2.utdallas.edu | :x: offline | :grey_question: unknown | :grey_question: unknown | NA | NA | NA/NA | NA |
| nsc3.utdallas.edu | :x: offline | :grey_question: unknown | :grey_question: unknown | NA | NA | NA/NA | NA |
| nsc4.utdallas.edu | :x: offline | :grey_question: unknown | :grey_question: unknown | NA | NA | NA/NA | NA |

## Hardware Inventory (latest known)

| Server | Logical CPUs | Physical CPUs | GPU count | GPU model(s) | RAM total (GB) |
| ------ | ------------ | ------------- | --------- | ------------ | -------------- |
| nsc1.utdallas.edu | NA | NA | NA | NA | NA |
| nsc2.utdallas.edu | NA | NA | NA | NA | NA |
| nsc3.utdallas.edu | NA | NA | NA | NA | NA |
| nsc4.utdallas.edu | NA | NA | NA | NA | NA |

## Reliability & Utilization (all samples)

| Server | Samples | Ping uptime | CUDA healthy | Mumax3 healthy | Avg CPU util. | Avg GPU util. | CPU>85% samples | GPU>90% samples |
| ------ | ------- | ----------- | ------------ | -------------- | ------------- | ------------- | --------------- | --------------- |
| nsc1.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA | 0 | 0 |
| nsc2.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA | 0 | 0 |
| nsc3.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA | 0 | 0 |
| nsc4.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA | 0 | 0 |

## SLO Rollups

| Server | Window | Ping uptime | CUDA healthy | Mumax3 healthy |
| ------ | ------ | ----------- | ------------ | -------------- |
| nsc1.utdallas.edu | 24h | 0.00% | 0.00% | 0.00% |
| nsc1.utdallas.edu | 7d | 0.00% | 0.00% | 0.00% |
| nsc1.utdallas.edu | 30d | 0.00% | 0.00% | 0.00% |
| nsc2.utdallas.edu | 24h | 0.00% | 0.00% | 0.00% |
| nsc2.utdallas.edu | 7d | 0.00% | 0.00% | 0.00% |
| nsc2.utdallas.edu | 30d | 0.00% | 0.00% | 0.00% |
| nsc3.utdallas.edu | 24h | 0.00% | 0.00% | 0.00% |
| nsc3.utdallas.edu | 7d | 0.00% | 0.00% | 0.00% |
| nsc3.utdallas.edu | 30d | 0.00% | 0.00% | 0.00% |
| nsc4.utdallas.edu | 24h | 0.00% | 0.00% | 0.00% |
| nsc4.utdallas.edu | 7d | 0.00% | 0.00% | 0.00% |
| nsc4.utdallas.edu | 30d | 0.00% | 0.00% | 0.00% |

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
| 2026-02-11T15:54:57Z | nsc1.utdallas.edu | offline | unknown | unknown | NA | NA | NA/NA | NA | NA |
| 2026-02-11T15:54:57Z | nsc2.utdallas.edu | offline | unknown | unknown | NA | NA | NA/NA | NA | NA |
| 2026-02-11T15:54:57Z | nsc3.utdallas.edu | offline | unknown | unknown | NA | NA | NA/NA | NA | NA |
| 2026-02-11T15:54:57Z | nsc4.utdallas.edu | offline | unknown | unknown | NA | NA | NA/NA | NA | NA |
| 2026-02-11T15:55:27Z | nsc1.utdallas.edu | offline | unknown | unknown | NA | NA | NA/NA | NA | NA |
| 2026-02-11T15:55:27Z | nsc2.utdallas.edu | offline | unknown | unknown | NA | NA | NA/NA | NA | NA |
| 2026-02-11T15:55:27Z | nsc3.utdallas.edu | offline | unknown | unknown | NA | NA | NA/NA | NA | NA |
| 2026-02-11T15:55:27Z | nsc4.utdallas.edu | offline | unknown | unknown | NA | NA | NA/NA | NA | NA |

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
