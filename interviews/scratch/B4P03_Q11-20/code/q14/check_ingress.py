"""Check every Ingress backend names a real Service (same manifest set) and a port it exposes."""
import sys, yaml

def main(path):
    docs = [d for d in yaml.safe_load_all(open(path)) if d]
    services = {d["metadata"]["name"]: d for d in docs if d["kind"] == "Service"}
    secrets = {d["metadata"]["name"] for d in docs if d["kind"] == "Secret"}
    problems = 0
    for ing in (d for d in docs if d["kind"] == "Ingress"):
        name = ing["metadata"]["name"]
        spec = ing["spec"]
        if "ingressClassName" not in spec:
            print(f"WARN {name}: no ingressClassName (relies on a default class, or no controller picks it up)"); problems += 1
        for t in spec.get("tls", []):
            if t["secretName"] not in secrets:
                print(f"NOTE {name}: TLS secret {t['secretName']!r} is not in this file (fine if created elsewhere)")
        for rule in spec["rules"]:
            for p in rule["http"]["paths"]:
                be = p["backend"]["service"]
                svc = services.get(be["name"])
                where = f"{rule.get('host', '*')}{p['path']}"
                if svc is None:
                    print(f"FAIL {where}: backend Service {be['name']!r} not found"); problems += 1
                    continue
                ports = svc["spec"]["ports"]
                ok = any(("number" in be["port"] and pt["port"] == be["port"]["number"]) or
                         ("name" in be["port"] and pt.get("name") == be["port"]["name"]) for pt in ports)
                if not ok:
                    print(f"FAIL {where}: Service {be['name']!r} has no port {be['port']}; it exposes {[pt['port'] for pt in ports]}"); problems += 1
                else:
                    print(f"ok   {where} -> {be['name']}:{be['port']}")
    print("problems:", problems)

main(sys.argv[1])
