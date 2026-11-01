"""Tell cgroup OOM kill from node-pressure eviction, and size a memory limit."""
import json, math, sys

def classify(pod):
    st = pod["status"]
    if st.get("reason") == "Evicted":
        return "node-eviction", "node ran low on memory; this pod was chosen. Check requests vs usage and node size."
    for cs in st.get("containerStatuses", []):
        t = cs.get("lastState", {}).get("terminated", {})
        if t.get("reason") == "OOMKilled":
            return "container-oom", "this container hit ITS OWN memory limit (exit 137). Raise limit or cut usage."
    return "healthy", "no memory kill seen"

def size_memory(samples_mib, headroom=0.25, req_pctl=0.95):
    s = sorted(samples_mib)
    p = s[min(len(s) - 1, math.ceil(req_pctl * len(s)) - 1)]
    peak = s[-1]
    request = math.ceil(p / 64) * 64                 # round up to 64 MiB
    limit = math.ceil(peak * (1 + headroom) / 64) * 64
    return {"p95": p, "peak": peak, "request": request, "limit": limit}

def python_footprint(model_mib, workers, preload_shared=False):
    # naive model: each worker loads its own copy unless weights are shared (copy-on-write, fragile in Python)
    return model_mib if preload_shared else model_mib * workers

if __name__ == "__main__":
    for pod in json.load(open(sys.argv[1])):
        k, why = classify(pod)
        print(f"{pod['name']}: {k:14s} {why}")
    # hand-checkable: 20 samples of working set in MiB
    samples = [1500] * 16 + [1600, 1650, 1700, 1800]
    print("sizing:", size_memory(samples))
    print("2048 MiB model x 4 workers  =", python_footprint(2048, 4), "MiB")
    print("2048 MiB model, shared once =", python_footprint(2048, 4, True), "MiB")
