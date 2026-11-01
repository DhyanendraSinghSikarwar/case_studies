import yaml, pathlib
d = yaml.safe_load(open(pathlib.Path(__file__).with_name("q38_k8s_fragment.yaml")))["spec"]
c = d["containers"][0]; grace = d["terminationGracePeriodSeconds"]
pre = int(c["lifecycle"]["preStop"]["exec"]["command"][1]); uv = int(c["command"][c["command"].index("--timeout-graceful-shutdown") + 1])
print("YAML parses; grace", grace, "| preStop sleep", pre, "| uvicorn graceful timeout", uv, "| budget ok (pre + uvicorn < grace):", pre + uv < grace)
assert pre + uv < grace and "readinessProbe" in c
