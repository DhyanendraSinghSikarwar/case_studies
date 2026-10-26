"""Toy control plane: a store (etcd), controllers that only talk to the store, a scheduler and a kubelet.
Teaching model of the flow, not Kubernetes code."""
import itertools

class Store:                      # stands in for API server + etcd
    def __init__(self): self.objs, self.up, self.n = {}, True, itertools.count(1)
    def put(self, key, obj):
        if not self.up: raise ConnectionError("etcd down: write rejected")
        self.objs[key] = obj
    def delete(self, key):
        if not self.up: raise ConnectionError("etcd down: write rejected")
        self.objs.pop(key, None)
    def pods(self): return {k: v for k, v in self.objs.items() if k.startswith("pod/")}

def deployment_controller(s):     # Deployment -> ReplicaSet
    d = s.objs["deploy/scorer"]
    if "rs/scorer-abc" not in s.objs:
        s.put("rs/scorer-abc", {"replicas": d["replicas"]}); print("  deployment-ctl: created ReplicaSet scorer-abc")
    elif s.objs["rs/scorer-abc"]["replicas"] != d["replicas"]:
        s.put("rs/scorer-abc", {"replicas": d["replicas"]}); print(f"  deployment-ctl: ReplicaSet now wants {d['replicas']}")

def replicaset_controller(s):     # ReplicaSet -> Pods (desired vs actual)
    want = s.objs["rs/scorer-abc"]["replicas"]
    have = s.pods()
    for _ in range(want - len(have)):
        name = f"pod/scorer-abc-{next(s.n)}"
        s.put(name, {"node": None, "phase": "Pending"}); print(f"  replicaset-ctl: have {len(have)}, want {want} -> created {name}")
        have = s.pods()
    for name in list(have)[want:]:
        s.delete(name); print(f"  replicaset-ctl: too many -> deleted {name}")

def scheduler(s, nodes=("node-1", "node-2")):   # binds Pending pods to a node
    for name, p in s.pods().items():
        if p["node"] is None:
            p["node"] = nodes[int(name.rsplit("-", 1)[1]) % len(nodes)]
            s.put(name, p); print(f"  scheduler: bound {name} -> {p['node']}")

def kubelet(s):                   # starts containers for pods bound to its node
    for name, p in s.pods().items():
        if p["node"] and p["phase"] == "Pending":
            p["phase"] = "Running"; s.put(name, p); print(f"  kubelet({p['node']}): started {name}")

def tick(s, label, sched=True):
    print(f"[{label}]")
    try:
        deployment_controller(s); replicaset_controller(s)
        if sched: scheduler(s)
        kubelet(s)
    except ConnectionError as e:
        print("  ERROR:", e)
    ph = sorted((k.split("-")[-1], v["phase"]) for k, v in s.pods().items())
    print("  state:", ph)

s = Store()
s.put("deploy/scorer", {"replicas": 3})                    # what `kubectl apply` stores
tick(s, "apply: 3 replicas")
victim = next(iter(s.pods())); s.objs.pop(victim)           # a node loses a pod behind the API's back
print(f"\n-- {victim} vanished --")
tick(s, "self-heal")
s.objs["deploy/scorer"]["replicas"] = 5
tick(s, "scale to 5, scheduler DOWN", sched=False)
tick(s, "scheduler back")
s.up = False
s.objs["deploy/scorer"]["replicas"] = 6
tick(s, "etcd DOWN, try to scale to 6")
print("running pods still serving:", sum(p["phase"] == "Running" for p in s.pods().values()))
