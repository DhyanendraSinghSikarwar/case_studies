# Q14: pyyaml checks on the compose file: depends_on targets exist, ports, networks, volumes, env_file.
import sys, yaml, os
d = yaml.safe_load(open(sys.argv[1])); base = os.path.dirname(sys.argv[1])
svcs = d["services"]; errs = []
for n, s in svcs.items():
    deps = s.get("depends_on", {}); deps = deps if isinstance(deps, list) else list(deps)
    for t in deps:
        if t not in svcs: errs.append(f"{n}: depends_on unknown service {t}")
    for t, c in (s.get("depends_on", {}) if isinstance(s.get("depends_on"), dict) else {}).items():
        if c.get("condition") == "service_healthy" and "healthcheck" not in svcs.get(t, {}):
            errs.append(f"{n}: waits for {t} healthy but {t} has no healthcheck")
    for net in s.get("networks", []):
        if net not in d.get("networks", {}): errs.append(f"{n}: undefined network {net}")
    for v in s.get("volumes", []):
        src = v.split(":")[0]
        if not src.startswith((".", "/")) and src not in d.get("volumes", {}): errs.append(f"{n}: undefined volume {src}")
    ef = s.get("env_file");
    if ef and not os.path.exists(os.path.join(base, ef)): errs.append(f"{n}: env_file {ef} missing")
    pubs = [p for p in s.get("ports", [])]
    print(f"{n:9} published: {pubs or 'none'}")
print("ERRORS:" if errs else "all checks passed", *errs, sep="\n" if errs else " ")
