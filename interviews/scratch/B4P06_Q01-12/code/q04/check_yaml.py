import yaml
d = yaml.safe_load(open("probes.yaml"))
for k, v in d.items():
    print(k, v["httpGet"]["path"], "period", v["periodSeconds"], "fail", v["failureThreshold"])
assert d["livenessProbe"]["httpGet"]["path"] != d["readinessProbe"]["httpGet"]["path"]
print("max startup window:", d["startupProbe"]["periodSeconds"] * d["startupProbe"]["failureThreshold"], "s")
