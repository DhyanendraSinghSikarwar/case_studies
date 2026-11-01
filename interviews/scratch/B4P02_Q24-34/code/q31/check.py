import subprocess, sys, yaml

def cfg(*files, profiles=()):
    cmd = ["docker", "compose"]
    for f in files: cmd += ["-f", f]
    for p in profiles: cmd += ["--profile", p]
    cmd += ["config"]
    return yaml.safe_load(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)

def gpu_ok(svc):
    devs = svc.get("deploy", {}).get("resources", {}).get("reservations", {}).get("devices", [])
    return any(d.get("driver") == "nvidia" and "gpu" in d.get("capabilities", []) for d in devs)

dev  = cfg("compose.yml", "compose.override.yml")
prod = cfg("compose.yml", "compose.prod.yml")
dev_all = cfg("compose.yml", "compose.override.yml", profiles=["dev", "monitoring"])
print("dev  services (no profile):      ", sorted(dev["services"]))
print("dev  services (+dev,monitoring): ", sorted(dev_all["services"]))
print("prod services:                   ", sorted(prod["services"]))
for name, c in [("dev", dev), ("prod", prod)]:
    a = c["services"]["api"]
    print(f"{name}: restart={a.get('restart')!r} gpu_reserved={gpu_ok(a)} ports={[ (p.get('host_ip','*'), p['published']) for p in a.get('ports', [])]} mem_limit={a['deploy']['resources']['limits']['memory']}")
assert gpu_ok(prod["services"]["api"]) and prod["services"]["api"]["restart"] == "always"
assert all(p.get("host_ip") == "127.0.0.1" for p in prod["services"]["api"]["ports"])
print("assertions OK: prod keeps GPU reservation, restarts always, publishes on localhost only")
