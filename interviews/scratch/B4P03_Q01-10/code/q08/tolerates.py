"""Would this pod tolerate these node taints? Mirrors the Kubernetes matching rules (NoSchedule/NoExecute)."""
import sys, yaml

def tol_matches(tol, taint):
    if tol.get("effect") and tol["effect"] != taint["effect"]:
        return False
    op = tol.get("operator", "Equal")
    if op == "Exists":
        return not tol.get("key") or tol["key"] == taint["key"]     # empty key + Exists matches all
    return tol.get("key") == taint["key"] and tol.get("value", "") == taint.get("value", "")

def tolerates(pod_spec, taints):
    blocking = [t for t in taints if t["effect"] in ("NoSchedule", "NoExecute")
                and not any(tol_matches(x, t) for x in pod_spec.get("tolerations", []))]
    return not blocking, blocking

def check_gpu(pod_spec):
    errs = []
    for c in pod_spec["containers"]:
        r = c.get("resources", {})
        lim, req = r.get("limits", {}), r.get("requests", {})
        g = lim.get("nvidia.com/gpu", req.get("nvidia.com/gpu"))
        if g is None:
            continue
        if not str(g).isdigit():
            errs.append(f"{c['name']}: GPU count {g!r} must be a whole number")
        if "nvidia.com/gpu" in req and "nvidia.com/gpu" not in lim:
            errs.append(f"{c['name']}: GPU in requests without limits is rejected")
        if "nvidia.com/gpu" in req and "nvidia.com/gpu" in lim and str(req["nvidia.com/gpu"]) != str(lim["nvidia.com/gpu"]):
            errs.append(f"{c['name']}: GPU request must equal limit")
    return errs

if __name__ == "__main__":
    dep = next(yaml.safe_load_all(open(sys.argv[1])))
    spec = dep["spec"]["template"]["spec"]
    nodes = {
        "gpu-node-1":  [{"key": "nvidia.com/gpu", "value": "present", "effect": "NoSchedule"}],
        "cpu-node-1":  [],
        "spot-gpu-2":  [{"key": "nvidia.com/gpu", "value": "present", "effect": "NoSchedule"},
                        {"key": "spot", "value": "true", "effect": "NoSchedule"}],
        "pref-node-3": [{"key": "nvidia.com/gpu", "value": "present", "effect": "PreferNoSchedule"}],
    }
    for n, taints in nodes.items():
        ok, why = tolerates(spec, taints)
        print(f"{n:12s} taints={len(taints)} tolerated={ok}", "" if ok else f"blocked by {[t['key'] for t in why]}")
    print("node label match for nodeSelector pool=gpu is a separate check (labels, not taints)")
    print("GPU spec errors:", check_gpu(spec) or "none")
    bad = {"containers": [{"name": "c", "resources": {"requests": {"nvidia.com/gpu": "0.5"}}}]}
    print("fractional/request-only case:", check_gpu(bad))
