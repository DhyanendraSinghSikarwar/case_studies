"""Audit a compose file for hardening settings."""
import sys, yaml
doc = yaml.safe_load(open(sys.argv[1]))
bad = 0
for name, s in doc["services"].items():
    checks = {
      "non-root user": str(s.get("user", "0")).split(":")[0] not in ("0", "root"),
      "read_only rootfs": s.get("read_only") is True,
      "tmpfs scratch": bool(s.get("tmpfs")),
      "cap_drop ALL": "ALL" in (s.get("cap_drop") or []),
      "no-new-privileges": any(str(o).startswith("no-new-privileges") for o in s.get("security_opt", [])),
      "not privileged": not s.get("privileged", False),
      "no docker.sock": not any("docker.sock" in str(v) for v in s.get("volumes", [])),
    }
    for k, ok in checks.items():
        print(f"{name}: {'PASS' if ok else 'FAIL'} {k}"); bad += (not ok)
print("failures:", bad)
sys.exit(1 if bad else 0)
