"""Cross-check a Service against the Deployment(s) in the same file. Static checks only."""
import sys, yaml

def check(path):
    docs = list(yaml.safe_load_all(open(path)))
    svcs = [d for d in docs if d["kind"] == "Service"]
    deps = [d for d in docs if d["kind"] == "Deployment"]
    problems = []
    for s in svcs:
        sel = s["spec"].get("selector", {})
        matches = [d for d in deps if all(d["spec"]["template"]["metadata"]["labels"].get(k) == v for k, v in sel.items())]
        if not matches:
            problems.append(f"Service {s['metadata']['name']}: selector {sel} matches no pod template -> endpoints will be empty")
            matches = [d for d in deps if d["metadata"]["name"] == s["metadata"]["name"]]   # keep checking the same-named Deployment
        for d in matches:
            c = d["spec"]["template"]["spec"]["containers"][0]
            cports = {p["containerPort"] for p in c.get("ports", [])}
            for sp in s["spec"]["ports"]:
                tp = sp.get("targetPort", sp["port"])
                if tp not in cports:
                    problems.append(f"Service port {sp['port']} -> targetPort {tp}, but container declares {sorted(cports)}")
            rp = c.get("readinessProbe", {}).get("httpGet", {}).get("port")
            if rp is not None and rp not in cports:
                problems.append(f"readinessProbe port {rp} is not a declared containerPort {sorted(cports)}: pods may never become Ready")
            args = c.get("args", []) + c.get("command", [])
            for i, a in enumerate(args):
                if a in ("127.0.0.1", "localhost") or (a.startswith("--host=") and a.split("=")[1] in ("127.0.0.1", "localhost")):
                    problems.append(f"app binds {a}: only reachable inside the pod, use 0.0.0.0")
    # selector vs Deployment's own matchLabels must match template labels
    for d in deps:
        ml = d["spec"]["selector"]["matchLabels"]; tl = d["spec"]["template"]["metadata"]["labels"]
        if any(tl.get(k) != v for k, v in ml.items()):
            problems.append(f"Deployment {d['metadata']['name']}: selector.matchLabels does not match template labels")
    return problems

for f in sys.argv[1:]:
    probs = check(f)
    print(f"== {f}: {len(probs)} problem(s)")
    for p in probs: print("  -", p)
