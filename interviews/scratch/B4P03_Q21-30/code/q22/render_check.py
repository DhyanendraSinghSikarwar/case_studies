"""NOT helm. A hand-written Python mirror of chart/templates/deployment.yaml logic, used to
(1) check values against values.schema.json, (2) dump the YAML the template should produce,
(3) check the template text still contains the guards we rely on."""
import json, sys, yaml, jsonschema, copy, tempfile, subprocess, os
TMP = tempfile.mkdtemp()

CHART = "chart"
schema = json.load(open(f"{CHART}/values.schema.json"))
defaults = yaml.safe_load(open(f"{CHART}/values.yaml"))

def merge(a, b):
    out = copy.deepcopy(a)
    for k, v in b.items():
        out[k] = merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out

def render(overrides):
    v = merge(defaults, overrides)
    errs = sorted(jsonschema.Draft7Validator(schema).iter_errors(v), key=lambda e: list(e.path))
    if errs:
        return None, [f"schema: {'.'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errs]
    if not v["modelUri"]:                                   # mirrors: required "..." .Values.modelUri
        return None, ["required: modelUri is required (--set modelUri=s3://...)"]
    limits = dict(v["resources"]["limits"])
    if int(v["gpu"]["count"]) > 0:                          # mirrors: if gt (int .Values.gpu.count) 0
        limits["nvidia.com/gpu"] = v["gpu"]["count"]
    spec = {"containers": [{"name": "server",
        "image": f'{v["image"]["repository"]}:{v["image"]["tag"] or "1.4.2"}',   # default .Chart.AppVersion
        "imagePullPolicy": v["image"]["pullPolicy"],
        "env": [{"name": "MODEL_URI", "value": v["modelUri"]}],
        "ports": [{"containerPort": v["service"]["port"]}],
        "resources": {"requests": v["resources"]["requests"], "limits": limits}}]}
    if v["tolerations"]:                                    # mirrors: with .Values.tolerations
        spec["tolerations"] = v["tolerations"]
    labels = {"app.kubernetes.io/name": "model-api", "app.kubernetes.io/instance": "rel"}
    return {"apiVersion": "apps/v1", "kind": "Deployment",
            "metadata": {"name": "model-api", "labels": labels},
            "spec": {"replicas": v["replicaCount"],
                     "selector": {"matchLabels": {"app.kubernetes.io/name": "model-api"}},
                     "template": {"metadata": {"labels": labels}, "spec": spec}}}, []

cases = {
  "cpu-only": {"modelUri": "s3://bucket/m1"},
  "gpu+toleration": {"modelUri": "s3://bucket/m1", "gpu": {"count": 1},
        "tolerations": [{"key": "nvidia.com/gpu", "operator": "Exists", "effect": "NoSchedule"}]},
  "missing modelUri": {},
  "bad pullPolicy + replicas 0": {"modelUri": "x", "image": {"pullPolicy": "Sometimes"}, "replicaCount": 0},
  "gpu count as string": {"modelUri": "x", "gpu": {"count": "two"}},
}
for name, ov in cases.items():
    doc, errs = render(ov)
    print(f"=== {name}")
    if errs:
        print("REJECTED:"); [print("  -", e) for e in errs]
    else:
        path = os.path.join(TMP, name.split("+")[0] + ".yaml")
        yaml.safe_dump(doc, open(path, "w"), sort_keys=False)
        r = subprocess.run(["kubernetes-validate", "--strict", path], capture_output=True, text=True)
        print("kubernetes-validate --strict rc =", r.returncode, "|", r.stdout.strip().split(" against")[-1])
        lim = doc["spec"]["template"]["spec"]["containers"][0]["resources"]["limits"]
        print("OK limits:", lim, "| tolerations:", "tolerations" in doc["spec"]["template"]["spec"])

tpl = open(f"{CHART}/templates/deployment.yaml").read()
for needle in ["required ", "toYaml", "nindent", "with .Values.tolerations", "gt (int .Values.gpu.count) 0", "include "]:
    print(f"template contains {needle!r}:", needle in tpl)
