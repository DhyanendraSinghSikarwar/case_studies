"""Simplified NetworkPolicy evaluator for INGRESS. Model: a pod is 'isolated' if any policy selects it;
isolated pods accept only traffic allowed by the union of rules of the policies that select them.
Ignores egress, ipBlock, named ports, endPort. A teaching model, not a CNI."""
import yaml

docs = [d for d in yaml.safe_load_all(open("netpol.yaml")) if d["kind"] == "NetworkPolicy"]
ns_labels = {"gateway": {"kubernetes.io/metadata.name": "gateway"},
             "ml-serving": {"kubernetes.io/metadata.name": "ml-serving"},
             "research": {"kubernetes.io/metadata.name": "research"}}

def match(sel, labels):
    return all(labels.get(k) == v for k, v in (sel or {}).get("matchLabels", {}).items())

def allowed(src, dst, port, policies):
    selecting = [p for p in policies if p["metadata"]["namespace"] == dst["ns"]
                 and match(p["spec"]["podSelector"], dst["labels"])
                 and "Ingress" in p["spec"].get("policyTypes", [])]
    if not selecting:
        return True, "no policy selects the destination: open"
    for p in selecting:
        for rule in p["spec"].get("ingress", []):
            ports_ok = not rule.get("ports") or any(r["port"] == port for r in rule["ports"])
            for peer in rule.get("from", []):
                ns_ok = "namespaceSelector" not in peer or match(peer["namespaceSelector"], ns_labels[src["ns"]])
                pod_ok = "podSelector" not in peer or match(peer["podSelector"], src["labels"])
                if "podSelector" in peer and "namespaceSelector" not in peer and src["ns"] != dst["ns"]:
                    pod_ok = False                      # bare podSelector means same namespace only
                if ns_ok and pod_ok and ports_ok:
                    return True, f"allowed by {p['metadata']['name']}"
    return False, "isolated and no rule matches: dropped"

dst = {"ns": "ml-serving", "labels": {"app": "model-api"}}
tests = [
  ("envoy in gateway -> model-api:8080", {"ns": "gateway", "labels": {"app": "envoy"}}, dst, 8080),
  ("envoy in gateway -> model-api:9000", {"ns": "gateway", "labels": {"app": "envoy"}}, dst, 9000),
  ("notebook in research -> model-api:8080", {"ns": "research", "labels": {"app": "notebook"}}, dst, 8080),
  ("other pod in gateway -> model-api:8080", {"ns": "gateway", "labels": {"app": "debug"}}, dst, 8080),
  ("anyone -> pod in a namespace with no policy", {"ns": "research", "labels": {}}, {"ns": "research", "labels": {"app": "x"}}, 80),
]
for name, s, d, port in tests:
    ok, why = allowed(s, d, port, docs)
    print(f"{'ALLOW' if ok else 'DENY ':5} {name:45} ({why})")
