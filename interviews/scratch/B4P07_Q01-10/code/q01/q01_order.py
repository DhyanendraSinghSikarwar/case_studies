import sys, graphlib, yaml
wf = yaml.safe_load(open(sys.argv[1]))
print("top-level keys:", list(wf))            # note: 'on' is parsed as True
jobs = wf["jobs"]
deps = {}
for name, j in jobs.items():
    n = j.get("needs", [])
    deps[name] = [n] if isinstance(n, str) else list(n)
order = list(graphlib.TopologicalSorter(deps).static_order())
for i, j in enumerate(order, 1):
    print(i, j, "<-", deps[j] or "-")
ts = graphlib.TopologicalSorter(deps); ts.prepare()
wave = 0
while ts.is_active():
    ready = sorted(ts.get_ready()); wave += 1
    print("wave", wave, "runs in parallel:", ready)
    ts.done(*ready)
