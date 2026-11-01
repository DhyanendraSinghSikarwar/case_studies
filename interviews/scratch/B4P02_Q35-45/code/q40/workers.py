"""Q40: pick a worker count from the CONTAINER CPU limit, not the host core count.
Run: python3 -I workers.py"""
import math, os

def cpu_limit():
    """cgroup v2 cpu.max looks like 'max 100000' (no limit) or '200000 100000' (= 2 CPUs)."""
    try:
        quota, period = open("/sys/fs/cgroup/cpu.max").read().split()
        if quota != "max":
            return int(quota) / int(period)
    except (FileNotFoundError, ValueError):
        pass
    return float(len(os.sched_getaffinity(0)))            # fallback: CPUs this process may use

def workers(cpus, model_mb, mem_limit_mb, shared_fraction=0.0):
    by_cpu = max(1, math.floor(cpus))
    # memory per extra worker: private part of the model plus ~ nothing for shared pages
    per_worker = model_mb * (1 - shared_fraction)
    by_mem = max(1, int((mem_limit_mb - model_mb) // max(per_worker, 1)) + 1)
    return min(by_cpu, by_mem), by_cpu, by_mem

print("detected CPU limit:", cpu_limit())
for cpus, model, mem, shared in [(2, 800, 4096, 0.0), (8, 800, 4096, 0.0), (8, 800, 4096, 0.9)]:
    w, c, m = workers(cpus, model, mem, shared)
    print(f"cpus={cpus} model={model}MB mem_limit={mem}MB shared={shared:.0%} -> by_cpu={c} by_mem={m} -> use {w}")
