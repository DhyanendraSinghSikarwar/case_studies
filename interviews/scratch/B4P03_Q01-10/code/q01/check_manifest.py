"""Cross-checks that schema validation cannot do: labels, selectors, ports."""
import sys, yaml

docs = [d for d in yaml.safe_load_all(open(sys.argv[1])) if d]
dep = next(d for d in docs if d["kind"] == "Deployment")
svc = next(d for d in docs if d["kind"] == "Service")

tmpl_labels = dep["spec"]["template"]["metadata"]["labels"]
dep_sel = dep["spec"]["selector"]["matchLabels"]
svc_sel = svc["spec"]["selector"]
ports = {p["name"]: p["containerPort"] for c in dep["spec"]["template"]["spec"]["containers"]
         for p in c.get("ports", [])}

def subset(sel, labels):
    return all(labels.get(k) == v for k, v in sel.items())

problems = []
if not subset(dep_sel, tmpl_labels):
    problems.append("Deployment selector does not match its own pod template labels")
if not subset(svc_sel, tmpl_labels):
    problems.append("Service selector matches no pod: it would have zero endpoints")
for sp in svc["spec"]["ports"]:
    tp = sp["targetPort"]
    if isinstance(tp, str) and tp not in ports:
        problems.append(f"Service targetPort name {tp!r} is not a named containerPort")

print("replicas:", dep["spec"]["replicas"])
print("service reaches pods with labels:", svc_sel, "->", "OK" if subset(svc_sel, tmpl_labels) else "NO MATCH")
print("targetPort", svc["spec"]["ports"][0]["targetPort"], "resolves to container port",
      ports.get(svc["spec"]["ports"][0]["targetPort"]))
print("problems:", problems or "none")
sys.exit(1 if problems else 0)
