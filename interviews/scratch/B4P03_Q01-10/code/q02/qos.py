"""Classify QoS from a pod spec and sanity-check resource quantities."""
import re, sys, yaml

UNITS = {"Ki": 2**10, "Mi": 2**20, "Gi": 2**30, "Ti": 2**40,
         "k": 10**3, "M": 10**6, "G": 10**9, "T": 10**12, "m": 1e-3, "": 1}

def qty(s):
    m = re.fullmatch(r"(\d+(?:\.\d+)?)(Ki|Mi|Gi|Ti|k|M|G|T|m|)", str(s))
    if not m:
        raise ValueError(f"bad quantity {s!r}")
    return float(m.group(1)) * UNITS[m.group(2)]

def qos(pod_spec):
    ctrs = pod_spec["containers"] + pod_spec.get("initContainers", [])
    any_set, all_guaranteed = False, True
    for c in pod_spec["containers"]:
        r = c.get("resources", {})
        req, lim = r.get("requests", {}), r.get("limits", {})
        req = {**lim, **req}                       # requests default to limits
        if req or lim:
            any_set = True
        for res in ("cpu", "memory"):
            if res not in lim or res not in req or qty(req[res]) != qty(lim[res]):
                all_guaranteed = False
    if not any_set:
        return "BestEffort"
    return "Guaranteed" if all_guaranteed else "Burstable"

def check_quantities(pod_spec):
    out = []
    for c in pod_spec["containers"]:
        r = c.get("resources", {})
        for res, v in {**r.get("requests", {}), **r.get("limits", {})}.items():
            qty(v)                                  # raises on junk such as "x"
        for res, v in r.get("requests", {}).items():
            lim = r.get("limits", {}).get(res)
            if lim is not None and qty(v) > qty(lim):
                out.append(f"{c['name']}: {res} request {v} > limit {lim}")
    return out

EVICTION_ORDER = {"BestEffort": 0, "Burstable": 1, "Guaranteed": 2}   # lower = evicted earlier (roughly)

if __name__ == "__main__":
    rows = []
    for d in yaml.safe_load_all(open(sys.argv[1])):
        spec = d["spec"]["template"]["spec"] if d["kind"] == "Deployment" else d["spec"]
        rows.append((d["metadata"]["name"], qos(spec), check_quantities(spec)))
    for name, q, issues in sorted(rows, key=lambda r: EVICTION_ORDER[r[1]]):
        print(f"{name:26s} {q:11s} issues={issues or 'none'}")
    # mixed case: memory limit only, no cpu -> Burstable
    print("memory-only limit  ->", qos({"containers": [{"name": "a", "resources": {"limits": {"memory": "1Gi"}}}]}))
    print("limits only (cpu+mem)->", qos({"containers": [{"name": "a", "resources": {"limits": {"cpu": "1", "memory": "1Gi"}}}]}))
    try:
        qty("x")
    except ValueError as e:
        print("junk quantity caught:", e)
