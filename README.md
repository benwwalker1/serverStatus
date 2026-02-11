# Server Status Dashboard

Updated: **2026-02-11T15:20:48Z**

Interactive dashboard: [dashboard.html](./dashboard.html)

## Latest Check

| Server | Ping | CUDA | Mumax3 | CPU count | CPU util. | GPU count | GPU util. |
| ------ | ---- | ---- | ------ | --------- | --------- | --------- | --------- |
| nsc1.utdallas.edu | :x: (offline) | :grey_question: (unknown) | :grey_question: (unknown) | NA | NA | NA | NA |
| nsc2.utdallas.edu | :x: (offline) | :grey_question: (unknown) | :grey_question: (unknown) | NA | NA | NA | NA |
| nsc3.utdallas.edu | :x: (offline) | :grey_question: (unknown) | :grey_question: (unknown) | NA | NA | NA | NA |
| nsc4.utdallas.edu | :x: (offline) | :grey_question: (unknown) | :grey_question: (unknown) | NA | NA | NA | NA |

## Uptime over time windows

### 1 day uptime
| Server | Samples | Ping uptime | CUDA healthy | Mumax3 healthy | CPU avg util. | GPU avg util. |
| ------ | ------- | ----------- | ------------ | -------------- | ------------- | ------------- |
| nsc1.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA |
| nsc2.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA |
| nsc3.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA |
| nsc4.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA |

### 1 week uptime
| Server | Samples | Ping uptime | CUDA healthy | Mumax3 healthy | CPU avg util. | GPU avg util. |
| ------ | ------- | ----------- | ------------ | -------------- | ------------- | ------------- |
| nsc1.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA |
| nsc2.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA |
| nsc3.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA |
| nsc4.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA |

### 1 month uptime
| Server | Samples | Ping uptime | CUDA healthy | Mumax3 healthy | CPU avg util. | GPU avg util. |
| ------ | ------- | ----------- | ------------ | -------------- | ------------- | ------------- |
| nsc1.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA |
| nsc2.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA |
| nsc3.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA |
| nsc4.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA |

### 6 months uptime
| Server | Samples | Ping uptime | CUDA healthy | Mumax3 healthy | CPU avg util. | GPU avg util. |
| ------ | ------- | ----------- | ------------ | -------------- | ------------- | ------------- |
| nsc1.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA |
| nsc2.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA |
| nsc3.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA |
| nsc4.utdallas.edu | 2 | 0.00% | 0.00% | 0.00% | NA | NA |

## Recent Samples

<details>
<summary>Expand to view latest 60 samples</summary>

| Timestamp (UTC) | Server | Ping | CUDA | Mumax3 | CPU count | CPU util. | GPU count | GPU util. |
| --------------- | ------ | ---- | ---- | ------ | --------- | --------- | --------- | --------- |
| 2026-02-11T15:20:32Z | nsc1.utdallas.edu | offline | unknown | unknown | NA | NA | NA | NA |
| 2026-02-11T15:20:32Z | nsc2.utdallas.edu | offline | unknown | unknown | NA | NA | NA | NA |
| 2026-02-11T15:20:32Z | nsc3.utdallas.edu | offline | unknown | unknown | NA | NA | NA | NA |
| 2026-02-11T15:20:32Z | nsc4.utdallas.edu | offline | unknown | unknown | NA | NA | NA | NA |
| 2026-02-11T15:20:48Z | nsc1.utdallas.edu | offline | unknown | unknown | NA | NA | NA | NA |
| 2026-02-11T15:20:48Z | nsc2.utdallas.edu | offline | unknown | unknown | NA | NA | NA | NA |
| 2026-02-11T15:20:48Z | nsc3.utdallas.edu | offline | unknown | unknown | NA | NA | NA | NA |
| 2026-02-11T15:20:48Z | nsc4.utdallas.edu | offline | unknown | unknown | NA | NA | NA | NA |

</details>

## Definitions

- **Ping uptime**: percentage of samples in which ICMP ping succeeded.
- **CUDA healthy uptime**: percentage of samples in which `nvidia-smi` returned valid GPU utilization data.
- **Mumax3 healthy uptime**: percentage of samples in which `mumax3` command check succeeded.
- **CPU utilization**: average active CPU percentage computed from `/proc/stat` over ~0.5s during each sample.
- **GPU utilization**: mean `%utilization.gpu` across all GPUs reported by `nvidia-smi` at sample time.
- **CPU/GPU counts**: `nproc` for CPU logical cores, and number of GPUs returned by `nvidia-smi`.
