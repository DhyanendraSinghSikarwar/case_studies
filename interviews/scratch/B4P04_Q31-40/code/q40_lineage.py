"""OpenLineage-style events (field names follow the public spec as I know it; check the spec for your version)
and a walk from a dataset to every downstream model. Pure Python, no lineage server."""
import json
from collections import defaultdict, deque

def event(job, run_id, inputs, outputs, ts):
    return {"eventType": "COMPLETE", "eventTime": ts,
            "run": {"runId": run_id},
            "job": {"namespace": "prod-airflow", "name": job},
            "inputs": [{"namespace": "wh", "name": n} for n in inputs],
            "outputs": [{"namespace": "wh" if not o.startswith("model:") else "mlflow", "name": o} for o in outputs],
            "producer": "https://example.invalid/my-scheduler", "schemaURL": "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/RunEvent"}

events = [
    event("load_customers",   "r1", ["raw.customer_feed"],                 ["dw.customer"],                "2026-03-01T01:00:00Z"),
    event("build_features",   "r2", ["dw.customer", "dw.txn"],             ["fs.cust_features"],           "2026-03-01T02:00:00Z"),
    event("train_churn",      "r3", ["fs.cust_features"],                  ["model:churn@v7"],             "2026-03-01T03:00:00Z"),
    event("train_limit",      "r4", ["dw.customer"],                       ["model:credit_limit@v3"],      "2026-03-02T03:00:00Z"),
    event("train_fraud",      "r5", ["dw.txn"],                            ["model:fraud@v12"],            "2026-03-02T04:00:00Z"),
    event("report_kpi",       "r6", ["dw.customer"],                       ["bi.kpi_daily"],               "2026-03-02T05:00:00Z"),
]
print("one event, trimmed:"); print(json.dumps(events[2], indent=2)); print()

down = defaultdict(list)                       # dataset -> [(job, output, time)]
for e in events:
    for i in e["inputs"]:
        for o in e["outputs"]: down[i["name"]].append((e["job"]["name"], o["name"], e["eventTime"]))

def downstream(start):
    seen, q, paths = {start}, deque([(start, [start])]), []
    while q:
        node, path = q.popleft()
        for job, out, ts in down.get(node, []):
            if out in seen: continue
            seen.add(out); p = path + [f"--{job}-->", out]; paths.append(p); q.append((out, p))
    return paths

for p in downstream("dw.customer"):
    print(" ".join(p))
models = [p[-1] for p in downstream("dw.customer") if p[-1].startswith("model:")]
print("\nmodels downstream of dw.customer:", models)
print("not affected:", sorted({o["name"] for e in events for o in e["outputs"] if o["name"].startswith("model:")} - set(models)))
