"""Can N replicas be placed given a node->zone map? Simplified scheduler model:
 - topology spread over zones (maxSkew, DoNotSchedule): after placing, count(zone) - min(count over all zones) <= maxSkew
 - optional HARD pod anti-affinity per node: at most one pod per node
 - each node has a slot limit (max pods of this app). Pods are placed one by one."""
def place(nodes, replicas, max_skew=1, hard_anti_affinity=False, slots=2):
    zones = sorted(set(nodes.values()))
    per_node = {n: 0 for n in nodes}
    per_zone = {z: 0 for z in zones}
    placed, pending = [], 0
    for i in range(replicas):
        ok = []
        for n, z in nodes.items():
            if hard_anti_affinity and per_node[n] >= 1: continue
            if per_node[n] >= slots: continue
            new = dict(per_zone); new[z] += 1
            if new[z] - min(new.values()) > max_skew: continue
            ok.append((per_zone[z], per_node[n], n))
        if not ok:
            pending += 1; continue
        _, _, n = min(ok)                       # prefer emptier zone, then emptier node
        per_node[n] += 1; per_zone[nodes[n]] += 1; placed.append(n)
    return placed, per_zone, pending

def show(title, nodes, replicas, **kw):
    placed, per_zone, pending = place(nodes, replicas, **kw)
    print(f"{title}\n  placed on {placed}\n  per zone {per_zone}  Pending pods: {pending}")

three_zones = {"n1": "a", "n2": "b", "n3": "c"}
show("A) 3 nodes in 3 zones, 3 replicas, skew 1", three_zones, 3)
show("B) 3 replicas, 2 nodes in same zone a, one node in b (zone c has NO nodes)", {"n1": "a", "n2": "a", "n3": "b"}, 3)
show("C) 3 replicas, HARD anti-affinity, only 2 nodes", {"n1": "a", "n2": "b"}, 3, hard_anti_affinity=True)
show("D) rolling update: 4 pods (3 + 1 surge), HARD anti-affinity, 3 nodes", three_zones, 4, hard_anti_affinity=True)
show("E) 4 replicas, 3 nodes in zone a, 1 node in zone b, 1 slot per node, skew 1, DoNotSchedule", {"n1": "a", "n2": "a", "n3": "a", "n4": "b"}, 4, slots=1)
