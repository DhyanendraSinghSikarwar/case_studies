"""Why is my GPU pod Pending? Offline model of a few scheduler filters on a made-up node inventory."""
from collections import Counter

NODES = {
  "gpu-a":   {"labels": {"pool": "gpu"}, "taints": [("nvidia.com/gpu", "NoSchedule")],   "alloc": {"nvidia.com/gpu": 8}, "used": {"nvidia.com/gpu": 6}},
  "gpu-b":   {"labels": {"pool": "gpu"}, "taints": [("nvidia.com/gpu", "NoSchedule")],   "alloc": {"nvidia.com/gpu": 4}, "used": {"nvidia.com/gpu": 2}},
  "gpu-c":   {"labels": {"pool": "gpu"}, "taints": [("nvidia.com/gpu", "NoSchedule")],   "alloc": {"nvidia.com/gpu": 4}, "used": {"nvidia.com/gpu": 2}},
  "gpu-d":   {"labels": {"pool": "gpu"}, "taints": [("nvidia.com/gpu", "NoSchedule")],   "alloc": {}, "used": {}},   # device plugin down: no GPU advertised
  "mig-e":   {"labels": {"pool": "gpu"}, "taints": [("nvidia.com/gpu", "NoSchedule")],   "alloc": {"nvidia.com/mig-1g.10gb": 7}, "used": {}},
  "cpu-f":   {"labels": {"pool": "cpu"}, "taints": [],                                    "alloc": {}, "used": {}},
  "train-g": {"labels": {"pool": "gpu"}, "taints": [("dedicated=training", "NoSchedule")], "alloc": {"nvidia.com/gpu": 8}, "used": {}},
}
RUNNING = [  # who holds GPUs on gpu-a, with a made-up utilisation sample (percent, last 3 days)
  {"pod": "notebook-ravi", "node": "gpu-a", "gpus": 2, "util": 0},
  {"pod": "train-bert",    "node": "gpu-a", "gpus": 4, "util": 93},
]
POD = {"name": "train-big", "request": {"nvidia.com/gpu": 4}, "selector": {"pool": "gpu"},
       "tolerates": [("nvidia.com/gpu", "NoSchedule")]}

def reason(pod, n):
    if any(n["labels"].get(k) != v for k, v in pod["selector"].items()):
        return "node(s) didn't match Pod's node selector"
    for t in n["taints"]:
        if t not in pod["tolerates"]:
            return f"node(s) had untolerated taint {{{t[0]}}}"
    for res, need in pod["request"].items():
        if res not in n["alloc"]:
            return f"Insufficient {res} (node does not advertise it)"
        if n["alloc"][res] - n["used"].get(res, 0) < need:
            return f"Insufficient {res}"
    return None

def explain(pod, nodes=NODES):
    reasons = {name: reason(pod, n) for name, n in nodes.items()}
    fits = [k for k, v in reasons.items() if v is None]
    print(f"pod {pod['name']} wants {pod['request']}")
    for name, r in reasons.items():
        print(f"  {name:8} {r or 'FITS'}")
    if fits:
        print("  -> schedulable on", fits)
        return
    c = Counter(reasons.values())
    print(f"  event: 0/{len(nodes)} nodes are available: " + ", ".join(f"{n} {r}" for r, n in c.items()) + ".")
    # fragmentation: only nodes that pass the non-resource filters count
    res = next(iter(pod["request"]))
    eligible = {k: n for k, n in nodes.items()
                if not (reasons[k] or "").startswith(("node(s) didn't", "node(s) had"))}
    free = {k: n["alloc"].get(res, 0) - n["used"].get(res, 0) for k, n in eligible.items() if res in n["alloc"]}
    need = pod["request"][res]
    print(f"  free {res} on eligible nodes: {free}  total={sum(free.values())} largest block={max(free.values(), default=0)} need={need}")
    if sum(free.values()) >= need > max(free.values(), default=0):
        print("  -> FRAGMENTATION: enough GPUs in total, never enough on ONE node")

explain(POD)
print()
print("idle-but-held GPUs:", [(r["pod"], r["node"], r["gpus"]) for r in RUNNING if r["util"] < 5])
print()
explain({**POD, "name": "serve-small", "request": {"nvidia.com/gpu": 2}})
