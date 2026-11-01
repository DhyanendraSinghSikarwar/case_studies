"""Tiny `kubectl auth can-i` model for namespaced Roles + a quota admission toy. Offline."""
import yaml, sys

docs = [d for d in yaml.safe_load_all(open(sys.argv[1])) if d]
roles = {d["metadata"]["name"]: d for d in docs if d["kind"] == "Role"}
bindings = [d for d in docs if d["kind"] == "RoleBinding"]

def allowed(sa, verb, resource, name=None, group=""):
    for b in bindings:
        if not any(s["kind"] == "ServiceAccount" and s["name"] == sa for s in b["subjects"]):
            continue
        for r in roles[b["roleRef"]["name"]]["rules"]:
            if group not in r["apiGroups"] and "*" not in r["apiGroups"]: continue
            if resource not in r["resources"] and "*" not in r["resources"]: continue
            if verb not in r["verbs"] and "*" not in r["verbs"]: continue
            if "resourceNames" in r and name not in r["resourceNames"]: continue
            return True
    return False

CHECKS = [  # (verb, resource, name, expected)
    ("get",    "secrets", "train-creds", True),
    ("get",    "secrets", "db-admin",    False),   # another Secret
    ("list",   "secrets", None,          False),   # list would expose every Secret
    ("update", "secrets", "train-creds", False),
    ("get",    "pods",    None,          False),
]
bad = 0
print("kubectl auth can-i --as=system:serviceaccount:team-a:trainer ...   (modelled, not the real command)")
for verb, res, name, expect in CHECKS:
    got = allowed("trainer", verb, res, name)
    bad += got != expect
    print(f"  {verb:6} {res + ('/' + name if name else ''):22} -> {'yes' if got else 'no':3} (expected {'yes' if expect else 'no'}){'' if got == expect else '  <-- MISMATCH'}")

print("risky-verb scan:")
for role in roles.values():
    for r in role["rules"]:
        flags = [v for v in r["verbs"] if v in ("*", "escalate", "bind", "impersonate")]
        if "*" in r["resources"]: flags.append("resources:*")
        if "secrets" in r["resources"] and ({"list", "watch"} & set(r["verbs"])): flags.append("list/watch secrets")
        if flags: print(f"  {role['metadata']['name']}: {flags} on {r['resources']} resourceNames={r.get('resourceNames')}")

# --- ResourceQuota admission toy: a pod is rejected if it would push 'used' over 'hard' ---
quota = next(d for d in docs if d["kind"] == "ResourceQuota")["spec"]["hard"]
used = {k: 0 for k in quota}
def admit(pod_name, gpus, cpu):
    want = {"requests.nvidia.com/gpu": gpus, "requests.cpu": cpu, "pods": 1}
    for k, v in want.items():
        if used[k] + v > float(quota[k]):
            print(f"  {pod_name}: REJECTED, exceeded quota {k}: used {used[k]}, requested {v}, limited {quota[k]}")
            return
    for k, v in want.items(): used[k] += v
    print(f"  {pod_name}: admitted, gpu used {used['requests.nvidia.com/gpu']}/{quota['requests.nvidia.com/gpu']}")
print("quota toy (GPU hard limit 4):")
for i, g in enumerate([2, 1, 1, 1], 1): admit(f"train-{i}", g, 4)
print("mismatches:", bad)
