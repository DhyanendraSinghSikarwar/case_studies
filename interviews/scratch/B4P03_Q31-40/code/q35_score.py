"""Q35: score a Pod manifest against a short hardening checklist (Pod Security 'restricted' flavoured). Not a full PSS check."""
import pathlib, sys, yaml

def score(pod):
    spec = pod["spec"]; psc = spec.get("securityContext", {}); out = []
    def add(name, ok, why=""): out.append((name, bool(ok), why))
    add("automountServiceAccountToken false", spec.get("automountServiceAccountToken") is False, "token mounted by default")
    add("no hostNetwork/hostPID/hostIPC", not any(spec.get(k) for k in ("hostNetwork", "hostPID", "hostIPC")))
    add("pod seccomp RuntimeDefault", psc.get("seccompProfile", {}).get("type") in ("RuntimeDefault", "Localhost"))
    for c in spec["containers"]:
        sc = c.get("securityContext", {}); n = c["name"]
        add(f"{n}: runAsNonRoot", psc.get("runAsNonRoot") or sc.get("runAsNonRoot"))
        add(f"{n}: not privileged", not sc.get("privileged"))
        add(f"{n}: allowPrivilegeEscalation false", sc.get("allowPrivilegeEscalation") is False)
        add(f"{n}: readOnlyRootFilesystem", sc.get("readOnlyRootFilesystem") is True)
        add(f"{n}: drop ALL capabilities", "ALL" in sc.get("capabilities", {}).get("drop", []))
        img = c["image"]
        add(f"{n}: image pinned (digest or non-latest tag)", "@sha256:" in img or (":" in img.split("/")[-1] and not img.endswith(":latest")))
        add(f"{n}: memory limit set", "memory" in c.get("resources", {}).get("limits", {}))
    return out

for f in sys.argv[1:]:
    pod = yaml.safe_load(pathlib.Path(f).read_text())
    res = score(pod); ok = sum(r[1] for r in res)
    print(f"== {pathlib.Path(f).name}: {ok}/{len(res)}")
    for name, good, why in res:
        if not good: print(f"   FAIL {name} {('(' + why + ')') if why else ''}")
