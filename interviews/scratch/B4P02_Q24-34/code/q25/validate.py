import sys, yaml
c = yaml.safe_load(open(sys.argv[1]))
s = c["services"]["jupyter"]
problems = []
if not str(s.get("user", "")).strip(): problems.append("no user: container runs as root, files on bind mount become root-owned")
for p in s.get("ports", []):
    if not str(p).startswith("127.0.0.1:"): problems.append(f"port {p} is published on all interfaces")
if "JUPYTER_TOKEN" not in s.get("environment", {}): problems.append("no token")
dev = s["deploy"]["resources"]["reservations"]["devices"][0]
if dev.get("driver") != "nvidia" or "gpu" not in dev.get("capabilities", []): problems.append("GPU reservation malformed")
if dev.get("count") == "all": problems.append("takes every GPU on a shared box")
named = [v for v in s["volumes"] if not v.startswith(("./", "/"))]
print("named volumes used:", [v.split(":")[0] for v in named])
print("problems:", problems or "none")
sys.exit(1 if problems else 0)
