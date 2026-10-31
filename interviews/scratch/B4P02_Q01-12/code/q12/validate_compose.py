"""Validate: every depends_on with service_healthy points to a service that defines a healthcheck."""
import sys, yaml
doc = yaml.safe_load(open(sys.argv[1])); svcs = doc["services"]; errors = []
for name, s in svcs.items():
    deps = s.get("depends_on", {})
    if isinstance(deps, list): deps = {d: {"condition": "service_started"} for d in deps}
    for dep, cfg in deps.items():
        if dep not in svcs: errors.append(f"{name}: depends_on unknown service {dep}"); continue
        if cfg.get("condition") == "service_healthy" and "healthcheck" not in svcs[dep]:
            errors.append(f"{name}: waits for {dep} to be healthy but {dep} has no healthcheck")
    hc = s.get("healthcheck")
    if hc:
        if "curl" in str(hc.get("test")): errors.append(f"{name}: healthcheck uses curl; slim images often lack it")
        for k in ("interval", "timeout", "start_period", "retries"):
            if k not in hc: errors.append(f"{name}: healthcheck missing {k}")
print("OK" if not errors else "\n".join(errors)); sys.exit(1 if errors else 0)
