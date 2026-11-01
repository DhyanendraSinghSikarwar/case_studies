"""Scale-up / scale-down decisions of a GPU node pool, one tick = 1 minute. Made-up round numbers.
A model of the usual Cluster Autoscaler rules, NOT its code. Real defaults and flags: check current docs."""
import math

GPUS_PER_NODE, POOL_MAX, POOL_MIN = 4, 3, 0
READY_AFTER = 3 + 2 + 5        # minutes: instance start + driver/device plugin + image pull (made up)
UNNEEDED_FOR, UTIL_BELOW = 10, 0.5   # node must look removable for 10 min; 'low use' = under 50% of GPUs

nodes, pods, n_counter, node_minutes, warned = {}, {}, 0, 0, set()

def add_pod(name, gpus, kind, **flags):
    pods[name] = dict(gpus=gpus, kind=kind, node=None, **flags)

EVENTS = {
    0:  lambda: [add_pod("train-A", 4, "job", no_evict=True), add_pod("serve-B", 2, "deploy"), add_pod("serve-C", 2, "deploy")],
    40: lambda: add_pod("notebook-E", 1, "bare"),
    60: lambda: pods.pop("train-A"),                      # training finished
    80: lambda: [pods.pop("serve-B"), pods.pop("serve-C")],
}

def used(n): return sum(p["gpus"] for p in pods.values() if p["node"] == n)

def blockers(n):
    out = []
    for name, p in pods.items():
        if p["node"] != n: continue
        if p["kind"] == "bare": out.append(f"{name}: no controller (cannot be recreated elsewhere)")
        if p.get("no_evict"): out.append(f"{name}: safe-to-evict=false")
    return out

for t in range(121):
    if t in EVENTS: EVENTS[t]()
    # 1. place pending pods on READY nodes with room (first fit)
    for name, p in pods.items():
        if p["node"] is None:
            for n, nd in nodes.items():
                if nd["ready_at"] <= t and GPUS_PER_NODE - used(n) >= p["gpus"]:
                    p["node"] = n; print(f"t={t:3} {name} placed on {n}"); break
    # 2. scale up: pending pods that fit on no ready OR starting node need new nodes (first-fit decreasing)
    pending = sorted((p["gpus"], nm) for nm, p in pods.items() if p["node"] is None)[::-1]
    free = [GPUS_PER_NODE - used(n) for n, nd in nodes.items()]       # ready or starting, current free
    for g, nm in pending:
        for i, f in enumerate(free):
            if f >= g: free[i] -= g; break
        else:
            if len(nodes) < POOL_MAX:
                n_counter += 1; n = f"gpu-node-{n_counter}"
                nodes[n] = dict(ready_at=t + READY_AFTER, unneeded=None)
                free.append(GPUS_PER_NODE - g)
                print(f"t={t:3} scale UP: {nm} ({g} GPU) is Pending and fits no node -> {n}, ready at t={t + READY_AFTER}")
            else:
                print(f"t={t:3} {nm} stays Pending: pool at max {POOL_MAX}")
    # 3. scale down
    for n, nd in list(nodes.items()):
        if nd["ready_at"] > t: continue
        util = used(n) / GPUS_PER_NODE
        if util >= UTIL_BELOW or len(nodes) <= POOL_MIN:
            nd["unneeded"] = None; continue
        b = blockers(n)
        if b:
            key = (n, tuple(b))
            if key not in warned: warned.add(key); print(f"t={t:3} {n} util {util:.0%} but NOT removable: {b}")
            nd["unneeded"] = None; continue
        if nd["unneeded"] is None:
            nd["unneeded"] = t; print(f"t={t:3} {n} util {util:.0%}, marked unneeded")
        elif t - nd["unneeded"] >= UNNEEDED_FOR:
            print(f"t={t:3} scale DOWN: removing {n} (unneeded for {t - nd['unneeded']} min)")
            for p in pods.values():
                if p["node"] == n: p["node"] = None       # would be evicted and rescheduled (none here)
            del nodes[n]
    node_minutes += len(nodes)

print(f"\nnodes at t=120: {sorted(nodes)}   billed node-minutes: {node_minutes}   (3 static nodes for 120 min = {3 * 120})")
print(f"still held by a bare pod: {[n for n in nodes if any(p['kind'] == 'bare' and p['node'] == n for p in pods.values())]}")
